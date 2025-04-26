import pymysql
import pymysql.cursors
from pymysql.err import OperationalError
from flask import jsonify

def get_db_connection():
    try:
        db_connection = pymysql.connect(
        host ='localhost',
        user = 'root',
        password = 'admin',
        database = 'capstone',
        charset = 'utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
        return db_connection
    
    except OperationalError as e:
        print(f'db connection error {e}')
        return None

def get_result(SQL):
    connection = get_db_connection()
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

def get_result(SQL):
    connection = get_db_connection()
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