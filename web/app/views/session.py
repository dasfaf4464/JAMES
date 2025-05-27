from flask import Blueprint, render_template, request
from app.manager.db_manager import mariadb_user_manager
import re

session_bp = Blueprint("session", __name__)


@session_bp.route("/session/<sessioncode>")
def session(sessioncode):
    content = {"error": "True", "pw": None}
    user_key = request.cookies.get("user_key")

    def is_valid_session_code(code: str) -> bool:
        pattern = r"^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$"
        return bool(re.match(pattern, code))

    if not sessioncode:
        return render_template("session.html", **content)  # 세션 주소가 없을때

    if not is_valid_session_code(sessioncode):  # 세션 포맷이 잘못되었을 때
        return render_template("session.html", **content)

    session = mariadb_user_manager.select("sessioninfo", {"session_key": sessioncode})
    if session:  # 세션이 존재할 때
        pw = session[0].get("pw")
        title = session[0].get("title")
        content.update({"error": "False", "pw": pw, "name": title})
        return render_template("session.html", **content)

    return render_template("session.html", **content)
