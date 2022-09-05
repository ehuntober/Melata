from app import db
from random import choices
from datetime import datetime
import string
from flask_login import UserMixin


def shorten():

    characters = string.digits + string.ascii_letters
    short = ''.join(choices(characters, k=3))
    link1 = Userlink.query.filter_by(short_url=short).first()
    link2 = Guestlink.query.filter_by(short_url=short).first()

    if link1 or link2:
        shorten()
    return short

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100))
    email = db.Column(db.Text)
    password = db.Column(db.String(100))
    links = db.relationship('Userlink', backref='user')

    def __repr__(self):
        return f'<User "{self.name}">'


class Userlink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(100))
    visits = db.Column(db.Integer, default = 0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def shortened(self):
        raise AttributeError('short url is not readable attribute')

    @shortened.setter
    def shortened(self, text):
        self.short_url = shorten()

    def __repr__(self):
        return f'<Userlink "{str(self.original_url)}">'


class Guestlink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_url = db.Column(db.String(100))

    @property
    def shortened(self):
        raise AttributeError('short url is not readable attribute')

    @shortened.setter
    def shortened(self, text):
        self.short_url = shorten()

    def __repr__(self):
        return f'<Guestlink "{str(self.original_url)}">'