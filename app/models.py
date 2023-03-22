from email.policy import default
from sqlalchemy.sql import func
from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cpassword = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150),unique=True, nullable=False)
    isadmin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.user_id
    def get_username(self):
        return self.username
    def get_isAdmin(self):
        return self.isadmin


class Shows(db.Model):
    __tablename__ = "shows"
    show_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    show_name = db.Column(db.String, unique=True, nullable=False)
    venue_name = db.Column(db.String, db.ForeignKey('venues.venue_name'), nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)
    release_date = db.Column(db.String, nullable=False)
    rating = db.Column(db.Numeric(precision=2, scale=1))
    tags = db.Column(db.String)
    show_description = db.Column(db.String)
    cast = db.Column(db.String)
    poster_link = db.Column(db.String)
    venue = db.relationship('Venues', backref=db.backref('shows', lazy=True))

    
    def get_id(self):
        return self.show_id

class Admin(db.Model, UserMixin):
    __tablename__ = "admin"
    admin_id = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)


class Venues(db.Model):
    __tablename__ = "venues"
    venue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name = db.Column(db.String(150), unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    street = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(150), nullable=False)
    State = db.Column(db.String(150), nullable=False)
    venue_tags = db.Column(db.String(150))

    def venue_capacity(venue_name):
        venue = Venues.query.filter_by(venue_name=venue_name).first()
        print(venue)
        if venue:
            return venue.capacity
        else:
            return 0
    
class TicketsBooked(db.Model):
    __tablename__="ticket_booked"
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, db.ForeignKey('user.username'),nullable=False)
    showname = db.Column(db.String, db.ForeignKey('shows.show_name'), nullable=False)
    venuename = db.Column(db.String, db.ForeignKey('venues.venue_name'), nullable=False)
    totalticket = db.Column(db.Integer, nullable=False)
    show_date = db.Column(db.Date, nullable=False)
    
    def current_total_bookings(show_name, venue_name):
        current_total_bookings = db.session.query(func.sum(TicketsBooked.totalticket)).filter_by(
            showname=show_name, venuename=venue_name).scalar()
        if current_total_bookings:
            return current_total_bookings
        else:
            return 0
    

