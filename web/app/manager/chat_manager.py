"""
세션을 관리하는 클래스입니다.
"""

from flask import jsonify
from flask_socketio import SocketIO, emit, rooms
from datetime import datetime, timedelta, timezone
import random, string
from app.manager.db_manager import (
    redis_manager,
    mariadb_admin_manager,
    mariadb_user_manager,
)

"""
redis | session:<session_code> = set{user}
"""


class ChatManager:
    def __init__(
        self,
        sessioncode: str,
        title: str,
        description: str,
        is_temporary: bool,
    ):
        self.user = set()
        self.sessioncode = sessioncode
        self.session_name = title
        self.description = description
        self.isTemporary = is_temporary
        self.start_time = datetime.now(timezone.utc)

    @staticmethod
    def create_room(admin_key: str, title: str, description: str, is_temporary: bool):
        """
        세션을 만들고 Mariadb에 저장합니다.
        """
        import pymysql

        max_retry = 5
        for _ in range(max_retry):
            new_session_code = ChatManager._create_server_code()
            try:
                if mariadb_admin_manager.insert(
                    "sessioninfo",
                    {
                        "name": title,
                        "description": description,
                        "session_key": new_session_code,
                        "host": admin_key,
                        "is_temporary": is_temporary,
                    },
                ):
                    print("session create successfully ", new_session_code)
                    return new_session_code
            except pymysql.err.IntegrityError:
                # 중복 세션 코드가 존재하면 재시도
                continue

        print("session creation failed after retries")
        return False

    @staticmethod
    def user_join(session_code: str, user_key: str):
        session = mariadb_user_manager.select(
            "sessioninfo", {"session_key": session_code}
        )

        if not session:  # 세션이 생성되지 않은 경우
            return False

        with redis_manager.redis_client.lock(
            f"lock:session:{session_code}", blocking_timeout=5
        ):
            if not redis_manager.redis_client.exists(
                f"session:{session_code}"
            ):  # 첫 사용자 입장
                redis_manager.put_set(f"session:{session_code}", [user_key])
                if session[0].get("is_temporary") == 1:
                    create_at = session[0].get("create_at")

                    KST = timezone(timedelta(hours=9))
                    create_at_kst = create_at.replace(tzinfo=KST)

                    expire = create_at_kst + timedelta(hours=3)
                    now_kst = datetime.now(KST)

                    time_left = expire - now_kst
                    remaining_seconds = int(time_left.total_seconds())
                    if remaining_seconds > 0:
                        redis_manager.redis_client.expire(
                            f"session:{session_code}", remaining_seconds
                        )
            else:  # 세션이 활성화 된 경우 (사용자 >= 1)
                redis_manager.put_set(f"session:{session_code}", [user_key])

        mariadb_admin_manager.insert("userinsession", {"user_key":user_key, "session_key": session_code})

        return True

    def user_leave(session_code:str, user_key: str):
        """
        유저가 세션에서 나가면 레디스에서 삭제합니다.
        """
        redis_manager.redis_client.srem(f"session:{session_code}", user_key)

    def change_admin(self, new_admin_key):
        self.admin_key = new_admin_key

    def update_options(self, name, temporary: bool, open: bool, password: str):
        self.session_name = name
        self.isTemporary = temporary
        self.isOpen = open
        self.password = password

    def _create_server_code():
        charset = string.ascii_uppercase + string.digits
        parts = ["".join(random.choices(charset, k=4)) for _ in range(3)]
        return "-".join(parts)
