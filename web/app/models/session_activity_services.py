"""
세션에서 발생하는 접속이나 이벤트를 관리합니다.
"""

from app.util.redis_dao import redis_DAO
from app.util.post_dao import post_DAO


def join_session(user_key, session_code):

    if redis_DAO.get_activated_users_count(session_code) == 0:
        posts = post_DAO.get_all_select_by_session_key(session_code)

        category_count = {}
        for post in posts:
            category = post.get("main") + "/" + post.get("sub")
            count = category_count.get(category)
            if count == None:
                count = 1
            else:
                count = count + 1
            category_count.update({category:count})

        redis_DAO.increment_multiple_categories(session_code, category_count)

    redis_DAO.set_activated_session(session_code, user_key)

def leave_session(user_key, session_code):
    redis_DAO.remove_user_from_session(session_code, user_key)
    
    if redis_DAO.get_activated_users_count(session_code) == 0:
        redis_DAO.remove_categories(session_code)