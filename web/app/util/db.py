import pymysql
import pymysql.cursors
from pymysql.err import OperationalError, Error
import redis
from redis.exceptions import ConnectionError

DB_ADMIN = {"id": "root", "pw": "admin"}
DB_USER = {"id": "user", "pw": "user"}
REDIS_DBNUM = {"before-llm": 0, "after-llm": 1, "all-q&a": 2}


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


def disconnection_mariadb(connection: pymysql.Connection):
    try:
        connection.close()
    except Error as e:
        print("mariadb already disconnected")


def get_redis_connection(dbnum: int):
    try:
        redis_connection = redis.Redis(
            host="127.0.0.1", port=6379, db=dbnum, decode_responses=True
        )
        print("redis 서버 연결 성공:", redis_connection.ping())
        return redis_connection
    except ConnectionError as e:
        print("Redis 연결 실패:", e)
        return None


def disconnect_redis(redis: redis.Redis.client):
    try:
        redis.client_kill(redis)
    except ConnectionError as e:
        print("redis already disconnected")


"""
SQL injection 대비
SQL transaction 확인 및 에러 처리
"""
