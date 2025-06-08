from flask import Blueprint, render_template, request, jsonify, make_response
import app.models.user_services as user_services

register_bp = Blueprint("register", __name__)
create_name_bp = Blueprint("create_name", __name__, url_prefix="/api/user")
sign_up_bp = Blueprint("sign_up", __name__, url_prefix="/api/user")


@register_bp.route("/register", methods=["GET"])
def register():
    """
    회원가입 페이지를 반환합니다.

    GET /register
    """
    return render_template("register.html")


@create_name_bp.route("/name", methods=["GET"])
def create_name():
    """
    무작위로 생성된 이름을 반환하는 API입니다.

    GET /api/user/name
    """
    name_result = user_services.create_name()
    return jsonify({"name": name_result})


@sign_up_bp.route("/signup", methods=["POST"])
def sign_up():
    """
    회원가입 요청 처리 API입니다.

    POST /api/user/signup
    - 요청 JSON 예: {"id": "...", "pw": "...", "email": "..."}
    - 기존 쿠키 user_key 기반 임시 유저를 정식 유저로 전환
    """
    data = request.get_json()

    user_key = request.cookies.get("user_key")
    if not user_key:
        return (
            jsonify(
                {
                    "register_result": False,
                    "register_message": "유저 키가 존재하지 않습니다.",
                }
            ),
            400,
        )

    user_id = data.get("id")
    pw = data.get("pw")
    email = data.get("email")

    # 정식 회원 등록
    register_result = user_services.register(
        user_id=user_id,
        user_key=user_key,
        pw=pw,
        email=email,
        temporary=False,
    )

    if register_result == "duplicate_id":
        return (
            jsonify(
                {
                    "register_result": False,
                    "register_message": "이미 존재하는 아이디입니다.",
                }
            ),
            409,
        )

    if register_result != "ok":
        return (
            jsonify(
                {
                    "register_result": False,
                    "register_message": "회원가입에 실패했습니다.",
                }
            ),
            500,
        )

    # 회원가입 성공 후, 새로운 임시 유저 생성
    new_user_name = user_services.create_name()
    new_user_key = user_services.create_key()
    temp_register_result = user_services.register(
        name=new_user_name,
        user_key=new_user_key,
        temporary=True,
    )

    if temp_register_result != "ok":
        # 임시 유저 생성 실패해도 기존 유저 가입 성공했으니 에러 처리 로깅만 하고 진행
        print("[WARN] 신규 임시 사용자 생성 실패")

    response = make_response(
        jsonify(
            {
                "register_result": True,
                "register_message": "회원가입에 성공했습니다.",
            }
        )
    )

    response.set_cookie("user_name", new_user_name, httponly=True)
    response.set_cookie("user_key", new_user_key, httponly=True)
    response.set_cookie("temporary", "True", httponly=True)

    return response
