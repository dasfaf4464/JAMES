import pymysql
import pymysql.cursors
from pymysql.err import OperationalError
from flask import jsonify

DB_ADMIN = {'id':'root', 'pw':'admin'}
DB_USER = {'id':'user', 'pw':'user'}

def get_db_connection(id, pw):
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

def get_result(SQL, id, pw):
    connection = get_db_connection(id, pw)
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

def put_sql(SQL, id, pw):
    connection = get_db_connection(id, pw)
    try:
        with connection.cursor() as cursor:
            cursor.execute(SQL)
            connection.commit()
    except OperationalError as e:
        return jsonify({"error": "DB 연결 오류", "message": str(e)})
    finally:
        if connection:
            connection.close()
            
'''
SQL injection 대비
SQL transaction 확인 및 에러 처리
'''