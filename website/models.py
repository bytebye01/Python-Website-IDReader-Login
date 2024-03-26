from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    notes = db.relationship('Note')
    role = db.Column(db.String(50), default='user')


class IDCard(db.Model):
    id_number = db.Column(db.String(20), primary_key=True, unique=True)
    thai_name = db.Column(db.String(100))
    english_name = db.Column(db.String(100))
    gender = db.Column(db.String(20))
    date_of_birth = db.Column(db.String(20))
    age = db.Column(db.String(10))
    religion = db.Column(db.String(50))
    address = db.Column(db.String(200))
    issuer = db.Column(db.String(50))
    date_of_issue = db.Column(db.String(20))
    date_of_expiry = db.Column(db.String(20))
    photo_base64 = db.Column(db.Text)