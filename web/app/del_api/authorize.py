"""
회원 관리 api를 관리하는 모듈입니다.
키 확인과 생성, 로그인, 회원가입-이름생성, 회원가입
"""

from flask import (
    Blueprint,
    request,
    jsonify,
    url_for,
    make_response,
    Response,
    redirect,
)
from app.util.db_manager import mariadb_user_manager, mariadb_admin_manager
from datetime import datetime, timedelta, timezone
import random
import string

userChecking_bp = Blueprint("check_key", __name__, url_prefix="/auth")
login_bp = Blueprint("login", __name__, url_prefix="/auth")
logout_bp = Blueprint("logout", __name__, url_prefix="/auth")
makename_bp = Blueprint("make_name", __name__, url_prefix="/auth")
signup_bp = Blueprint("signup", __name__, url_prefix="/auth")

NAME_ADJ = [
    "Curious", "Wise", "Smart","Kind","Friendly","Clever","Thoughtful","Cheerful","Bright",
    "Honest","Logical","Noble","Insightful","Creative","Calm","Gentle","Patient","Witty","Brilliant",
    "Reliable","Helpful","Eloquent","Focused","Polite","Rational"
]

NAME_NOUN = [
    "Lantern","Library","Notebook","Compass","Quill","Clock","Mirror","Tablet","Candle","Vessel",
    "Scroll","Key","Circuit","Anchor","Helmet","Feather","Stone","Book","Map","Bridge",
    "Tower","Coin","Globe","Ink","Signal",
]

def create_user_key():
    charset = list(string.ascii_lowercase)
    return "".join(random.sample(charset, 12))


def create_user_name():
    adj = random.choice(NAME_ADJ)
    noun = random.choice(NAME_NOUN)
    return f"{adj} {noun}"


@userChecking_bp.before_app_request
def handle_user_redirection():
    """
    로그인 여부 및 임시 사용자 상태에 따라 리디렉션을 처리합니다.
    - 로그인한 사용자가 '/'로 접근하려 할 때 /home으로 리디렉션
    - 로그인하지 않은 사용자(임시 사용자)가 /home, /history 으로 접근하려 할 때 /로 리디렉션
    """
    client_cookie = request.cookies
    is_temporary = client_cookie.get("is_temporary")

    if is_temporary == "True":
        if request.path == "/home" or request.path == '/history':
            return redirect(url_for("index.index"))
    elif is_temporary == "False":
        if request.path == "/":
            return redirect(url_for("home.home"))
    return None


