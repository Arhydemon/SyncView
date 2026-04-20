from .pages import bp as pages_bp
from .errors import bp as errors_bp
from .auth import bp as auth_bp
from .rooms import bp as rooms_bp
from .uploads import bp as uploads_bp

def register_blueprints(app):
    app.register_blueprint(pages_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(errors_bp)