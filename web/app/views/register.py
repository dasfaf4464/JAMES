from flask import Blueprint, render_template, request, jsonify

register_bp = Blueprint('register', __name__)
signup_bp = Blueprint('signup', __name__)

@register_bp.route('/register', methods=["GET"])
def register():
    return render_template('register.html')

@signup_bp.route('/signup', methods=["POST"])
def signup():
    try:
        data = request.get_json()
        user_id = data.get('id')
        password = data.get('pw')
        email = data.get('email')
        name = data.get('name')

        # TODO: 여기에 DB 저장 로직 넣기 쿠키에 있는 임시키 포함해서
        # 예: mariadb_user_manager.put_sql("INSERT INTO userinfo (id, pw, email, name) VALUES (%s, %s, %s, %s)", (user_id, password, email, name))

        return jsonify({"success": True, "message": "회원가입 성공!"})

    except Exception as e:
        return jsonify({"success": False, "message": "회원가입 실패: " + str(e)}), 500
