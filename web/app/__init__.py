from flask import Flask
from app.views.index import index_bp
from app.views.register import register_bp
from app.views.home import home_bp
from app.views.history import history_bp
from app.views.session import session_bp
from app.util.login import login_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(index_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(login_bp)

    with app.app_context():
        print(app.url_map)

    return app
