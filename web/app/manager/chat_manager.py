"""
세션을 관리하는 클래스입니다.
"""

from flask import jsonify
from flask_socketio import SocketIO, emit, rooms
from datetime import datetime, timedelta, timezone
from app.util.naming import create_server_code
from app.manager.db_manager import redis_manager

active_sessions = dict()

def isActivated(session_code: str):
    return session_code in active_sessions

class ChatManager:
    def __init__(self, sessioncode: str, admin_key:str, temporary:bool, open: bool):
        self.user = list()
        self.sessioncode = sessioncode
        self.session_name = None
        self.room = None
        self.admin_key = admin_key
        self.isTemporary = True
        self.isOpen = open
        self.password = None
        self.start_time = datetime.now(timezone.utc)

    def create_room(self, admin_key, temporary: bool, open: bool):
        new_session_code = create_server_code()
        while new_session_code in active_sessions:
            new_session_code = create_server_code()

        new_session = ChatManager(new_session_code, admin_key, temporary)
        new_session.user.append(admin_key)
        active_sessions.update({new_session_code:new_session})

    def get_text_fromuser(user_key ,text: str, category: dict):
        redis_manager.push_dict_to_list("user_text", {user_key:text})

    def push_text_touser(user_key, text_set: set):
        return

    def change_admin(self, new_admin_key):
        self.admin_key = new_admin_key

    def update_options(self, name, temporary: bool, open: bool, password):
        self.session_name = name
        self.isTemporary = temporary
        self.isOpen = open
        self.password = password