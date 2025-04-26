from flask import Blueprint, render_template

session_bp = Blueprint('session', __name__)

@session_bp.route('/session')
def session_error():
    return render_template('session.html')

@session_bp.route('/session/<sessioncode>')##정규식 포함 예정
def session():
    return render_template('session.html')