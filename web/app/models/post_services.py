"""
사용자가 작성한 게시글을 관리하는 모듈입니다.
"""

from app.util.post_dao import post_DAO
from app.util.redis_dao import redis_DAO
import app.util.mistral_client as mistral
from app.util.mistral_client import mistral_client

import datetime


def get_all_posts(user_key: str):
    posts = post_DAO.get_all_selected_by_user_key(user_key)
    result = []
    for post in posts:
        create_at_str = (
            post["create_at"].strftime("%Y-%m-%d %H:%M:%S")
            if post["create_at"]
            else None
        )
        result.append(
            {
                "create_at": create_at_str,
                "original": post["original"],
                "llm": post["llm"],
                "main": post["main"],
                "sub": post["sub"],
                "minor": post["minor"],
            }
        )

    return result


def get_post_by_category_in_session(session_key: str, main: str, sub: str):
    posts = post_DAO.get_all_select_by_session_key(session_key)

    post_list = []

    for post in posts:
        if post.get("main") == main and post.get("sub") == sub:
            view = {
                "original": post.get("original"),
                "refined_text": post.get("llm"),
                "memo": "",
                "minor": post.get("minor"),
            }
            post_list.append(view)
    return post


def get_session_category(session_key):
    posts = post_DAO.get_all_select_by_session_key(session_key)

    categories = {}

    for post in posts:
        category = post.get("main") + "/" + post.get("sub")
        if category in categories:
            category_count = categories.get(category) + 1
        else:
            category_count = 1
        categories.update({category: category_count})
    return categories


def get_post_by_keys(post_keys):
    post_list = []
    for post_key in post_keys:
        post = post_DAO.get_by_postkey(post_key)
        post_list.append(post)
    return post_list


def select_post(session_code, post_key):
    post_DAO.update_post_selected(post_key)
    post = post_DAO.get_by_postkey(post_key)
    category = post.get("main") + "/" + post.get("sub")
    redis_DAO.increment_category_count(session_code, category)


def send_llm(user_key, session_code, text):
    def dict_list_to_tuples(dict_list, user_key, original_text, session_key):
        tuples_list = []
        for item in dict_list:
            main = item["category"].get("main", "")
            sub = item["category"].get("sub", "")
            minor = item["category"].get("minor", "")
            error = item.get("error", 0)
            refined = item.get("content", "")

            tuples_list.append(
                (user_key, refined, original_text, main, sub, minor, error, session_key)
            )
        return tuples_list

    if not text or not isinstance(text, str):
        raise ValueError("입력된 텍스트가 유효하지 않습니다.")

    pre_text = mistral.preprocess(text)
    refined = mistral_client.request(pre_text)

    if refined is None:
        raise RuntimeError("LLM 요청 실패: refined 값이 None입니다.")

    post_texts = mistral.postprocess(refined)

    error_0_posts = post_texts[0]
    error_1_posts = post_texts[1]
    error_2_posts = post_texts[2]

    db_num = []
    if error_0_posts:
        tuple_list = dict_list_to_tuples(error_0_posts, user_key, text, session_code)
        db_num.append(post_DAO.add_post_multiple(tuple_list))

    if error_1_posts:
        tuple_list = dict_list_to_tuples(error_1_posts, user_key, text, session_code)
        db_num.append(post_DAO.add_post_multiple(tuple_list))

    if error_2_posts:
        tuple_list = dict_list_to_tuples(error_2_posts, user_key, text, session_code)
        db_num.append(post_DAO.add_post_multiple(tuple_list))

    return db_num[0]
