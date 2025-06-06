"""
Maria DB my_session table을 관리하는 클래스입니다.
"""

from mariadb_clients import mariaDBPool, MariaDBPooledConnection


class MySessionDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_user_key(self, user_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user_info WHERE user_key=%s"
                cursor.execute(sql, (user_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def get_by_session_key(self, session_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user_info WHERE session_key=%s"
                cursor.execute(sql, (session_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)


my_session_DAO = MySessionDAO(mariaDBPool)
