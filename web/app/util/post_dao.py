"""
Maria DB post table과 selected_llm_responses view를 관리하는 클래스입니다.
"""

from mariadb_clients import mariaDBPool, MariaDBPooledConnection


class PostDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_key(self, post_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM post WHERE key=%s"
                cursor.execute(sql, (post_key,))
                return cursor.fetchone()
        finally:
            self.pool.release_connection(conn)

    def get_many_selected_by_user_key(self, user_key, count):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM post WHERE user_key=%s ORDER BY post_key DESC LIMIT %s"
                cursor.execute(sql, (user_key, count,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def get_all_selected_by_user_key(self, user_key):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM selected_post WHERE user_key=%s"
                cursor.execute(sql, (user_key,))
                return cursor.fetchall()
        finally:
            self.pool.release_connection(conn)

    def add_post_once(
        self,
        user_key: str,
        refined: str,
        original: str,
        category: dict,
        error: int,
        session_key: str,
    ):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO post (user_key, llm, original, main, sub, minor, error, session) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(
                    sql,
                    (
                        user_key,
                        refined,
                        original,
                        category.get("main"),
                        category.get("sub"),
                        category.get("minor"),
                        error,
                        session_key,
                    ),
                )
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)
    
    def add_post_multiple(self, posts: list[tuple]):
        """
        posts: list of tuples like
            (user_key, refined, original, main, sub, minor, error, session_key)
        """
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                    INSERT INTO post (user_key, llm, original, main, sub, minor, error, session)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING post_key
                """
                cursor.executemany(sql, posts)
                post_keys = cursor.fetchall()
                conn.commit()
                return [row[0] for row in post_keys]
        finally:
            self.pool.release_connection(conn)

post_DAO = PostDAO(mariaDBPool)