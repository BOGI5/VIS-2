from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize extensions
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth'
login_manager.session_protection = 'strong'

from app.models.user import User
with app.app_context():
    db.create_all()


from app.controllers import auth