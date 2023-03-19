from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from .admin_forms import LowercaseStringField
from werkzeug.security import check_password_hash
from .models import User, TicketsBooked, Venues
from sqlalchemy.sql import func
from . import db

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=150)])
    remember = BooleanField('remember me')


class RegistrationForm(FlaskForm):

    first_name = StringField('first name', validators=[
                             InputRequired(), Length(min=4, max=16)])

    last_name = StringField('last name', validators=[
                            InputRequired(), Length(min=4, max=16)])

    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])

    email = StringField('email', validators=[InputRequired(), Email(
        message='Invalid Email'), Length(max=80)])

    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80), EqualTo('cpassword', message='Passwords don\'t match')])
    cpassword = PasswordField('Confirm password', validators=[
                             InputRequired(), Length(min=8, max=80)])


def check_password(form, field):
        user = User.query.get_or_404(form.username)
        if not check_password_hash(field.data, user.password):
            raise ValidationError("Incorrect Password")
        
def verify_user(form, field):
     user = User.query.filter_by(username=field.data).first()
     if not user:
          raise ValidationError("user does not exist")


def get_total_tickets_booked(show_name, venue_name):
    total_tickets_booked = TicketsBooked.query.with_entities(db.func.sum(
        TicketsBooked.totalticket)).filter_by(showname=show_name, venuename=venue_name).scalar()
    if total_tickets_booked:
        return total_tickets_booked
    else:
         return 0
def ticket_avialable(form, field):
    current_total_bookings = TicketsBooked.current_total_bookings(form.showname.data, form.venuename.data)
    # venue = Venues.query.filter_by(venue_name=form.venuename.data).first()
    venue_capacity = Venues.venue_capacity
    # venue_capacity = venue.capacity
    ticket_remaining = int(venue_capacity) - int(current_total_bookings)
    if ticket_remaining < field.data:
         raise ValidationError("Only " + str(ticket_remaining) + " tickets are remaning")


class BookShowForm(FlaskForm):
    username = LowercaseStringField('Enter Your Username', validators=[InputRequired(), verify_user], render_kw={"placeholder":"enter your username"})
    showname=LowercaseStringField("Show name", validators=[InputRequired()])
    venuename = LowercaseStringField("venue name", validators=[InputRequired()])
    totaltickets=IntegerField("Total tickets", validators=[InputRequired(), ticket_avialable])
    show_date = DateField("Date of reservation", validators=[InputRequired()])
    # password = PasswordField("Password", validators=[InputRequired()], render_kw={"placehold":"password"})

    
    

