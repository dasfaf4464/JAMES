"""
사용자 인증, 가입, 정보를 처리하는 모듈입니다.
"""
from app.util.user_info_dao import user_info_DAO
from app.util.post_dao import post_DAO

import random, string, re
from datetime import datetime, timezone

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
    if user_info == None or id == "NULL":
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
    key = "".join(random.sample(charset, 12))

    if user_info_DAO.get_by_user_key(key):
        key = "".join(random.sample(charset, 12))

    return key

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


def register(
    id: str | None = None,
    pw: str | None = None,
    name: str = "",
    email: str | None = None,
    user_key: str = "",
    temporary: bool = False,
):
    """
    회원가입을 처리하는 함수입니다.
    """
    if temporary:
        user_info_DAO.add_user_info(
            user_name=name,
            id=None,
            pw=None,
            email=None,
            user_key=user_key,
            temporary=True
        )
        return "ok"

    user_info = user_info_DAO.get_by_id(id)
    if user_info is not None:
        return "id"

    if not re.fullmatch(r'[a-zA-Z0-9]{7,20}', pw):
        return "pw"

    user_info_DAO.update_by_user_key(
        user_name=name,
        id=id,
        pw=pw,
        email=email,
        user_key=user_key,
        temporary=False
    )
    return "ok"


def question_count(user_key :str):
    """
    사용자의 질문 개수를 가져오는 함수입니다.
    """
    posts = post_DAO.get_all_selected_by_user_key(user_key)
    
    return len(posts)


def memo_count(user_key: str):
    """
    """


def get_from_create_day(user_key: str) -> int:
    """
    사용자의 가입일로부터 지난 날짜 수를 반환합니다.

    Args:
        user_key (str): 사용자의 고유 키

    Returns:
        int: 가입일부터 현재까지 지난 일 수
    """
    user_info = user_info_DAO.get_by_user_key(user_key)
    create_at = user_info.get("create_at")

    if not create_at:
        raise ValueError("가입일 정보가 없습니다.")
    if not isinstance(create_at, datetime):
        raise TypeError("create_at이 datetime 타입이 아닙니다.")

    if create_at.tzinfo is None:
        create_at = create_at.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    delta = now - create_at
    return delta.days
