"""
세션을 관리하는 클래스입니다.
"""

from flask_socketio import SocketIO, emit
from datetime import datetime, timedelta

active_sessions = dict()
class ChatManager:
    def __init__(self, sessioncode, session_name, admin_uuid, admin_name, temporary, isOpen):
        self.sessioncode = sessioncode
        self.session_name = session_name
        self.user = dict
        self.admin = admin_uuid
        self.user.update(admin_uuid, admin_name)
        self.temporary = temporary
        self.isOpen = isOpen
        self.start_time = None
        self.end_time = None

    def join_new_user(self, uuid:str, name:str):
        self.user[uuid] = name

    def change_admin(self, uuid:str):
        self.admin = uuid