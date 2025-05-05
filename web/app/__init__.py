from flask import Flask
from app.views.index import index_bp
from app.views.register import register_bp
from app.views.home import home_bp
from app.views.history import history_bp
from app.views.session import session_bp
from app.util.login import login_bp, makename_bp, signup_bp, tempkey_bp

def create_app():
    app = Flask(__name__)
    #페이지 제공 라우트
    app.register_blueprint(index_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(session_bp)
    #로그인
    app.register_blueprint(login_bp)
    #회원가입
    app.register_blueprint(makename_bp)
    app.register_blueprint(signup_bp)
    #회원확인
    app.register_blueprint(tempkey_bp)

    return app
