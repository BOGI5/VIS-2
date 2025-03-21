from app import db
from app import login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=True)
    tokens = db.Column(db.Text)

class Customer(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    family_status = db.Column(db.String(50), nullable=False)
    income = db.Column(db.Float, nullable=False)
    egn = db.Column(db.String(10), nullable=False)
    credit_expire = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    job = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

