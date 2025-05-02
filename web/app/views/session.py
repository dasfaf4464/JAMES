from flask import Blueprint, render_template
from app.util import check_server_code_format
from flask_socketio import SocketIO

session_bp = Blueprint('session', __name__)

@session_bp.route('/session/<sessioncode>')
def session(sessioncode):
    if not sessioncode:
        return render_template('session.html', error = True) #잘못된 세션 주소
    elif sessioncode:
        if not check_server_code_format(sessioncode):
            return render_template('session.html', error = True)
        '''
        elif session is not existed in DB:
            return reder_template('session.html', error = True)
        else:
            return reder_template('session.html', error= False)
        '''
