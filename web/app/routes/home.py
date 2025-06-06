"""
[Home 페이지]
Home 페이지 - Home 페이지는 메인 페이지 입니다.

router
    - home(페이지 제공)
    - logout(로그아웃)
    - get_my_session(사용자가 속한 세션 가져오기)
    - create_session_at_home(세션 만들기)

작성자 : 조해천
"""

from flask import Blueprint, request, render_template, jsonify

import web.app.models.user_services as user_services
import web.app.models.session_read_services as session_read_services
import web.app.models.session_write_services as session_write_services

home_bp = Blueprint("home", __name__)
logout_bp = Blueprint("logout", __name__, url_prefix="/api/user")
get_my_session_bp = Blueprint("get_session", __name__, url_prefix="/api/user")
create_session_at_home_bp = Blueprint("create_session_home", __name__, url_prefix="/api/session")


@home_bp.route("/home", methods=["GET"])
def home():
    """
    메인 페이지를 반환하는 API입니다.

    Request:
        Path: "/home" (GET)
        Cookies:
            - user_name (str): 사용자 이름
            - user_key (str): 사용자 인증 키

    Response:
        HTML:
            - home.html
            Template Variables:
                - name (str): 사용자 이름
                - list (dict): {"question": int, "answer": int, "saving": int}
    """
    cookie = request.cookies

    content = {
        "name": "server test",
        "list": {"question": 1, "answer": 2, "saving": 3},
    }
    count = user_services.question_count(cookie.get("user_key"))
    name = cookie.get("user_name")

    content["list"]["question"] = count
    content["name"] = name

    return render_template("home.html", **content)


@logout_bp.route("/logout", methods=["POST"])
def logout():
    """
    로그아웃을 처리하는 API입니다.

    Request:
        Path:  /api/user/logout
        Cookies:
            - user_key (str): 사용자 인증 키
            - user_name (str): 사용자 이름

    Response:
        Body (JSON):
            - logout_result (bool): True(성공) | False(실패)
            - logout_message (str): 처리 메시지
    """
    pass
    # TODO: 쿠키처리
    return jsonify(
        {"logout_result": True, "logout_message": "로그아웃에 성공했습니다."}
    )


@get_my_session_bp.route("/get/my_sessions", methods=["GET"])
def get_my_session():
    """
    현재 사용자가 포함된 세션 목록을 가져오는 API입니다.

    Request:
        Path: "/api/user/get/my_sessions" (GET)
        Cookies:
            - user_key (str): 사용자 인증 키

    Query Params:
        - start (int): 시작 인덱스
        - count (int): 가져올 세션 개수

    Response:
        JSON (List):
            - session_title (str)
            - session_description (str)
            - session_code (str)
            - activated_user_count (int)
            - create_at (str | datetime)
    """
    data = request.get_json()
    cookie = request.cookies

    session_read_services.get_session_list(cookie.get("user_key"), data.get("start"), data.get("count"))


@create_session_at_home_bp.route("create/home", methods=["POST"])
def create_session_home():
    """
    Home 페이지에서 세션을 생성할 때 호출되는 API입니다.

    Request:
        Path: "/api/session/create/home" (POST)
        Cookies:
            - user_key (str): 사용자 인증 키
        Body(JSON):
            - title (str): 세션 제목
            - description (str): 세션 설명
            - pw (str): 세션 비밀번호
            - temporary (bool): 임시 세션 여부

    Response:
        JSON:
            - session_result (bool): True(성공) | False(실패)
            - session_create_message (str): 처리 메시지
            - session_code (str | None): 생성된 세션 코드
    """
    data = request.get_json()
    cookie = request.cookies

    session = session_write_services.create_session(
        cookie.get("user_key"),
        data.get("title"),
        data.get("description"),
        data.get("pw"),
        data.get("temporary"),
    )

    if session == False:
        session_create_message = "세션 생성에 실패했습니다."
        return jsonify(
            {
                "session_result": False,
                "session_create_message": session_create_message,
                "session_code": None,
            }
        )
    else:
        session_create_message = "세션 생성에 성공했습니다."
        return jsonify(
            {
                "session_result": True,
                "session_create_message": session_create_message,
                "session_code": session,
            }
        )
