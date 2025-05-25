"""
세션을 관리하는 클래스입니다.
"""

from flask import jsonify
from flask_socketio import SocketIO, emit, rooms
from datetime import datetime, timedelta, timezone
import random, string
from app.manager.db_manager import redis_manager

active_sessions = dict()


def isActivated(session_code: str):
    return session_code in active_sessions


class ChatManager:
    def __init__(
        self,
        sessioncode: str,
        admin_key: str,
        title: str,
        description: str,
        is_temporary: bool,
    ):
        self.user = list()
        self.sessioncode = sessioncode
        self.session_name = title
        self.description = description
        self.admin_key = admin_key
        self.isTemporary = is_temporary
        self.start_time = datetime.now(timezone.utc)

    def create_room(admin_key: str, title: str, description: str, is_temporary: bool):
        new_session_code = ChatManager.create_server_code()
        while new_session_code in active_sessions:
            new_session_code = ChatManager.create_server_code()

        new_session = ChatManager(
            sessioncode=new_session_code,
            admin_key=admin_key,
            title=title,
            description=description,
            is_temporary=is_temporary,
        )
        new_session.user.append(admin_key)
        active_sessions.update({new_session_code: new_session})
        return new_session_code

    def change_admin(self, new_admin_key):
        self.admin_key = new_admin_key

    def update_options(self, name, temporary: bool, open: bool, password):
        self.session_name = name
        self.isTemporary = temporary
        self.isOpen = open
        self.password = password

    def create_server_code():
        charset = string.ascii_uppercase + string.digits
        parts = ["".join(random.choices(charset, k=4)) for _ in range(3)]
        return "-".join(parts)

    def user_join(self, user_key):
        self.user.append(user_key)
        # 웹소켓 여기서 연결

    def user_leave(self, user_key):
        self.user.pop(user_key)
