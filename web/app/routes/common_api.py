from flask import Blueprint, request, g, redirect, url_for
import app.models.user_services as user_services
from datetime import datetime, timezone, timedelta

check_cookie_bp = Blueprint("check_cookie", __name__)
set_cookie_bp = Blueprint("set_cookie", __name__)
authorize_bp = Blueprint("authorize_bp", __name__)


@check_cookie_bp.before_app_request
def ensure_cookie():
    """
    사용자 쿠키를 확인합니다.
    """
    cookie = request.cookies
    # user_key가 없으면 새 쿠키 세팅 필요 표시
    if not cookie.get("user_key"):
        g.need_set_cookie = True


@set_cookie_bp.after_app_request
def set_cookie(response):
    """
    사용자 쿠키를 확인하고 관리합니다.
    """
    # 로그인/로그아웃 API는 쿠키 처리 제외
    if request.path in ("/api/user/login", "/api/user/logout", "/api/user/signup"):
        return response

    MAXAGE = 10800  # 3시간

    cookie = request.cookies

    # 새 쿠키 세팅이 필요한 경우 (user_key 없을 때)
    if getattr(g, "need_set_cookie", False):
        user_name = user_services.create_name()
        user_key = user_services.create_key()
        result = user_services.register(name=user_name, user_key=user_key, temporary=True)
        if result != "ok":
            # 로그 기록 또는 에러처리 가능
            print("[WARN] 임시 사용자 생성 실패")

        response.set_cookie(
            key="user_name",
            value=user_name,
            max_age=MAXAGE,
            path="/",
            samesite="Lax",
        )
        response.set_cookie(
            key="user_key",
            value=user_key,
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

    # 기존 쿠키가 있고, temporary 상태가 True인 경우 (임시 유저)
    if cookie.get("temporary") == "True":
        # 쿠키 갱신 (재설정)
        for key in ("user_name", "user_key", "temporary"):
            if cookie.get(key):
                response.set_cookie(
                    key=key,
                    value=cookie.get(key),
                    max_age=MAXAGE,
                    httponly=(key != "user_name"),  # user_name은 httponly False로 둠
                    path="/",
                    samesite="Lax",
                )
        return response

    # 기존 쿠키가 있고, temporary 상태가 False인 경우 (정식 유저)
    if cookie.get("temporary") == "False":
        expire_time = datetime.now(timezone.utc) + timedelta(days=7)
        for key in ("user_name", "user_key", "temporary"):
            if cookie.get(key):
                response.set_cookie(
                    key=key,
                    value=cookie.get(key),
                    expires=expire_time,
                    httponly=(key != "user_name"),
                    path="/",
                    samesite="Lax",
                )
        return response

    # 그 외(temporary 쿠키 없거나 알 수 없는 상태) - 기본 임시 유저로 재설정
    user_name = user_services.create_name()
    user_key = user_services.create_key()
    result = user_services.register(name=user_name, user_key=user_key, temporary=True)
    if result != "ok":
        print("[WARN] 임시 사용자 생성 실패")

    response.set_cookie(
        key="user_name",
        value=user_name,
        max_age=MAXAGE,
        path="/",
        samesite="Lax",
    )
    response.set_cookie(
        key="user_key",
        value=user_key,
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


@authorize_bp.before_app_request
def authorize():
    """
    사용자 권한을 확인하고 권한에 맞지 않으면 제한합니다.
    """
    # 접근 제한 대상 블루프린트 목록
    CANNOTACCESS_NONMEMBER = {"home", "profile"}
    CANNOTACCESS_MEMBER = {"index", "register"}

    cookie = request.cookies
    temporary = cookie.get("temporary")

    # blueprint가 None일 수 있으니 예외 처리
    current_blueprint = request.blueprint or ""

    if temporary == "True":
        # 임시 유저는 회원만 접근 가능한 페이지 접근 제한
        if current_blueprint in CANNOTACCESS_NONMEMBER:
            return redirect(url_for("index.index"))

    elif temporary == "False":
        # 정식 회원은 비회원용 페이지 접근 제한
        if current_blueprint in CANNOTACCESS_MEMBER:
            return redirect(url_for("home.home"))

    else:
        # temporary 쿠키 없거나 알 수 없는 경우 -> 비회원용 페이지만 접근 가능하게 제한
        if current_blueprint in CANNOTACCESS_NONMEMBER:
            return redirect(url_for("index.index"))
