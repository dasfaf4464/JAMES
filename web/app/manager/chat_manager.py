"""
세션을 관리하는 클래스입니다.
"""

from flask_socketio import SocketIO, emit, rooms
from app.util.naming import create_server_code
from datetime import datetime, timedelta, timezone

active_sessions = dict()


class ChatManager:
    def __init__(self, sessioncode, admin_key):
        self.sessioncode = sessioncode
        self.session_name = None
        self.room = None
        self.admin_key = admin_key
        self.isTemporary = True
        self.isOpen = False
        self.password = None
        self.start_time = datetime.now(timezone.utc)

    def isActivated(session_code):
        return session_code in active_sessions

    def create_room(self, admin_key):
        new_session_code = create_server_code()
        while new_session_code in active_sessions:
            new_session_code = create_server_code()

        new_session = ChatManager(new_session_code, admin_key)
        active_sessions.update(new_session_code, new_session)

    def change_admin(self, new_admin_key):
        self.admin_key = new_admin_key

    def update_options(self, name, temporary: bool, open: bool, password):
        self.session_name = name
        self.isTemporary = temporary
        self.isOpen = open
        self.password = password
