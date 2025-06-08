"""
Maria DB post table과 selected_llm_responses view를 관리하는 클래스입니다.
"""

from app.util.mariadb_clients import mariaDBPool, MariaDBPooledConnection


class PostDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_by_postkey(self, post_key):
        conn = self.pool.get_connection()
        try:
            conn.commit()  # 혹은 conn.rollback()
            with conn.cursor() as cursor:
                sql = "SELECT * FROM post WHERE post_key=%s"
                cursor.execute(sql, (post_key,))
                return cursor.fetchone()
        finally:
            self.pool.release_connection(conn)

    def get_many_selected_by_user_key(self, user_key, count):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM post WHERE user_key=%s ORDER BY post_key DESC LIMIT %s"
                cursor.execute(
                    sql,
                    (
                        user_key,
                        count,
                    ),
                )
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

    def get_all_select_by_session_key(self, session_key: str):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM selected_post WHERE session=%s"
                cursor.execute(sql, (session_key,))
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
                """
                cursor.executemany(sql, posts)
                conn.commit()

                n = len(posts)
                if n == 0:
                    return []

                user_key = posts[0][0]
                original = posts[0][2]
                session_key = posts[0][7]

                cursor.execute(
                    f"""
                    SELECT post_key FROM post
                    WHERE user_key = %s AND original = %s AND session = %s
                    ORDER BY post_key DESC
                    LIMIT {n}
                """,
                    (user_key, original, session_key),
                )

                rows = cursor.fetchall()
                post_keys = [row["post_key"] for row in reversed(rows)]
                return post_keys
        finally:
            self.pool.release_connection(conn)

    def update_post_selected(self, post_key):
        from pymysql.err import MySQLError

        conn = self.pool.get_connection()
        try:
            conn.autocommit(False)  # autocommit 해제
            with conn.cursor() as cursor:
                cursor.execute(
                    "SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;"
                )
                conn.begin()

                cursor.execute(
                    "SELECT selected FROM post WHERE post_key = %s FOR UPDATE;",
                    (post_key,),
                )
                row = cursor.fetchone()
                if row is None:
                    conn.rollback()
                    return 0

                selected = row["selected"]
                if selected == 1:
                    conn.rollback()
                    return 0

                cursor.execute(
                    "UPDATE post SET selected = 1 WHERE post_key = %s AND selected = 0;",
                    (post_key,),
                )
                conn.commit()
                return cursor.rowcount

        except MySQLError as e:
            conn.rollback()
            raise e
        finally:
            self.pool.release_connection(conn)


post_DAO = PostDAO(mariaDBPool)
