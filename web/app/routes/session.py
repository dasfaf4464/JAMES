"""
[Session 페이지]
Session 페이지 - Session 페이지는 사용자들을 연결하며 질문을 올리거나 메모를 작성할 수 있습니다.

router
    - session(페이지 제공)
    - is_session_create(세션이 생성되었는지 확인)
    - is_session_locked(세션에 비밀번호가 있는지 확인)
    - get_previous_category(세션의 카테고리들을 제공)
    - refine_text(텍스트 정제)
    - view_questions_category(카테고리에 해당하는 게시글 보기)

ws
    - join_session(세션에 참가)
    - leave_session(세션에서 퇴장)
    - select_text(텍스트 리스트중 하나를 게시)
    - pick_text(텍스트에 좋아요)
    - delete_text(게시한 질문을 삭제)

작성자 : 조해천
"""

from flask import Blueprint, request, render_template, jsonify
from flask_socketio import join_room, leave_room, emit, send

import app.models.session_read_services as session_read_services
import app.models.session_write_services as session_write_services
import app.models.session_activity_services as session_activity_services
import app.models.post_services as post_services

import re

session_bp = Blueprint("session", __name__)
get_session_info_bp = Blueprint("get_session_info", __name__, url_prefix="/api/session")
pass_session_lock_bp = Blueprint(
    "pass_session_lock", __name__, url_prefix="/api/session"
)
get_previous_category_bp = Blueprint(
    "get_privious_category", __name__, url_prefix="/api/post"
)
refine_text_bp = Blueprint("refine_text", __name__, url_prefix="/api/post")
get_category_questions_bp = Blueprint(
    "get_category_questions", __name__, url_prefix="/api/post"
)


@session_bp.route("/session/<sessioncode>", methods=["GET"])
def session(sessioncode):
    """
    session 페이지를 반환하는 API입니다.

    Request:
        Path: "/session/<session_code>" (GET)
        Path Params:
            - sessioncode (str): 세션의 고유 코드.

    Response:
        HTML:
            - session.html
    """

    if re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", sessioncode):
        return render_template("session.html")
    else:
        return render_template("session_error.html")


@get_session_info_bp.route("/<sessioncode>/get/info", methods=["GET"])
def get_session_info(sessioncode):
    """
    세션이 생성되었는지 확인하고 비밀번호 유무를 확인하는 API입니다.

    Request
        Path: "/api/session/<sessioncode>/get/info" (GET)
        Path Params:
            - sessioncode (str): 세션의 고유 코드.

    Response:
    """
    session_info = session_read_services.get_session_info(sessioncode)
    if session_info:
        session_exists = True
        if session_info.get("pw") == None:
            session_locked = False
        else:
            session_locked = True
    else:
        session_exists = False
        return jsonify({"session_exists": session_exists})

    return jsonify({"session_exists": session_exists, "session_lock": session_locked})


@pass_session_lock_bp.route("/<sessioncode>/pass", methods=["POST"])
def pass_session_lock(sessioncode):
    """
    세션 비밀번호 확인 API

    Request:
        POST /api/session/<sessioncode>/pass
        Body(JSON): { password: str }

    Response:
        JSON: { valid: bool }
    """
    data = request.get_json()

    session_info = session_read_services.get_session_info(sessioncode)
    if not session_info:
        return jsonify({"valid": False}), 404

    correct_password = session_info.get("pw")
    input_password = data.get("password")

    if correct_password == input_password:
        return jsonify({"valid": True})
    else:
        return jsonify({"valid": False})


@get_previous_category_bp.route("/<sessioncode>/get/previous_category", methods=["GET"])
def get_previous_category(sessioncode):
    """
    세션에 저장되어있는 카테고리를 반환하는 API입니다.

    Request:
        Path: "/api/post/<sessioncode>/get/previous_category" (GET)
        Path Params:
            - sessioncode (str): 세션의 고유 코드.

    Response:
        JSON(List):
            - category (str): 대분류/중분류
            - count (int): 카테고리 개수
    """
    post_services.get_all_posts()
    # 사용 안함


@refine_text_bp.route("/<sessioncode>/refine_text", methods=["POST"])
def refine_text(sessioncode):
    """
    내용을 정제하는 API입니다.

    Request:
        Path: "/api/post/<sessioncode>/refine_text
        Path Params:
            - sessioncode (str):세션의 고유 코드.
        Cookies:
            - user_key (str): 사용자 인증 키
            - temporary (bool): 임시 사용자
        Body (JSON):
            - text (str): 텍스트
            - category (str): 카테고리

    Response:
        JSON:
            refined_text (str): 정제된 텍스트
            category (str): 카테고리 정보
            number (int): 저장된 index번호
    """
    data = request.get_json()
    cookie = request.cookies

    post_nums = post_services.send_llm(
        cookie.get("user_key"), sessioncode, data.get("content")
    )
    post_list = post_services.get_post_by_keys(post_nums)
    response_list = []
    for post in post_list:
        res = {
            "content": post.get("llm"),
            "category": {
                "main": post.get("main"),
                "sub": post.get("sub"),
                "minor": post.get("minor"),
            },
            "key": post.get("post_key"),
            "error": post.get("error"),
        }
        response_list.append(res)
    return jsonify(response_list)


@get_category_questions_bp.route("/<sessioncode>/get/questions", methods=["GET"])
def get_category_questions(sessioncode):
    """
    해당 카테고리의 게시된 질문을 가져옵니다.

    Request:
        Path: "/api/post/<sessioncode>/get/questions"
        Path Params:
            - sessioncode (str): 세션의 고유 코드

    Query Params:
        - category (str): 받아올 카테고리(메이저/서브)
        - start (int): 시작 인덱스
        - count (int): 받아올 개수

    Response:
        JSON (List):
            - original_text (str): 원본 텍스트
            - refined_text (str): 정제 텍스트
            - memo (str): 메모
            - category (str): 마이너 카테고리
    """
    category = request.args.get("category", "")
    try:
        main, sub = category.split("/")
    except ValueError:
        return jsonify({"error": "Invalid category format. Use 'main/sub'."}), 400

    try:
        start = int(request.args.get("start", 0))
        count = int(request.args.get("count", 10))
    except ValueError:
        return jsonify({"error": "Invalid start or count parameter."}), 400

    post_list = post_services.get_post_by_category_in_session(sessioncode, main, sub)
    return jsonify(post_list[start : start + count])


def register_socket(socketio):
    @socketio.on("connect")
    def connect():
        cookie = request.cookies
        session_code = request.args.get("session_code")
        session_activity_services.join_session(cookie.get("user_key"), session_code)
        if cookie.get("temporary") == "False":
            session_write_services.add_my_session(cookie.get("user_key"), session_code)
        category_count = post_services.get_session_category(session_code)
        emit("init_categories", category_count)

        join_room(session_code)

    @socketio.on("disconnect")
    def disconnect():
        cookie = request.cookies
        session_activity_services.leave_session(
            cookie.get("user_key"), request.args.get("session_code")
        )
        leave_room(request.args.get("session_code"))

    @socketio.on("select")
    def select(data):
        post_services.select_post(data.get("session_code"), data.get("key"))
        post = post_services.get_post_by_keys([data.get("key")])
        category = post[0].get("main") + "/" + post[0].get("sub")
        emit("update", {"category": category}, room=data.get("session_code"))
