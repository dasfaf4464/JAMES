"""
[Index 페이지]
Index 페이지 - index 페이지는 사용자가 처음 접근 했을 때 만나는 플랫폼 페이지입니다.

router
    - index(페이지 제공)
    - login(로그인)
    - create_session_at_index(세션 만들기)

작성자 - 조해천
"""

from flask import Blueprint, request, render_template, jsonify

import app.models.user_services as user_services
import app.models.session_write_services as session_write_services

from datetime import datetime, timezone, timedelta

index_bp = Blueprint("index", __name__)
login_bp = Blueprint("login", __name__, url_prefix="/api/user")
create_session_at_index_bp = Blueprint("create_session_index", __name__, url_prefix="/api/session")


@index_bp.route("/", methods=["GET"])#checked
def index():
    """
    인덱스 페이지를 반환합니다.

    Request:
        Path: "/" (GET)

    Response:
        HTML:
            - index.html
    """
    return render_template("index.html")


@login_bp.route("/login", methods=["POST"])#checked
def login():
    """
    로그인 api입니다.

    Request:
        Path: "/api/user/login" (POST)
        Body (JSON):
            - id (str): 사용자 아이디
            - pw (str): 사용자 비밀번호

    Response:
        JSON:
            - login_result (bool): 로그인 성공 여부 (True/False)
            - login_message (str): 로그인 성공 또는 실패 사유 메시지
        Cookies:
            - user_key (str): 사용자 고유 키
            - user_name (str): 사용자 이름
            - expire_time (str): 쿠키 만료 시간
    """
    data = request.get_json()

    login_result = user_services.login(data.get("id"), data.get("pw"))

    if login_result == "id":
        login_message = "존재하지 않는 아이디입니다."
        return jsonify({"login_result": False, "login_message": login_message})
    elif login_result == "pw":
        login_message = "비밀번호가 틀렸습니다."
        return jsonify({"login_result": False, "login_message": login_message})
    else:
        login_message = "로그인에 성공했습니다."
        response = jsonify({"login_result": True, "login_message": login_message})
        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        response.set_cookie(
            "user_key",
            login_result.get("user_key"),
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "user_name",
            login_result.get("user_name"),
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "temporary",
            "False",
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response


@create_session_at_index_bp.route("/create/index", methods=["POST"])
def create_session_index():
    """
    Index 페이지에서 세션을 만들 때 호출되는 API입니다.
    Index 페이지는 비회원이므로 영구적으로 생성하지 않습니다.

    Request:
        Path: "/api/session/create/index" (POST)
        JSON Body:
            - title (str): 세션 제목
            - description (str): 세션 설명
            - pw (str): 세션 비밀번호
        Cookies:
            - user_key (str): 사용자 인증 키

    Response:
        JSON:
            - session_result (bool): 세션 생성 성공 여부
            - session_create_message (str): 세션 생성 성공/실패 메시지
            - session_code (str or None): 생성된 세션 코드 또는 None
    """
    data = request.get_json()
    cookie = request.cookies

    session = session_write_services.create_session(
        cookie.get("user_key"),
        data.get("title"),
        data.get("description"),
        data.get("pw"),
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
