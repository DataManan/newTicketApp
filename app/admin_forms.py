# from random import choices
from datetime import date
from flask_wtf import FlaskForm
# from flask import current_app as app
from wtforms import StringField, IntegerField, DecimalField, DateField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, ValidationError, Regexp
from .models import Venues, Shows, Shows_in_Venues, User
from . import db


class LowercaseStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].lower()
        else:
            self.data = ''


class VenueForm(FlaskForm):
    venue_name = LowercaseStringField('venue name', validators=[
        InputRequired(), Length(min=3, max=256)])

    capacity = IntegerField('capacity', validators=[InputRequired()])
    location = LowercaseStringField('location', validators=[
        InputRequired(), Length(min=8, max=256)])
    tags = LowercaseStringField('tags', validators=[InputRequired()])

# custom validator to check is venue name exist in databse


def validate_venue_name(self, venue_name):
    venue = Venues.query.filter_by(venue_name=venue_name.data).first()
    if not venue:
        raise ValidationError('Invalid venue name.')
    

def DateNotInFuture(form, field):
    if field.data > date.today():
        raise ValidationError('Date cannot be in the future.')

class ShowForm(FlaskForm):

    # print(venues_list)
    show_name = LowercaseStringField('Show Name', validators=[
        InputRequired(), Length(min=3, max=256)])
    
    venue_name = SelectField('Venue Name', choices=[], validators=[InputRequired(), Length(min=3, max=256), validate_venue_name])

    release_date = StringField('Release Date', validators=[InputRequired(), Length(min=3, max=256)])
    

    rating = DecimalField('Ratings', places=2, validators=[InputRequired()])
    tags = LowercaseStringField('Tags', validators=[
        InputRequired(), Length(min=3, max=256)])
    show_descp = LowercaseStringField('Show Description', validators=[
        InputRequired(), Length(min=3, max=1024)])
    cast = LowercaseStringField('Cast')
    poster_link = StringField('Poster Link')

    
