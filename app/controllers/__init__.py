from .admin_controller import admin_bp
from .auth_controller import auth_bp
from .main_controller import main_bp
from .user_controller import user_bp

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
