from flask import Blueprint, render_template

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=["GET", "POST"])
def register():

    return render_template('register.html')

'''
    회원 가입시 이름 선택
    인증 번호 발송
'''