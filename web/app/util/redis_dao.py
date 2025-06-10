"""
redis를 관리하는 클래스 입니다.
"""

from app.util.redis_clients import redisPool, RedisPooledConnection

class RedisDAO:
    def __init__(self, connection_pool: RedisPooledConnection):
        self.pool = connection_pool
        self.client = self.pool.get_client()
    
    def set_activated_session(self, session_code, user_key):
        try:
            self.client.sadd(f'session:{session_code}:users', user_key)
        except Exception as e:
            print(f"[ERROR] set_activated_session: {e}")

    def get_activated_users(self, session_code: str):
        try:
            return self.client.smembers(f"session:{session_code}:users")
        except Exception as e:
            print(f"[ERROR] get_activated_users: {e}")
            return set()
    
    def get_activated_users_count(self, session_code:str):
        try:
            return self.client.scard(f"session:{session_code}:users")
        except Exception as e:
            print(f"[ERROR] get_activated_users: {e}")
            return set()

    def remove_user_from_session(self, session_code: str, user_key: str):
        """
        Redis Set에서 유저 키를 제거합니다.
        """
        try:
            self.client.srem(f"session:{session_code}:users", user_key)
        except Exception as e:
            print(f"[ERROR] remove_user_from_session: {e}")

    def increment_category_count(self, session_code: str, category_key: str, count: int = 1):
        """
        특정 카테고리에 count만큼 누적합니다. (기본은 1 증가)
        """
        try:
            redis_key = f"session:{session_code}:categories"
            self.client.hincrby(redis_key, category_key, count)
        except Exception as e:
            print(f"[ERROR] increment_category_count: {e}")


    def increment_multiple_categories(self, session_code: str, category_dict: dict):
        """
        여러 개의 카테고리에 대해 값을 누적합니다.
        category_dict 예시: { "python": 2, "java": 3 }
        """
        try:
            redis_key = f"session:{session_code}:categories"
            for key, value in category_dict.items():
                self.client.hincrby(redis_key, key, value)
        except Exception as e:
            print(f"[ERROR] increment_multiple_categories: {e}")

    def remove_categories(self, session_code: str):
        try:
            redis_key = f"session:{session_code}:categories"
            self.client.delete(redis_key)
        except Exception as e:
            print(f"Error removing categories: {e}")

redis_DAO = RedisDAO(redisPool)
