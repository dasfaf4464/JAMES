"""
API를 관리하는 모듈입니다.
사용자의 모든 요청을 처리하는 API가 정의되어있습니다.
각 파일에는 페이지와 1:1로 연결되어 있습니다.

작성자 - 조해천
"""
from flask import Flask
from flask_socketio import SocketIO

from app.routes.common_api import check_cookie_bp, set_cookie_bp, authorize_bp
from app.routes.index import index_bp, login_bp, create_session_at_index_bp
from app.routes.register import register_bp, create_name_bp, sign_up_bp
from app.routes.home import (
    home_bp,
    logout_bp,
    get_my_session_bp,
    create_session_at_home_bp,
)
from app.routes.profile import profile_bp, get_my_question_bp
from app.routes.session import (
    session_bp,
    get_session_info_bp,
    pass_session_lock_bp,
    get_previous_category_bp,
    refine_text_bp,
    get_category_questions_bp,
)


def create_app():
    app = Flask(__name__)

    app.register_blueprint(check_cookie_bp)
    app.register_blueprint(set_cookie_bp)
    app.register_blueprint(authorize_bp)

    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(create_session_at_index_bp)

    app.register_blueprint(register_bp)
    app.register_blueprint(create_name_bp)
    app.register_blueprint(sign_up_bp)

    app.register_blueprint(home_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(get_my_session_bp)
    app.register_blueprint(create_session_at_home_bp)

    app.register_blueprint(profile_bp)
    app.register_blueprint(get_my_question_bp)

    app.register_blueprint(session_bp)
    app.register_blueprint(get_session_info_bp)
    app.register_blueprint(pass_session_lock_bp)
    app.register_blueprint(get_previous_category_bp)
    app.register_blueprint(refine_text_bp)
    app.register_blueprint(get_category_questions_bp)

    return app
