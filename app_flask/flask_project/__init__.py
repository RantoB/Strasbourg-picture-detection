from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_project.config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from flask_project.main.routes import main
    from flask_project.pages.routes import pages
    from flask_project.errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(pages)
    app.register_blueprint(errors)

    return app
