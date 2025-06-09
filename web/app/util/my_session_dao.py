"""
Maria DB my_session table을 관리하는 클래스입니다.
"""

from app.util.mariadb_clients import mariaDBPool, MariaDBPooledConnection


class MySessionDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_user_key(self, user_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM my_session WHERE user_key=%s"
                cursor.execute(sql, (user_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def get_by_session_key(self, session_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM my_session WHERE session_key=%s"
                cursor.execute(sql, (session_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def join_session(self, user_key, session_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql_insert = """
                    INSERT IGNORE INTO my_session(user_key, session_key)
                    VALUES (%s, %s)
                """
                cursor.execute(sql_insert, (user_key, session_key))
                conn.commit()
                return cursor.lastrowid  # 삽입되지 않았다면 0이거나 None일 수 있음
        finally:
            self.pool.release_connection(conn)

    def exit_session(self, user_key, session_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM my_session WHERE user_key=%s and session_key=%s"
                cursor.execute(
                    sql,
                    (
                        user_key,
                        session_key,
                    ),
                )
                conn.commit()
                return cursor.rowcount
        finally:
            self.pool.release_connection(conn)


my_session_DAO = MySessionDAO(mariaDBPool)
