"""
세션 정보를 가져오는 모듈입니다.
"""

from app.util.my_session_dao import my_session_DAO
from app.util.session_info_dao import session_info_DAO
from app.util.post_dao import post_DAO
from app.util.redis_dao import redis_DAO


def get_session_list(user_key: str, start_index: int, count: int):
    """
    사용자가 속한 세션을 가져오는 함수입니다.
    """
    my_sessions = my_session_DAO.get_by_user_key(user_key)
    session_keys = [session["session_key"] for session in my_sessions]
    selected_keys = session_keys[start_index : start_index + count]

    sessions = []
    for session_key in selected_keys:
        session_list = session_info_DAO.get_by_session_key(session_key)
        if session_list:
            name = session_list[0]["name"]
            type = session_list[0]["is_temporary"]
            if type == "1":
                period = "임시"
            else:
                period = "영구"

            people_count = redis_DAO.get_activated_users_count(session_key)
            questions = len(post_DAO.get_all_select_by_session_key(session_key))
            sessions.append(
                {
                    "name": name,
                    "people": people_count,
                    "questions": questions,
                    "type": period,
                    "session_key": session_key,
                }
            )
    return sessions


def get_session_info(session_key: str):
    """
    세션에 대한 정보를 가져옵니다.
    """
    session = session_info_DAO.get_by_session_key(session_key)
    session = session[0]
    create_datetime = session.get("create_at")
    create_date = create_datetime.strftime("%Y-%m-%d")
    create_time = create_datetime.strftime("%H:%M:%S")
    people_count = redis_DAO.get_activated_users_count(session_key)
    questions = len(post_DAO.get_all_select_by_session_key(session_key))

    session.update(
        {
            "people": people_count,
            "questions": questions,
            "created_date": create_date,
            "created_time": create_time,
            "entered_at": "NULL",
        }
    )
    return session
