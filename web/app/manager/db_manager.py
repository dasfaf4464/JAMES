"""
사용자가 입력한 채팅 데이터를 관리하고 사용자 정보, 세션 정보를 관리합니다.
"""

import pymysql
import pymysql.cursors
from pymysql.err import OperationalError, Error

import redis
from redis.exceptions import ConnectionError

import atexit
import json

# MariaDB id&pw
DB_ADMIN = {"id": "root", "pw": "admin"}
DB_USER = {"id": "user", "pw": "user"}
# Redis DB number
REDIS_DBNUM = {"sessions": 0}


"""
maria db class foundation fuctions
"""
def get_mariadb_connection(id: str, pw: str):
    try:
        db_connection = pymysql.connect(
            host="127.0.0.1",
            user=id,
            password=pw,
            database="capstone",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )
        return db_connection

    except OperationalError as e:
        print(f"db connection error {e}")
        return None


def get_result(connection, SQL: str, params=None):
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            if params:
                cursor.execute(SQL, params)  # 파라미터화된 쿼리 사용
            else:
                cursor.execute(SQL)  # 파라미터가 없을 경우 그냥 실행
            connection.commit()
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(f"Error: {e}")
        return []


def put_sql(connection, SQL: str, params=None):
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            if params:
                cursor.execute(SQL, params)
            else:
                cursor.execute(SQL)
            connection.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def disconnect_mariadb(connection: pymysql.Connection):
    try:
        connection.close()
    except Error as e:
        print("mariadb already disconnected")


class MariadbManager:
    def __init__(self, id, pw):
        self.account = get_mariadb_connection(id, pw)
        atexit.register(self.disconnect)

    def disconnect(self):
        disconnect_mariadb(self.account)

    def is_connected(self):
        return self.account is not None

    def insert(self, table: str, data: dict):
        """
        Args:
            table (str): 테이블 이름
            data (dict): {"column": value} 형식

        Example:
            insert("users", { "name": "Alice", "age": 25 })
        """
        if not self.is_connected():
            print("연결된 db가 없습니다.")
            return False

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return put_sql(self.account, sql, values)

    def select(self, table: str, where: dict = None):
        """
        Args:
            table (str): 테이블 이름
            where (dict, optional): 조건 {"column": value}

        예시:
            db.select("users")  # 전체 선택
            db.select("users", {"age": 25})  # age가 25인 행들
        """
        if not self.is_connected():
            print("연결된 db가 없습니다.")
            return []

        if where:
            conditions = " AND ".join([f"{k}=%s" for k in where])
            sql = f"SELECT * FROM {table} WHERE {conditions}"
            values = tuple(where.values())
        else:
            sql = f"SELECT * FROM {table}"
            values = None

        return get_result(self.account, sql, values)

    def update(self, table: str, data: dict, where: dict):
        """
        Args:
            table (str): 테이블 이름
            data (dict): 변경할 값 {"column": value}
            where (dict): 조건 {"column": value}

        예시:
            db.update("users", {"age": 26}, {"name": "Alice"})
        """
        if not self.is_connected():
            print("연결된 db가 없습니다.")
            return False

        set_clause = ", ".join([f"{k}=%s" for k in data])
        where_clause = " AND ".join([f"{k}=%s" for k in where])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        values = tuple(data.values()) + tuple(where.values())
        return put_sql(self.account, sql, values)

    def delete(self, table: str, where: dict):
        """
        Args:
            table (str): 테이블 이름
            where (dict): 삭제 조건 {"column": value}

        예시:
            db.delete("users", {"name": "Alice"})
        """
        if not self.is_connected():
            print("연결된 db가 없습니다.")
            return False

        where_clause = " AND ".join([f"{k}=%s" for k in where])
        sql = f"DELETE FROM {table} WHERE {where_clause}"
        values = tuple(where.values())
        return put_sql(self.account, sql, values)

    def put_sql(self, SQL: str, params: tuple):
        if self.account is not None:
            return put_sql(self.account, SQL, params)
        else:
            print("연결된 db가 없습니다.")

    def put_sql_result(self, SQL: str, params: tuple):
        if self.account is not None:
            return get_result(self.account, SQL, params)
        else:
            print("연결된 db가 없습니다.")


"""
redis manager foundation functions
"""
def get_redis_connection(dbnum: int = 0):
    """Redis 3 호환: Redis에 연결하고 성공 여부 확인"""
    try:
        client = redis.StrictRedis(
            host="127.0.0.1", port=6379, db=dbnum, decode_responses=True
        )
        client.ping()
        print("Redis 서버 연결 성공")
        return client
    except ConnectionError as e:
        print("Redis 연결 실패:", e)
        return None


class RedisManager:
    def __init__(self, redis_db_num: int = 0):
        self.redis_client = get_redis_connection(redis_db_num)

    def set_json(self, key: str, data: dict) -> bool:
        """
        JSON 형태의 데이터를 Redis에 저장합니다.

        Args:
            key (str): Redis 키
            data (dict): 저장할 딕셔너리 데이터

        Example:
            redis_manager.set_json("user:1001", {"name": "Alice", "age": 30})
        """
        try:
            json_data = json.dumps(data)
            return self.redis_client.set(key, json_data)
        except Exception as e:
            print(f"Error setting JSON data: {e}")
            return False

    def get_json(self, key: str) -> dict | None:
        """
        Redis에 저장된 JSON 데이터를 읽어와 dict로 반환합니다.

        Args:
            key (str): Redis 키

        Returns:
            dict or None: 저장된 딕셔너리 데이터 또는 None (없으면)

        Example:
            user = redis_manager.get_json("user:1001")
        """
        try:
            json_data = self.redis_client.get(key)
            if json_data is None:
                return None
            return json.loads(json_data)
        except Exception as e:
            print(f"Error getting JSON data: {e}")
            return None

mariadb_admin_manager = MariadbManager(DB_ADMIN.get("id"), DB_ADMIN.get("pw"))
mariadb_user_manager = MariadbManager(DB_USER.get("id"), DB_USER.get("pw"))
redis_manager = RedisManager(0)

def tmp_session_cleaner():
    import time
    while True:
        SQL = "DELETE FROM sessioninfo WHERE is_temporary = 1 AND create_at < NOW() - INTERVAL 3 HOUR"
        mariadb_admin_manager.put_sql(SQL=SQL, params = ())
        time.sleep(1800)