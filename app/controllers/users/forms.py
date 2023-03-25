from datetime import date
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, Length, ValidationError
from ..admin.admin_forms import LowercaseStringField
from werkzeug.security import check_password_hash
from ...models.models import User, TicketsBooked, Venues, Shows
from sqlalchemy.sql import func
from ... import db

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


class SearchForm(FlaskForm):
    search = StringField('Search')
    submit = SubmitField('Search')

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


def ticket_avialable(form, field):
    if field.data > 0:
        # uses class method current_total_bookings from TciektsBooked class
        current_total_bookings = TicketsBooked.current_total_bookings(form.showname.data, form.venuename.data)
        # Returns the total capacity of the venue
        # for each show in venue, full capacity of venue is alloted
        venue_capacity = Venues.venue_capacity(form.venuename.data)
        # calculates the tickets remaining 
        ticket_remaining = venue_capacity - current_total_bookings
        if ticket_remaining < field.data:
            #  Raises a validation error if user is booking tickets greater than number of tickets left
            raise ValidationError("Only " + str(ticket_remaining) + " tickets are remaning")
    else:
         raise ValidationError("Less than 1 tickets cannot be booked!")

def get_venue_choices(showname):
     venues = Shows.query.filter_by(show_name=showname).first()
     venue_list = venues.venue_name.split(',')

     venue_choices = [(venue) for venue in venue_list]
     return venue_choices

class BookShowForm(FlaskForm):
    username = LowercaseStringField('Enter Your Username', validators=[InputRequired(), verify_user], render_kw={"placeholder":"enter your username"})
    # Showname is prefilled with than show that user has clicked on
    showname=LowercaseStringField("Show name", validators=[InputRequired()])
    # For each Show, venuename gives options for the user to select one of the given venues
    venuename = SelectField("venue name", choices=[], validators=[InputRequired()])
    totaltickets=IntegerField("Total tickets", validators=[InputRequired(), ticket_avialable])
    show_date = DateField("Date of reservation", validators=[InputRequired()])


    # password = PasswordField("Password", validators=[InputRequired()], render_kw={"placehold":"password"})

    
    

