"""
모든 페이지에 공통적으로 적용되는 API입니다.

router
    - ensure_cookie(쿠키 확인)
    - authorize(권한 확인)

작성자 : 조해천
"""
from flask import Blueprint, request, g, redirect, url_for

import app.models.user_services as user_services

from datetime import datetime, timezone, timedelta

check_cookie_bp = Blueprint("check_cookie", __name__)
set_cookie_bp = Blueprint("set_cookie", __name__)
authorize_bp = Blueprint("authorize_bp", __name__)


@check_cookie_bp.before_app_request#checked
def ensure_cookie():
    """
    사용자 쿠키를 확인합니다.
    """
    cookie = request.cookies
    if cookie.get("user_key") is None:
        g.need_set_cookie = True


@set_cookie_bp.after_app_request#checked
def set_cookie(response):
    """
    사용자 쿠키를 확인하고 관리합니다.
    """
    if request.path =="/api/user/login" or request.path =="/api/user/logout":
        return response

    MAXAGE = 10800

    cookie = request.cookies

    if getattr(g, "need_set_cookie", False):
        user_name = user_services.create_name()
        user_key = user_services.create_key()
        user_services.register(name=user_name, user_key=user_key, temporary=True)

        response.set_cookie(
            key="user_name",
            value=user_name,
            max_age=MAXAGE,
            path='/',
            samesite="Lax",
        )
        response.set_cookie(
            key="user_key",
            value=user_key,
            max_age=MAXAGE,
            httponly=True,
            path='/',
            samesite="Lax",
        )
        response.set_cookie(
            key="temporary",
            value="True",
            max_age=MAXAGE,
            httponly=True,
            path='/',
            samesite="Lax",
        )
        return response
    elif cookie.get("temporary") == "True":
        response.set_cookie(
            key="user_name",
            value=cookie.get("user_name"),
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            key="user_key",
            value=cookie.get("user_key"),
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            key="temporary",
            value="True",
            max_age=MAXAGE,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response
    else:
        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        response.set_cookie(
            key="user_name",
            value=cookie.get("user_name"),
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            key="user_key",
            value=cookie.get("user_key"),
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            key="temporary",
            value="False",
            expires=expire_time,
            httponly=True,
            path="/",
            samesite="Lax",
        )
        return response

@authorize_bp.before_app_request#checked
def authorize():
    """
    사용자 권한을 확인하고 권한에 맞지 않으면 제한합니다.
    """
    CANNOTACCESS_NONMEMBER = ("home", "profile")
    CANNOTACCESS_MEMBER = ("index", "register")

    cookie = request.cookies

    if cookie.get("temporary") == "True":
        if request.blueprint in CANNOTACCESS_NONMEMBER:
            return redirect(url_for("index.index"))

    elif cookie.get("temporary") == "False":
        if request.blueprint in CANNOTACCESS_MEMBER:
            return redirect(url_for("home.home"))

    else:
        if request.blueprint in CANNOTACCESS_NONMEMBER:
            return redirect(url_for("index.index"))