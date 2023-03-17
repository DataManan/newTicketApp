from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150),unique=True, nullable=False)

    def get_id(self):
        return self.user_id
    def get_username(self):
        return self.username


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
    
    def get_id(self):
        return self.show_id

class Admin(db.Model):
    __tablename__ = "admin"
    admin_id = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Venues(db.Model):
    __tablename__ = "venues"
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String(150), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    venue_tags = db.Column(db.String)


class Shows_in_Venues(db.Model):
    __tablename__ = "shows_in_venues"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(150), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.show_id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)
    show = db.relationship('Shows', backref=db.backref('shows_in_venues', lazy=True))
    venue = db.relationship('Venues', backref=db.backref('shows_in_venues', lazy=True))

    column_labels = {
        'show_id': 'Show',
        'venue_id': 'Venue',
    }
