from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, SelectField, DateTimeField, validators, SelectMultipleField
from wtforms.validators import InputRequired, Length, ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_admin.form.widgets import Select2Widget
from .models import Venues, Shows, User
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

    street = LowercaseStringField(
        'Street', validators=[InputRequired(), Length(min=3, max=256)])
    city = LowercaseStringField(
        'City', validators=[InputRequired(), Length(min=3, max=256)])
    state = LowercaseStringField(
        'State', validators=[InputRequired(), Length(min=3, max=256)])
    tags = LowercaseStringField('tags', validators=[InputRequired()])

# custom validator to check is venue name exist in databse


def validate_venue_name(self, venue_name):
    venue = Venues.query.filter_by(venue_name=venue_name.data).first()
    if not venue:
        raise ValidationError('Invalid venue name.')


class ShowForm(FlaskForm):

    show_name = LowercaseStringField('Show Name', validators=[InputRequired(), Length(min=3, max=256)])
    venue_name = SelectMultipleField('Venue Name', coerce=str , choices=[], option_widget=CheckboxInput(), 
                                     widget=ListWidget())
    ticket_price = IntegerField('Ticket Price', validators=[InputRequired()])
    release_date = StringField('Release Date', validators=[
                               InputRequired(), Length(min=3, max=256)])
    rating = DecimalField('Ratings', places=2, validators=[InputRequired()])
    tags = LowercaseStringField(
        'Tags', validators=[InputRequired(), Length(min=3, max=256)])
    show_description = LowercaseStringField('Show Description', validators=[
                                      InputRequired(), Length(min=3, max=1024)])
    cast = LowercaseStringField('Cast')
    poster_link = StringField('Poster Link')


"""
venue_name= QuerySelectField(query_factory=lambda: models.Venues.query.all(),
                           widget=Select2Widget())
"""