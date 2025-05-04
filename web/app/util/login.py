from flask import Blueprint, request, jsonify, url_for, make_response
from app.manager.db_manager import mariadb_user_manager

login_bp = Blueprint('login', __name__)

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
