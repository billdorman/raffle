from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_apscheduler import APScheduler

db = SQLAlchemy(session_options={"expire_on_commit": False})
ma = Marshmallow()
jwt = JWTManager()
login_manager = LoginManager()
scheduler = APScheduler()


@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    return User.query.get(user_id)
