"""
[Profile 페이지]
Profile 페이지 - Profile 페이지는 사용자 기록을 볼 수 있는 페이지 입니다.

router
    - profile(페이지 제공)
    - get_my_question(사용자가 한 질문 가져오기)

작성자 : 조해천
"""

from flask import Blueprint, request, render_template, jsonify

import web.app.models.user_services as user_services

profile_bp = Blueprint("profile", __name__)
get_my_question_bp = Blueprint("get_my_question", __name__, url_prefix="/api/user")


@profile_bp.route("/profile", methods=["GET"])
def profile():
    """
    profile 페이지를 반환하는 API입니다.

    Request:
        Path: "/profile" (GET)
        Cookies:
            - user_name (str): 사용자 이름
            - user_key (str): 사용자 인증 키

    Response:
        HTML:
            - profile.html
            Template Variables:
                - name (str): 사용자 이름
                - day (int): 생성일로부터 지난 일 수
    """
    content = {"name": "", "day": ""}
    cookie = request.cookies

    content["name"] = cookie.get("user_name")
    content["day"] = user_services.get_from_create_day(cookie.get("user_key"))

    return render_template("history.html", **content)


@get_my_question_bp.route("/get/my_questions", methods=["GET"])
def get_my_question():
    """
    사용자가 각 세션들에 게시한 질문을 가져오는 API입니다.
    
    Request:
        Path: "/api/user/get/my_questions" (GET)
        Cookies:
            - user_key (str) : 사용자 인증 키
    
    Query Params:
        - count (int): 가져올 개수

    Response:
        JSON (List):
            - original_text (str): 원본 질문
            - refined_text (str): llm을 거친 질문
            - category (dict): 카테고리 입니다.
            - memo (str): 작성된 메모입니다.
    """
    data = request.get_json()
    cookie = request.cookies