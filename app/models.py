from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False)

    def get_id(self):
        return self.user_id

class Shows(db.Model):
    __tablename__ = "shows"
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String(150), unique=True, nullable=False)
    release_date = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Numeric(precision=2, scale=1))
    tags = db.Column(db.String)
    show_description = db.Column(db.String)
    cast = db.Column(db.String)
    poster_link = db.Column(db.String)

