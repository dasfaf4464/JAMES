"""
세션에 대한 api를 관리하는 모듈입니다.
"""

from flask import Blueprint, request, make_response, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
import json
from app.manager.db_manager import (
    mariadb_user_manager,
    mariadb_admin_manager,
    redis_manager,
)
from app.manager.chat_manager import ChatManager, active_sessions
from app.manager.llm_manager import llmManager

createSession_bp = Blueprint("create_session", __name__, url_prefix="/room")
joinRoom_bp = Blueprint("join_room", __name__, url_prefix="/room")
sendtoLLM_bp = Blueprint("sendtollm", __name__, url_prefix="/room")


@createSession_bp.route("/create", methods=["POST"])
def create_sesison():
    """
    사용자가 보낸 options 에 따라 세션을 생성합니다.
    세션은 서버에 인스턴스로 존재하고 각 옵셥을 확인하거나 사용자를 확일할 때 사용됩니다.
    Content Type: Application/JSON
    Request: {
        *user_key (str): 호스트가 될 유저 키
        session_title (str): 세션 제목
        is_temporary (boolean): 임시 세션 또는 영구 세션
        is_open (boolean): 공개 세션 또는 비공개 세션
        password (str): 비공개시 사용할 비밀번호
        *쿠키에서 가져옴
    }

    해당 옵션을 가진 세션 인스턴스를 생성합니다.
    세션 인스턴스는 리스트에 등록됩니다.


    Response: {
        is_success (boolean): 세션
    }
    """
    request_data = request.get_json()
    request_cookie = request.cookies

    title = request_data.get("title")
    description = request_data.get("description")
    temp = request_data.get("temporary")
    admin_key = request_cookie["user_key"]

    if temp == "temporary":
        is_temporary = 1
    else:
        is_temporary = 0

    session_code = ChatManager.create_room(
        admin_key=admin_key, title=title, description=description, is_temporary=is_temporary
    )
    if not mariadb_admin_manager.insert(
        table="sessioninfo",
        data={
            "name": title,
            "description": description,
            "session_key": session_code,
            "host": admin_key,
            "is_temporary": is_temporary
        },
    ):
        print(active_sessions)
        active_sessions.pop(session_code)
        print("세션 db저장 오류")
        print(active_sessions)
        return jsonify({'error': "db_error"}), 500

    return jsonify({'session_code': session_code, 'error': False})


@joinRoom_bp.route("/join", methods=["GET"])
def user_join_room():
    """
    session 페이지 진입시 사용자 정보를 보내고 웹소켓을 연결합니다.
    """

    data = request.get_json()
    return


@sendtoLLM_bp.route("/llm", methods=["POST", "GET"])
def send_to_llm():
    """
    사용자가 보내려 하는 메시지를 가공하여 LLM으로 보냅니다.
    Content-Type: text/plain

    request:
        text/plain 문자열

    response:
        JSON { "count": int, "text": str or null, "error": int }
    """
    request_data = request.get_data(as_text=True)
    from_llm = llmManager[0]._request_llm(request_data)

    if from_llm is False:
        return jsonify({"error_content": "length error"}), 400

    success_list, fail_list, warn_list = from_llm
    error = 0

    combined = success_list + warn_list

    if len(warn_list) > 0:
        error = 2
    if len(fail_list) > 0:
        combined = []
        error = 1

    response_data = {
        "count": len(combined),
        "text": [
            {
                "original": request_data,
                "content": item["content"],
                "category": item["category"],
            }
            for item in combined
        ],
        "error": error,
    }
    return jsonify(response_data), 200


def init_socketio(socketio):
    @socketio.on("connect")
    def handle_connect(data):
        session_code = request.args.get("session_code")

        if session_code:
            join_room(session_code)
            print(f"{request.sid} joined room: {session_code}")
            emit(
                "system_message",
                f"자동으로 세션 {session_code} 방에 입장하였습니다.",
                room=request.sid,
            )
        else:
            print(f"{request.sid} tried to connect without a session_code.")
            emit("error", "세션 코드가 제공되지 않았습니다.", room=request.sid)

    @socketio.on("disconnect")
    def handle_disconnect(data):
        """
        사용자의 소켓 연결이 끊겼을 때 실행됩니다.
        """
        print(f"[DISCONNECT] {request.sid} disconnected.")

    @socketio.on("error")
    def handle_error(data):
        """ """

    @socketio.on("test")
    def test(data: str):
        print(data)

    @socketio.on("select_llm", namespace="/")
    def handle_select_llm(data):
        """
        Request :
            session_code (str):
            user_key (str):
            original_text (str):
            selected_text (str):
            category : {
                main (str):
                sub (str):
                minor (str):
            }
            with_origianl (bool):

        Response
        """
        data
