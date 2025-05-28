from flask import Flask
from app.views.index import index_bp
from app.views.register import register_bp
from app.views.home import home_bp
from app.views.history import history_bp
from app.views.session import session_bp
from app.api.authorize import userChecking_bp, login_bp, logout_bp, makename_bp, signup_bp
from app.api.search import mySession_bp, myQuestion_bp
from app.api.room import createSession_bp, joinSession_bp, sendtoLLM_bp

def create_app():
    app = Flask(__name__)
    #페이지 제공 라우트
    app.register_blueprint(index_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(session_bp)
    #authorize
    app.register_blueprint(userChecking_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(logout_bp)
    app.register_blueprint(makename_bp)
    app.register_blueprint(signup_bp)
    #search
    app.register_blueprint(mySession_bp)
    app.register_blueprint(myQuestion_bp)
    #session
    app.register_blueprint(createSession_bp)
    app.register_blueprint(joinSession_bp)
    app.register_blueprint(sendtoLLM_bp)

    return app
