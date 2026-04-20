from flask import Flask
from .config import Config
from .extensions import db, login_manager, csrf, socketio
from .routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    csrf.init_app(app)

    socketio.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id: str):
        try:
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    register_blueprints(app)

    from .sockets import register_socket_handlers
    register_socket_handlers()

    with app.app_context():
        db.create_all()

    return app