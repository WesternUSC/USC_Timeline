import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'p6Jtit8o7h6M5tM7MtyAs4o46JiPm683'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['UPLOAD_EXTENSIONS'] = ['.png', 'jpg', '.jpeg', '.svg']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail(app)

from usctimeline.users.routes import users
from usctimeline.events.routes import events
from usctimeline.categories.routes import categories
from usctimeline.tags.routes import tags
from usctimeline.main.routes import main

app.register_blueprint(users)
app.register_blueprint(events)
app.register_blueprint(categories)
app.register_blueprint(tags)
app.register_blueprint(main)