@userChecking_bp.route("/check_key")
def check_tempkey():
    MAXAGE = 10800
    """
    모든 페이지에 접근시 처음으로 요청받는 api입니다.
    클라이언트 쿠키를 확인하여 사용자 등록이 되었는지 검사합니다.
    클라이언트가 사용자 등록이 되어있는 상태라면 사용자 인증의 만료시간을 연장합니다.
    만약 클라이언트가 로그인 되지 않았다면 인덱스 페이지로 이동하게 합니다.
    
    Require Cookies: 
        user_key (str): 저장된 사용자 키

    Response Cookies:
        *변경이 필요한 경우
        *user_name (str): 사용자 이름
        *user_key (str): 사용자 키
        *is_temporary (boolean): 임시 사용자와 회원 구분

    Response:
        message (str): 서버 처리 메세지
        redirect_url (url): 허가받지 않은 경로로 진입시 돌아가야할 주소 제공 
    """
    client_cookie = request.cookies
    user_key = client_cookie.get("user_key")
    is_temporary = client_cookie.get("is_temporary")
    user_name = client_cookie.get("user_name")
    response_data = {"message": "", "redirect_url": ""}

    if not user_key:  # 쿠키가 없으면 임시유저로 처리
        response_data["message"] = "임시유저 키 발급 성공"
        response_data["redirect_url"] = "/"  # 로그인이 되어있지 않으면 홈으로 리디렉션
        response = make_response(jsonify(response_data))

        response.set_cookie(
            "user_key",
            value=create_user_key(),
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "is_temporary",
            value="True",
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "user_name",
            value=create_user_name(),
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response

    elif is_temporary == "True":
        response_data["message"] = "임시유저 시간 갱신 성공"
        response = make_response(jsonify(response_data))

        response.set_cookie(
            "user_key",
            value=user_key,
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "is_temporary",
            value=is_temporary,
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "user_name",
            value=user_name,
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response

    else:  # 로그인한 유저의 경우
        response_data["message"] = "회원 시간 갱신 성공"
        response = make_response(jsonify(response_data))

        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        response.set_cookie(
            "user_key",
            value=user_key,
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "is_temporary",
            value=is_temporary,
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "user_name",
            value=user_name,
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response


@login_bp.route("/login", methods=["POST"])
def login():
    """
    index 페이지에서 로그인시 인증하는 api입니다.
    클라이언트 쿠키를 사용자 정보로 변경합니다.
    클라이언트 키는 redis에 저장됩니다.

    Request:
        id (str): 사용자 아이디
        pw (str): 사용자 비밀번호

    Response Cookies:
        user_name (str): 사용자 이름
        user_key (str): 사용자 키
        expire_time (str): 키 만료 시간
        is_temporary (boolean): False

    Response:
        message (str): 로그인 처리 메세지
        redirect_url: 로그인 성공시 홈, 아닌경우 인덱스 페이지 주소 제공
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    response_data = {
        "isSuccess": False,
        "redirect_url": "",
        "message": "로그인에 실패하였습니다.",
    }

    try:
        sql_query = "SELECT id, pw, user_name, user_key FROM userinfo WHERE id = %s"
        in_db_list = mariadb_user_manager.put_sql_result(sql_query, (username,))

        if not in_db_list:
            response_data["message"] = "존재하지 않는 ID 입니다."
            response = make_response(jsonify(response_data))
            return response

        user = in_db_list[0]

        if user["pw"] != password:
            response_data["message"] = "비밀번호가 잘못되었습니다."
            response = make_response(jsonify(response_data))
            return response

        response_data["isSuccess"] = True
        response_data["message"] = "로그인에 성공했습니다."
        response_data["redirect_url"] = url_for("home.home")
        response = make_response(jsonify(response_data))

        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        response.set_cookie(
            "user_key",
            user["user_key"],
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "user_name",
            user["user_name"],
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            "is_temporary",
            "False",
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response

    except Exception as e:
        response = make_response(jsonify(response_data))
        return response, 500


@logout_bp.route("/logout", methods=["POST"])
def logout():
    """
    사용자 메뉴에서 로그아웃하는 api입니다.
    로그아웃시 redis에 있는 사용자 정보를 삭제합니다.
    클라이언트 쿠키를 초기화합니다.

    Require Cookies:
        user_key (str): 로그아웃할 사용자 키를 가져옵니다.

    Response Cookies:
        user_name (str): None
        user_key (str): None
        expire_time (str): None
        is_temporary (boolean): None

    Response:
        message (str): 로그아웃 처리 메세지
        redirect_url (url): index 페이지 주소
    """
    response = make_response()
    
    response_data = {"isSuccess":"", "message":"", "redirect_url":""}
    try:
        response_data["isSuccess"] = True
        response_data["message"] = "로그아웃"
        response_data["redirect_url"] = url_for('index.index')
        response = make_response(jsonify(response_data))
        
        response.delete_cookie("user_key")
        response.delete_cookie("is_temporary")
        response.delete_cookie("user_name")
        return response
    except Exception as e:
        return make_response(jsonify({"message":"로그아웃 실패"})), e


@makename_bp.route("/generate_name", methods=["GET"])
def generate_name():
    """
    회원가입 페이지에서 이름을 생성하는 api입니다.
    서버에서 생성된 이름(str)을 반환합니다.

    Response:
        name (str): 생성된 이름
    """
    generated_name = create_user_name()
    return Response(generated_name, mimetype="text/plain")


@signup_bp.route("/signup", methods=["POST"])
def signup():
    """
    회원가입 페이지에서 주어진 정보로 회원가입하는 api입니다.
    입력된 아이디가 중복인지 검사후 메세지로 안내합니다.
    아이디와 비밀번호는 영문으로 20글자까지 입력 가능합니다.

    Request:
        id (str): 사용자가 사용할 아이디
        pw (str): 사용자가 사용할 비밀번호
        email (str): 사용자 인증에 사용할 이메일
        name (str): 사용자가 사용할 이름

    Require Cookies:
        user_key (str): 임시 발급된 키

    Response:
        message (str): 회원가입 처리 메세지
        isSuccess (boolean): 회원가입 성공 유무
        redirect_url (url): 회원가입 성공시 인덱스 주소
    """
    response = make_response()

    try:
        response_data = {"isSuccess": False, "message": "", "redirect_url": ""}
        data = request.get_json()
        user_key = request.cookies.get("user_key")
        user_data = {
            "user_name": data.get("name", ""),
            "id": data.get("id", ""),
            "pw": data.get("pw", ""),
            "email": data.get("email", ""),
            "user_key": user_key,
        }

        sql_query = "SELECT id, user_key FROM userinfo WHERE id = %s OR user_key = %s"
        result = mariadb_user_manager.put_sql_result(
            sql_query, (user_data["id"], user_data["user_key"])
        )

        if result and len(result) > 0:
            for row in result:
                if row[0] == user_data["id"]:
                    response_data["message"] = "이미 존재하는 사용자 ID입니다."
                    response_data["isSuccess"] = False
                    response = make_response(jsonify(response_data))
                    return response
                if row[1] == user_data["user_key"]:
                    print(row[1])
                    response_data["message"] = "이미 사용 중인 사용자 키입니다."
                    response_data["isSuccess"] = False
                    response = make_response(jsonify(response_data))
                    return response
        else:
            columns = ", ".join(user_data.keys())
            placeholders = ", ".join(["%s"] * len(user_data))
            values = tuple(user_data.values())

            sql_query = f"INSERT INTO userinfo ({columns}) VALUES ({placeholders})"
            if mariadb_admin_manager.put_sql(sql_query, values):
                response_data["isSuccess"] = True
                response_data["message"] = "회원가입 성공"
                response_data["redirect_url"] = "/"
                response = make_response(jsonify(response_data))

                response.delete_cookie("user_key", path="/")
                response.delete_cookie("is_temporary", path="/")
                response.delete_cookie("user_name", path="/")
                return response
            else:
                response_data["isSuccess"] = False
                response_data["message"] = "DB오류, 회원가입 실패"
                response = make_response(jsonify(response_data))
                return response

    except Exception as e:
        return jsonify({"isSuccess": False, "message": "회원가입 실패"}), 500
