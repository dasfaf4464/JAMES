"""
사용자가 작성한 게시글을 관리하는 모듈입니다.
"""

from app.util.post_dao import post_DAO

import datetime

def get_all_posts(user_key: str):
    posts = post_DAO.get_all_selected_by_user_key(user_key)
    result = []
    for post in posts:
        create_at_str = post['create_at'].strftime("%Y-%m-%d %H:%M:%S") if post['create_at'] else None
        result.append({
            "create_at": create_at_str,
            "original": post['original'],
            "llm": post['llm'],
            "main": post['main'],
            "sub": post['sub'],
            "minor": post['minor']
        })
        
    return result