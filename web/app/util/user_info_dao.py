"""
Maria DB user_info table을 관리하는 클래스입니다.
"""

from app.util.mariadb_clients import mariaDBPool, MariaDBPooledConnection


class UserInfoDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_user_key(self, user_key: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user_info WHERE user_key=%s"
                cursor.execute(sql, (user_key,))
                return cursor.fetchone()
        finally:
            self.pool.release_connection(conn)

    def get_by_id(self, id: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM user_info WHERE id=%s"
                cursor.execute(sql, (id,))
                return cursor.fetchone()
        finally:
            self.pool.release_connection(conn)

    def add_user_info(
        self,
        user_name: str,
        id: str | None,
        pw: str | None,
        email: str | None,
        user_key: str,
        temporary: bool,
    ):
        if temporary:
            temp = 1
        else:
            temp = 0
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO user_info (user_name, id, pw, email, user_key, temporary) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (user_name, id, pw, email, user_key, temp))
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def update_by_user_key(self, user_key: str, user_name:str, id:str, pw: str, email: str, temporary:bool):
        conn = self.pool.get_connection()
        if temporary:
            temp = 1
        else:
            temp = 0
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE user_info SET user_name=%s, id=%s,pw=%s, email=%s, temporary=%s WHERE user_key=%s"
                cursor.execute(sql, (user_name, id, pw, email, temp, user_key))
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def delete_by_id(self, id: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM user_info WHERE id=%s"
                cursor.execute(sql, (id,))
                conn.commit()
                return cursor.rowcount
        finally:
            self.pool.release_connection(conn)


user_info_DAO = UserInfoDAO(mariaDBPool)
