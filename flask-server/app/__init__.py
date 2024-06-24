# flask-server/app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Set up logging
    if not app.debug:
        handler = logging.StreamHandler()
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)
    else:
        logging.basicConfig(level=logging.DEBUG)

    with app.app_context():
        # Import parts of our application
        from . import routes, models

        return app
