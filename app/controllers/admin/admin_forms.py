from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, DateField, SelectField, DateTimeField, validators, SelectMultipleField, PasswordField, BooleanField, FileField
from wtforms.validators import InputRequired, Length, NumberRange,ValidationError
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from flask_admin.form.widgets import Select2Widget
from ...models.models import Venues, Shows, User
from ... import db


class LowercaseStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].lower().strip()
        else:
            self.data = ''


class AdminLoginForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=16)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=150)])
    remember = BooleanField('remember me')


class VenueForm(FlaskForm):
    venue_name = LowercaseStringField('venue name', validators=[
        InputRequired(), Length(min=3, max=256)])

    capacity = IntegerField('capacity', validators=[InputRequired()])

    street = LowercaseStringField(
        'Street', validators=[InputRequired(), Length(min=3, max=256)])
    city = LowercaseStringField(
        'City', validators=[InputRequired(), Length(min=3, max=256)])
    state = LowercaseStringField(
        'state', validators=[InputRequired(), Length(min=3, max=256)])
    venue_tags = LowercaseStringField('tags', validators=[InputRequired()])

# custom validator to check is venue name exist in databse


def validate_venue_name(self, venue_name):
    venue = Venues.query.filter_by(venue_name=venue_name.data).first()
    if not venue:
        raise ValidationError('Invalid venue name.')

def validate_show_name(form, field):
    show = Shows.query.filter_by(show_name=field.data).first()
    if show:
        raise ValidationError("show with same name already exists")

class ShowForm(FlaskForm):

    show_name = LowercaseStringField('Show Name', validators=[
                                     InputRequired(), Length(min=3, max=256)])
    venues = SelectMultipleField('Venue Name', coerce=str, choices=[], option_widget=CheckboxInput(),
                                     widget=ListWidget())
    ticket_price = DecimalField('Ticket Price', validators=[InputRequired()])
    premiere_date = DateField('Premiere Date', validators=[
        InputRequired()], render_kw={"placeholder": "add date in dd-mm-YYYY format"})
    end_date = DateField('End Date', validators=[
        InputRequired()], render_kw={"placeholder": "add date in dd-mm-YYYY format"})
    rating = DecimalField('Ratings', places=2, validators=[InputRequired(), NumberRange(min=1, max=10, message="ratings has to be in a range between 1 to 10")],
                           render_kw={"placeholder": "add ratings from 1 to 10"})
    tags = LowercaseStringField(
        'Tags', validators=[InputRequired(), Length(min=3, max=256)])
    show_description = LowercaseStringField('Show Description', validators=[
        InputRequired(), Length(min=3, max=1024)])
    cast = LowercaseStringField('Cast')
    poster_file = FileField('Poster file')


"""
venue_name= QuerySelectField(query_factory=lambda: models.Venues.query.all(),
                           widget=Select2Widget())
"""
