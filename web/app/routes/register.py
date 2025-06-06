"""
[Register 페이지]
Register 페이지 - Register 페이지는 회원가입 할 수 있는 페이지 입니다.

router
    - register(페이지 제공)
    - name(이름 생성)
    - sign_up(회원가입)

작성자 : 조해천
"""

from flask import Blueprint, render_template, request, jsonify
import app.models.user_services as user_services

register_bp = Blueprint("register", __name__)
create_name_bp = Blueprint("create_name", __name__, url_prefix="/api/user")
sign_up_bp = Blueprint("sign_up", __name__, url_prefix="/api/user")


@register_bp.route("/register", methods=["GET"])#checked
def register():
    """
    회원가입 페이지를 반환합니다.

    Request:
        Path: "/register" (GET)

    Response:
        HTML:
            - register.html
    """
    return render_template("register.html")


@create_name_bp.route("/name", methods=["GET"])#checked
def create_name():
    """
    무작위로 생성된 이름을 반환하는 API입니다.

    Request:
        Path: "/api/user/name" (GET)

    Response:
        JSON:
            - name (str): 생성된 이름
    """
    name_result = user_services.create_name()
    return jsonify({"name": name_result})


@sign_up_bp.route("/signup", methods=["POST"])#checked
def sign_up():
    """
    회원가입 요청을 받는 API입니다.

    Request:
        Path: "/api/user/signup" (POST)
        Body (JSON):
            - id (str): 사용자 id
            - pw (str): 사용자 pw
            - name (str): 사용자 이름
            - email (str): 사용자 이메일
        Cookies:
            - user_key (str): 사용자 인증 키

    Response:
        JSON:
            - register_result (bool): 회원가입 성공 여부 (True/False)
            - register_message (str): 회원가입 성공 또는 실패 사유 메시지
    """
    data = request.get_json()
    cookie = request.cookies

    register = user_services.register(
        data.get("id"),
        data.get("pw"),
        data.get("name"),
        data.get("email"),
        cookie.get("user_key"),
        temporary=False
    )

    if register == "ok":
        register_message = "회원가입에 성공했습니다."
        return jsonify({"register_result": True, "register_message": register_message})
    elif register == "id":
        register_message = "중복된 아이디입니다."
        return jsonify({"register_result": False, "register_message": register_message})
    else:
        register_message = "비밀번호가 형식에 맞지 않습니다."
        return jsonify({"register_result": False, "register_message": register_message})
