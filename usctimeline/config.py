import os
import json


class Config:
    """Stores configuration information for creating Flask app."""
    with open('etc/config.json') as file:
        config = json.load(file)
    SECRET_KEY = config.get('FLASK_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = config.get("MAIL_SERVER")
    MAIL_PORT = config.get("MAIL_PORT")
    MAIL_USE_TLS = True
    MAIL_USERNAME = config.get('EMAIL_USERNAME')
    MAIL_PASSWORD = config.get('EMAIL_PASSWORD')
