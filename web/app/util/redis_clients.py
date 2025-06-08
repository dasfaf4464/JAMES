import redis
from redis.exceptions import ConnectionError

import atexit
import threading

class RedisPooledConnection:
    def __init__(self, max_connections=10, **redis_params):
        self.pool = redis.ConnectionPool(
            max_connections=max_connections,
            host="127.0.0.1",
            port=6379,
            db=0,
            decode_responses=True,
            client_name="Unmute",
        )
        self._lock = threading.Lock()
        self.client = redis.Redis(connection_pool=self.pool)
        atexit.register(self.close_all)

    def get_client(self):
        return self.client

    def close_all(self):
        with self._lock:
            try:
                self.pool.disconnect()
            except Exception:
                pass

redisPool = RedisPooledConnection(max_connections=8)