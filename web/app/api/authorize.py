"""
회원 관리 api를 관리하는 모듈입니다.
키 확인과 생성, 로그인, 회원가입-이름생성, 회원가입
"""
from flask import Blueprint, request, jsonify, url_for, make_response
from app.util.naming import create_user_name
from app.manager.db_manager import mariadb_user_manager

userChecking_bp = Blueprint('check_key', __name__, url_prefix='/auth')
login_bp = Blueprint('login', __name__, url_prefix='/auth')
logout_bp = Blueprint('logout', __name__, url_prefix='/auth')
makename_bp = Blueprint('make_name', __name__, url_prefix='/auth')
signup_bp = Blueprint('signup', __name__, url_prefix='/auth')

@userChecking_bp.route('/check_key')
def check_tempkey():
    """
    모든 페이지에 접근시 처음으로 요청받는 api입니다.
    클라이언트 쿠키를 확인하여 사용자 등록이 되었는지 검사합니다.
    클라이언트가 사용자 등록이 되어있는 상태라면 사용자 인증의 만료시간을 연장합니다.
    만약 클라이언트가 로그인 되지 않았다면 인덱스 페이지로 이동하게 합니다.
    
    Require Cookies: 
        user_key (str): 저장된 사용자 키
        expire_time (str): 키 만료 시간

    Response Cookies:
        *변경이 필요한 경우
        *user_name (str): 사용자 이름
        *user_key (str): 사용자 키
        expire_time (str): 키 만료 시간
        *is_temporary (boolean): 임시 사용자와 회원 구분

    Response:
        message (str): 서버 처리 메세지
        redirect_url (url): 허가받지 않은 경로로 진입시 돌아가야할 주소 제공 
    """
    user_cookie = {
        "user_key":""
    }
    
    client_cookie = request.cookies
    if not client_cookie.get("user_key"):
        return

@login_bp.route('/login', methods=['POST'])
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
    username = data.get('username')
    password = data.get('password')
    return_data = {
        'success': 'False',
        'redirect_url': '',
        'message': '로그인에 실패하였습니다.'
    }

    sql_query = "SELECT id, pw, random_key FROM userinfo WHERE id = %s"
    in_db_list = mariadb_user_manager.put_sql_result(sql_query, (username,))

    if not in_db_list:
        return jsonify(return_data)

    in_db = in_db_list[0]

    if in_db.get('pw') == password:
        return_data['success'] = 'True'
        return_data['redirect_url'] = url_for('home.home')
        return_data['message'] = '로그인에 성공하였습니다.'
        return jsonify(return_data)

    return jsonify(return_data), 401

@logout_bp.route('/logout')
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
    return

@makename_bp.route('/generate_name', methods=['GET'])
def generate_name():
    """
    회원가입 페이지에서 이름을 생성하는 api입니다.
    서버에서 생성된 이름(str)을 반환합니다.

    Response:
        name (str): 생성된 이름
    """
    generated_name = create_user_name()
    return jsonify({'name': generated_name})

@signup_bp.route('/signup', methods=["POST"])
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
    try:
        data = request.get_json()
        user_id = data.get('id')
        password = data.get('pw')
        email = data.get('email')
        name = data.get('name')
        user_key = request.cookies.get("user_key")
        
        # TODO: 여기에 DB 저장 로직 넣기 쿠키에 있는 임시키 포함해서
        # 예: mariadb_user_manager.put_sql("INSERT INTO userinfo (id, pw, email, name) VALUES (%s, %s, %s, %s)", (user_id, password, email, name))

        return jsonify({"success": True, "message": "회원가입 성공!"})

    except Exception as e:
        return jsonify({"success": False, "message": "회원가입 실패: " + str(e)}), 500
