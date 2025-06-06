"""
사용자 인증, 가입, 정보를 처리하는 모듈입니다.
"""
from app.util.user_info_dao import user_info_DAO
from app.util.post_dao import post_DAO

import random
import string, re

def login(id: str, pw: str):
    """
    사용자 로그인 처리를 하는 함수입니다.

    Parameters:
        - id (str): 사용자 id
        - pw (str): 사용자 pw
    
    Returns:
        - success (str): 성공 
        - user_key (str): 사용자 인증 키
        - user_name (str): 사용자 이름
    """
    user_info = user_info_DAO.get_by_id(id)
    if user_info == None:
        return "id"
    else:
        if user_info.get("pw") != pw:
            return "pw"
        else:
            return user_info
            

def create_key():
    """
    유저키를 생성하는 함수입니다.
    """
    charset = list(string.ascii_lowercase)
    return "".join(random.sample(charset, 12))

def create_name():
    """
    무작위 이름을 생성하는 함수입니다.
    """
    NAME_ADJ = [
        "Curious", "Wise", "Smart","Kind","Friendly","Clever","Thoughtful","Cheerful","Bright",
        "Honest","Logical","Noble","Insightful","Creative","Calm","Gentle","Patient","Witty","Brilliant",
        "Reliable","Helpful","Eloquent","Focused","Polite","Rational"
    ]

    NAME_NOUN = [
        "Lantern","Library","Notebook","Compass","Quill","Clock","Mirror","Tablet","Candle","Vessel",
        "Scroll","Key","Circuit","Anchor","Helmet","Feather","Stone","Book","Map","Bridge",
        "Tower","Coin","Globe","Ink","Signal",
    ]
    adj = random.choice(NAME_ADJ)
    noun = random.choice(NAME_NOUN)
    return f"{adj} {noun}"


def register(id: str, pw: str, name:str, email:str, user_key:str):
    """
    회원가입을 처리하는 함수입니다.
    """
    user_info = user_info_DAO.get_by_id(id)
    if user_info != None:
        return "id"
    elif re.fullmatch(r'[a-zA-Z0-9]{7,20}', pw):
        return "pw"
    else:
        user_info_DAO.add_user_info(name, id, pw, email, user_key)

def question_count(user_key :str):
    """
    사용자의 질문 개수를 가져오는 함수입니다.
    """
    posts = post_DAO.get_all_selected_by_user_key(user_key)
    
    return posts.count()

def get_from_create_day(user_key: str):
    """
    사용자의 가입일로 부터 지난 날짜를 가져옵니다.
    """
    user_info = user_info_DAO.get_by_user_key(user_key)
    user_info.get("create_at")