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

    def insert_user(self, user_name, user_key, temporary=True):
        """
        임시회원 등록용 함수
        id, pw, email은 None으로 저장
        """
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO user_info (user_name, id, pw, email, user_key, temporary)
                    VALUES (%s, NULL, NULL, NULL, %s, %s)
                """
                cursor.execute(sql, (user_name, user_key, int(temporary)))
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def update_by_user_key(self, user_key, user_name, id, pw, email, temporary):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                # user_name이 None이면 컬럼 업데이트에서 제외
                if user_name is None:
                    sql = """
                        UPDATE user_info
                        SET id=%s, pw=%s, email=%s, temporary=%s
                        WHERE user_key=%s
                    """
                    cursor.execute(sql, (id, pw, email, int(temporary), user_key))
                else:
                    sql = """
                        UPDATE user_info
                        SET user_name=%s, id=%s, pw=%s, email=%s, temporary=%s
                        WHERE user_key=%s
                    """
                    cursor.execute(sql, (user_name, id, pw, email, int(temporary), user_key))

                if cursor.rowcount == 0:
                    raise Exception("해당 user_key에 해당하는 유저 정보가 없습니다.")

                conn.commit()
                return True
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
