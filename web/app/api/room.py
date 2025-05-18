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


@createSession_bp.route("/create")
def craete_sesison():
    """
    session을 만드는
    """
    ChatManager.create_room()
    return


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
    from_llm = llmManager[2]._request_llm(request_data)

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
            {"content": item["content"], "category": item["category"]}
            for item in combined
        ],
        "error": error,
    }
    return jsonify(response_data), 200


def init_socketio(socketio):
    @socketio.on("connect")
    def handle_connect():
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
    def handle_disconnect():
        """
        사용자의 소켓 연결이 끊겼을 때 실행됩니다.
        어떤 방에 속해 있었는지는 이 시점에서 직접 알 수는 없지만,
        필요하면 서버 측에서 session_code → sid 매핑을 따로 관리해둘 수 있습니다.
        """
        print(f"[DISCONNECT] {request.sid} disconnected.")

    @socketio.on("error")
    def handle_error():
        """ """

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
        session = active_sessions.get(session_code)
