import pymysql
import pymysql.cursors
from pymysql.err import OperationalError
import redis
from redis.exceptions import ConnectionError
from flask import jsonify

DB_ADMIN = {'id':'root', 'pw':'admin'}
DB_USER = {'id':'user', 'pw':'user'}

def get_mariadb_connection(id:str, pw:str):
    try:
        db_connection = pymysql.connect(
        host ='localhost',
        user = id,
        password = pw,
        database = 'capstone',
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
        return db_connection
    
    except OperationalError as e:
        print(f'db connection error {e}')
        return None

def get_result(SQL:str, id:str, pw:str):
    connection = get_mariadb_connection(id, pw)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            result = cursor.fetchall()
            return jsonify(result)
    except OperationalError as e:
        return jsonify({"error": "DB 연결 오류", "message": str(e)})
    finally:
        if connection:
            connection.close()

def put_sql(SQL:str, id:str, pw:str):
    connection = get_mariadb_connection(id, pw)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            connection.commit()
    except OperationalError as e:
        return jsonify({"error": "DB 연결 오류", "message": str(e)})
    finally:
        if connection:
            connection.close()

def get_redis_connection(dbnum:int):
    try:
        redis_connection = redis.Redis(host='localhost', port=6379, db=dbnum, decode_responses=True)
        print("redis 서버 연결 성공:", redis_connection.ping())  # 서버 연결 확인
        return redis_connection
    except ConnectionError as e:
        print("Redis 연결 실패:", e)
        return None


'''
SQL injection 대비
SQL transaction 확인 및 에러 처리
'''