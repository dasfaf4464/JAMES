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
        #웹소켓 여기서 연결
    
    def user_leave(self, user_key):
        self.user.pop(user_key)
        


"""
redis에 저장할 때 병렬적으로 요청을 받아 redis 서버를 호출하는것보다 버퍼로 세션데이터를 모아서 한번에 넘기는게 좋다.
이 때 세션 데이터는 클라이언트 본인만 제어할 수 있는 권한이 있지만 추가와 삭제가 동시에 일어날 때 데이터 정합성이 깨질 수 있는 경우가 발생한다.

카테고리 선택시 redis에 전부 담아놓으면 세션개수*세션당 입력된 글 개수로 메모리 초과 가능성 발생 (입력된 글 정보가 0.1mb라 잡았을 때 1000개의 세션 * 100개의 글이라 하면 gb단위)
기존의 데이터를 mariadb와 redis에 섞어서 저장하면 속도차이 발생및 mariadb 디스크io 여러번 발생
한 명이 나왔다 들어갔다를 계속하면 요청 지속적으로 발생(비정상적 사용)

==>> 그래서
redis는 세션의 카테고리 개수와 카테고리당 최신글만 mariadb에서 가져옴
사용자가 카테고리 선택시 웹소켓으로 redis에 있는 카테고리의 내용을 보냄, 이후 카테고리의 게시글을 더 요청시 mariadb에서 가져옴 (혹은 미리 가져와도 됨)
사용자가 게시글 입력시 redis에서 카테고리/해당 카테고리의 최신글 업데이트 + mariadb에 저장 -> 웹소켓으로 현재 해당 카테고리에 접속한 사람에게 전달
사용자가 게시글 삭제시 redis에 있으면 redis와 mariadb에 삭제, redis에 없으면 mariadb에서만 삭제
삭제와 입력이 동시에 발생하면 데이터 정합성 깨질 위험, 충돌 발생!!
db io(redis, mariadb) 너무 많이 발생 가능 ,사용자 입력을 버퍼로 전달??

파일 구조 지금 변경해도 되나? HTTP API (페이지 제공, 기능 제공 통합/JS 기능별로 할지 도메인별로 할지/ util 내용을 manager로 통합)

DB정규화 어디까지? websocket에서 연결을 끊지 말고 이벤트이름으로 해당 내용 요청(이벤트를 동적으로 생성 가능?)?
"""
