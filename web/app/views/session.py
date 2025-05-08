from flask import Blueprint, render_template
from app.util import check_server_code_format
from flask_socketio import SocketIO

session_bp = Blueprint('session', __name__)

content = {'error':'True'}

@session_bp.route('/session/<sessioncode>')
def session(sessioncode):
    if not sessioncode:
        return render_template('session.html', **content) #세션 주소가 없을때
    elif sessioncode:
        if not check_server_code_format(sessioncode): #세션 포맷이 잘못되었을 때
            return render_template('session.html', **content)
        '''
        elif session is not existed in DB: #세션이 생성된 상태가 아닐때
            return reder_template('session.html', **content)
        else:
            return reder_template('session.html', **content)
        '''
