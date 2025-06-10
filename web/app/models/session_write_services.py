"""
세션을 생성하거나 세션 정보를 변경하는 모듈입니다.
"""

from app.util.session_info_dao import session_info_DAO
from app.util.my_session_dao import my_session_DAO
from app.util.redis_dao import redis_DAO
import random, string

def _create_session_code():
    letters = random.choices(string.ascii_uppercase, k=8)
    digits = random.choices(string.digits, k=4)
    chars = letters + digits
    random.shuffle(chars)

    part1 = ''.join(chars[0:4])
    part2 = ''.join(chars[4:8])
    part3 = ''.join(chars[8:12])

    return f"{part1}-{part2}-{part3}"

def create_session(host_key:str, title:str, description:str, pw :str, temporary = None):
    """
    세션을 생성합니다.

    Parameters:

    Returns:
    """
    session_code = _create_session_code()
    if session_info_DAO.get_by_session_key(session_code):
        session_code = _create_session_code()
    
    session_info_DAO.add_session_info(title, description, session_code, pw, host_key, temporary)
    
    return session_code

def add_my_session(user_key, session_code):
    my_session_DAO.join_session(user_key, session_code)

def exit_user(session_key: str, user_key: str):
    if my_session_DAO.exit_session(user_key, session_key) == 1:
        return True
    else:
        return False