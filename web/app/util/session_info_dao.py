"""
Maria DB session_info table을 관리하는 클래스입니다.
"""

from app.util.mariadb_clients import mariaDBPool, MariaDBPooledConnection


class SessionInfoDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_session_key(self, session_key: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM session_info WHERE session_key=%s"
                cursor.execute(sql, (session_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def add_session_info(
        self,
        name: str,
        description: str,
        session_key: str,
        pw: str,
        host_key: str,
        is_temporary: bool,
    ):
        if is_temporary:
            temporary = 1
        else:
            temporary = 0

        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO session_info (name, description, session_key, pw, host, is_temporary) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sql, (name, description, session_key, pw, host_key, temporary)
                )
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def update_by_session_key(self, session_key, description, pw):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = (
                    "UPDATE session_key SET description=%s, pw=%s WHERE session_key=%s"
                )
                cursor.execute(sql, (description, pw, session_key))
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def delete_by_session_key(self, session_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM session_info WHERE session_key=%s"
                cursor.execute(sql, (session_key,))
                conn.commit()
                return cursor.rowcount
        finally:
            self.pool.release_connection(conn)


session_info_DAO = SessionInfoDAO(mariaDBPool)
