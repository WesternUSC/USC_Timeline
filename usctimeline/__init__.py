from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from usctimeline.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    """Initializes a new Flask app.

    Initializes a new Flask app with provided configurations. Initializes
    database, bcrypt, login_manager and mail. Registers users, events, tags,
    main, and errors modules (blueprints).

    Args:
        config_class:
            Config class instance storing various configurations for
            initializing this Flask app. (see config.py)

    Returns:
        An instance of Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from usctimeline.users.routes import users
    from usctimeline.events.routes import events
    from usctimeline.tags.routes import tags
    from usctimeline.main.routes import main
    from usctimeline.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(events)
    app.register_blueprint(tags)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
