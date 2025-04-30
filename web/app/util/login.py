from flask import Blueprint, request, jsonify, url_for

login_bp = Blueprint('login', __name__)

mock = {"user":"1234"}

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in mock and mock[username] == password:
        return jsonify(success=True, redirect_url=url_for('home.home'))
    return jsonify(success=False, message="Login failed"), 401

'''
아이디 이메일형식 정규식 검사, 비밀번호 정규식 검사
db에서 연동
'''