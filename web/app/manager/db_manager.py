"""
사용자가 입력한 채팅 데이터를 관리하고 사용자 정보, 세션 정보를 관리합니다.
"""
import app.util.db as db
class RedisManager:
    def __init__(self, redis_db_num):
        self.redis = db.get_redis_connection(redis_db_num)

class MariadbManager:
    def __init__(self, admin):
        self.admin = admin