from flask import Flask

from .config import Config
from .extensions import db


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from .main.routes import bp as main_bp

    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
