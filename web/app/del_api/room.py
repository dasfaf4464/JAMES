"""
세션에 대한 api를 관리하는 모듈입니다.
"""

from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO, join_room, leave_room, emit
from app.util.db_manager import (
    mariadb_user_manager,
    mariadb_admin_manager,
    redis_manager,
)
from app.util.chat_manager import ChatManager
from app.util.llm_manager import llmManager

createSession_bp = Blueprint("create_session", __name__, url_prefix="/room")
joinSession_bp = Blueprint("join_session", __name__, url_prefix="/room")
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

    session = tuple()
    session = ChatManager.create_room(
        admin_key=admin_key,
        title=title,
        description=description,
        is_temporary=is_temporary,
    )

    if session:  # 세션 생성 성공
        return jsonify({"session_code": session, "error": False})

    return jsonify({"error": "db_error"}), 500


@joinSession_bp.route("/join", methods=["POST"])
def join_session():
    request_data = request.get_json()
    request_cookie = request.cookies
    user_key = request_cookie.get("user_key")

    if ChatManager.user_join(request_data.get("session_code"), user_key):
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})


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
    request_data = request.get_json()
    request_cookie = request.cookies
    from_llm = llmManager[0]._request_llm(
        request_cookie.get("user_key"),
        request_data.get("session_code"),
        request_data.get("content"),
    )

    if from_llm is False:
        return jsonify({"error_content": "length error"}), 400

    response_data = {
        "count": 3,
        "text": [
            {
                "content": item["llm"],
                "category": item["category"],
                "key": item["key"],
                "error": item["error"],
            }
            for item in from_llm
        ],
    }

    return jsonify(response_data), 200


def init_socketio(socketio):
    @socketio.on("connect")
    def handle_connect(data):
        """
        연결 테스트
        """
        print(request.sid + "   on   " + request.args.get("session_code"))

    @socketio.on("disconnect")
    def handle_disconnect(data):
        user_key = request.cookies.get("user_key")
        session_code = request.args.get("session_code")
        print(f"[DISCONNECT] {request.sid} disconnected.")
        ChatManager.user_leave(session_code, user_key)
        leave_room(session_code)

    @socketio.on("error")
    def handle_error(data):
        """ """

    @socketio.on("send_llm", namespace="/")
    def handle_select_llm(data):
        mariadb_admin_manager.put_sql(
            "UPDATE fromllm set selected = 1 WHERE `key` = %s;", (data.get("key"),)
        )
        select = mariadb_user_manager.select(
            "selected_llm_responses", {"`key`": data.get("key")}
        )
        select = select[0]
        i = 0
        with redis_manager.redis_client.lock(
            f"session:{select.get('session')}:category:lock", blocking_timeout=5
        ):
            test = redis_manager.get_hash(
                name=f"session:{select.get('session')}:category",
                key=select.get("main") + "/" + select.get("sub"),
            )
            if test == None:
                i = 1
            else:
                i = int(test) + 1
                
            redis_manager.put_hash(
                name=f"session:{select.get('session')}:category",
                data={select.get("main") + "/" + select.get("sub"): i},
            )
            emit("update", {"category": select.get("main") + "/" + select.get("sub")})

    @socketio.on("session", namespace="/")
    def handle_join_session(data):
        """
        세션에 입장해서 카테고리 정보 주기
        """
        session_code = data

        if session_code:
            join_room(session_code)
            print(f"{request.sid} joined room: {session_code}")
        else:
            print(f"{request.sid} tried to connect without a session_code.")

    @socketio.on("join_category", namespace="/")
    def handle_join_category(data):
        """
        유저가 선택한 카테고리를 받았을 때 카테고리 정보를 전송
        """
        categorie = request.args.get("session_code")

    @socketio.on("disconnect_category", namespace="/")
    def handle_disconnect_category(data):
        """
        유저가 다른 카테고리를 선택했을 때 연결 종료 - 이후 새로운 카테고리에 연결
        """
