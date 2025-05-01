"""
세션을 관리하는 클래스입니다.
"""

from flask_socketio import SocketIO, emit

class ChatManager:
    sessioncode = None
    user = dict
    admin = None
    isOpen = False
    isExpired = False

    def __init__(self, sessioncode, admin_uuid, admin_name):
        self.sessioncode = sessioncode
        self.admin = admin_uuid
        self.user.update(admin_uuid, admin_name)

    def join_new_user(self, uuid:str, name:str):
        self.user[uuid] = name

    def change_admin(self, uuid:str):
        self.admin = uuid