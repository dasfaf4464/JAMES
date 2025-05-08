"""
회원 관리 api
로그인, 회원가입-이름생성, 임시키-발급, 회원가입
"""
from flask import Blueprint, request, jsonify, url_for, make_response
from app.util.naming import create_user_name
from app.manager.db_manager import mariadb_user_manager

login_bp = Blueprint('login', __name__, url_prefix='/auth')
makename_bp = Blueprint('make_name', __name__, url_prefix='/auth')
tempkey_bp = Blueprint('check-key', __name__, url_prefix='/auth')
signup_bp = Blueprint('signup', __name__, url_prefix='/auth')

@login_bp.route('/login', methods=['POST'])
def login():
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


@makename_bp.route('/generate-name', methods=['GET'])
def generate_name():
    generated_name = create_user_name()
    return jsonify({'name': generated_name})

@tempkey_bp.route('/check-key')
def check_tempkey():
    user_cookie = {
        "user_key":""
    }
    
    client_cookie = request.cookies
    if not client_cookie.get("user_key"):
        return 

@signup_bp.route('/signup', methods=["POST"])
def signup():
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
