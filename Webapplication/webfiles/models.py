from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class CryptoCurrentInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_type = db.Column(db.String(3))
    current_price = db.Column(db.Float)
    date = db.Column(db.String(180))


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coin_type = db.Column(db.String(3))
    paid = db.Column(db.Integer)
    price_when_purchased = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    profit = db.Column(db.Float, nullable=True)
    purchases = db.relationship('Purchase')


class Authentication(db.Model, UserMixin):
    api_key = db.Column(db.String, primary_key=True)
