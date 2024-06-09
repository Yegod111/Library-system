from .config import app
from .controllers import register_blueprints

def create_app():
    register_blueprints(app)
    return app
