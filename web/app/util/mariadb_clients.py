"""
Maria DB와 연결하는 클라이언트와 클라이언트를 관리하는 모듈입니다.
"""

import pymysql
import pymysql.cursors as cursors
from pymysql.err import OperationalError, Error

import atexit
from queue import Queue, Empty
import threading
import concurrent.futures


class MariaDBPooledConnection:
    def __init__(self, maxsize=5):
        self.pool = Queue(maxsize)
        self.lock = threading.Lock()
        for _ in range(maxsize):
            conn = self._create_connection()
            self.pool.put(conn)
        atexit.register(self.close_all)

    def _create_connection(self):
        return pymysql.connect(
            host="127.0.0.1",
            user="root",
            password="admin",
            database="capstone",
            charset="utf8mb4",
            cursorclass=cursors.DictCursor,
        )

    def get_connection(self, timeout=5):
        try:
            conn = self.pool.get(timeout=timeout)
            if not conn.open:
                conn = self._create_connection()
            return conn
        except Empty:
            raise OperationalError("DB connection pool exhausted.")

    def release_connection(self, conn):
        if conn.open:
            try:
                self.pool.put(conn)
            except Exception:
                conn.close()
        else:
            conn.close()
            new_conn = self._create_connection()
            self.pool.put(new_conn)

    def close_all(self):
        with self.lock:
            while not self.pool.empty():
                conn = self.pool.get_nowait()
                try:
                    conn.close()
                except Exception:
                    pass


mariaDBPool = MariaDBPooledConnection(maxsize=8)

class PostDAO:
    def __init__(self, connection_pool: MariaDBPooledConnection):
        self.pool = connection_pool

    def get_post(self, post_id):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "SELECT * FROM posts WHERE id=%s"
                cursor.execute(sql, (post_id,))
                return cursor.fetchone()
        finally:
            self.pool.release_connection(conn)

    def add_post(self, title, content):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
                cursor.execute(sql, (title, content))
                conn.commit()
                return cursor.lastrowid
        finally:
            self.pool.release_connection(conn)

    def update_post(self, post_id, title, content):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "UPDATE posts SET title=%s, content=%s WHERE id=%s"
                cursor.execute(sql, (title, content, post_id))
                conn.commit()
                return cursor.rowcount
        finally:
            self.pool.release_connection(conn)

    def delete_post(self, post_id):
        conn = self.pool.get_connection()
        try:
            with conn.cursor() as cursor:
                sql = "DELETE FROM posts WHERE id=%s"
                cursor.execute(sql, (post_id,))
                conn.commit()
                return cursor.rowcount
        finally:
            self.pool.release_connection(conn)