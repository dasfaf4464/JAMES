from app.util.user_info_dao import user_info_DAO
from app.util.post_dao import post_DAO

import random, string
from datetime import datetime, timezone


def login(id: str, pw: str):
    user_info = user_info_DAO.get_by_id(id)
    if user_info is None or id == "NULL":
        return "id"
    if user_info.get("pw") != pw:
        return "pw"
    return user_info


def create_key():
    charset = list(string.ascii_lowercase)
    key = "".join(random.sample(charset, 12))

    if user_info_DAO.get_by_user_key(key):
        key = "".join(random.sample(charset, 12))

    return key


def create_name():
    NAME_ADJ = [
        "Curious", "Wise", "Smart", "Kind", "Friendly", "Clever",
        "Thoughtful", "Cheerful", "Bright", "Honest", "Logical", "Noble",
        "Insightful", "Creative", "Calm", "Gentle", "Patient", "Witty",
        "Brilliant", "Reliable", "Helpful", "Eloquent", "Focused", "Polite", "Rational",
    ]

    NAME_NOUN = [
        "Lantern", "Library", "Notebook", "Compass", "Quill", "Clock",
        "Mirror", "Tablet", "Candle", "Vessel", "Scroll", "Key", "Circuit",
        "Anchor", "Helmet", "Feather", "Stone", "Book", "Map", "Bridge",
        "Tower", "Coin", "Globe", "Ink", "Signal",
    ]
    adj = random.choice(NAME_ADJ)
    noun = random.choice(NAME_NOUN)
    return f"{adj} {noun}"


def register(user_id=None, user_key=None, pw=None, email=None, name=None, temporary=False):
    if temporary:
        # 임시 사용자 생성
        try:
            user_info_DAO.insert_user(user_name=name, user_key=user_key, temporary=True)
            return "ok"
        except Exception as e:
            print(f"[ERROR] Temporary user registration failed: {e}")
            return "error"
    else:
        # 정식 회원 등록: 기존 임시 사용자를 업데이트
        try:
            # ID 중복 체크
            if user_info_DAO.get_by_id(user_id):
                return "duplicate_id"

            result = user_info_DAO.update_by_user_key(
                user_key=user_key,
                user_name=None,  # 이름 변경 없으면 None으로 두고 DAO가 유지하도록 수정 가능
                id=user_id,
                pw=pw,
                email=email,
                temporary=False,
            )

            if result:
                return "ok"
            return "error"
        except Exception as e:
            print(f"[ERROR] User registration failed: {e}")
            return "error"


def question_count(user_key: str):
    posts = post_DAO.get_all_selected_by_user_key(user_key)
    return len(posts)


def memo_count(user_key: str):
    pass  # 구현 필요


def get_from_create_day(user_key: str) -> int:
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
