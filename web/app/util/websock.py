from flask import request
from flask_socketio import SocketIO, join_room, leave_room, emit

@SocketIO.on(message='connect', namespace=None)
def handle_connect(data):
    session_code = data['sessioncode']
    join_room(session_code)
    emit('')
    print('client connected')