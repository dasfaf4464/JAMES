"""
사용자가 입력한 채팅 데이터를 관리하고 사용자 정보, 세션 정보를 관리합니다.
"""

import app.util.db as db
import atexit
import json


class RedisManager:
    def __init__(self, redis_db_num):
        self.redis_client = db.get_redis_connection(redis_db_num)
        atexit.register(self.disconnect)

    def disconnect(self):
        db.disconnect_redis(self.redis_client)
        self.redis_client = None

    def push_dict_to_list(self, name :str, data: dict):
        seriealize_data = json.dumps(data)
        try:
            self.redis_client.lpush(name, seriealize_data)
        except Exception as e:
            print(e)

class MariadbManager:
    def __init__(self, id, pw):
        self.account = db.get_mariadb_connection(id, pw)
        atexit.register(self.disconnect)

    def put_sql(self, SQL: str, params: tuple):
        if self.account is not None:
            return db.put_sql(self.account, SQL, params)
        else:
            print("연결된 db가 없습니다.")

    def put_sql_result(self, SQL: str, params: tuple):
        if self.account is not None:
            return db.get_result(self.account, SQL, params)
        else:
            print("연결된 db가 없습니다.")

    def disconnect(self):
        db.disconnection_mariadb(self.account)


mariadb_admin_manager = MariadbManager(db.DB_ADMIN.get("id"), db.DB_ADMIN.get("pw"))
mariadb_user_manager = MariadbManager(db.DB_USER.get("id"), db.DB_USER.get("pw"))
redis_manager = RedisManager(0)