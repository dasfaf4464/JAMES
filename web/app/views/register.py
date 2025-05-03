from flask import Blueprint, render_template

register_bp = Blueprint('register', __name__)

content = {}

@register_bp.route('/register', methods=["GET", "POST"])
def register():

    return render_template('register.html', **content)

'''
    회원 가입시 이름 선택
    인증 번호 발송
'''