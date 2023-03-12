from crypt import methods
from dataclasses import dataclass
from tokenize import String
from flask import Blueprint, render_template, url_for, redirect, current_app
from . import db
from flask_admin import Admin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from .models import Venues

admin_controls = Blueprint('admin_controllers', __name__)


class AddVenue(FlaskForm):
    venue_name = StringField('venue name', validators=[
                             InputRequired(), Length(min=3, max=256)])
    cpacity = IntegerField('capacity', validators=[InputRequired()])
    location = StringField('location', validators=[
                           InputRequired(), Length(min=8, max=256)])
    tags = StringField('tags', validators=[InputRequired()])


@admin_controls.route("/venue_mgmt")
def venues():
    
    return render_template("venuemgmt.html.jinja2")


@admin_controls.route('/create_venue', methods=['GET', 'POST'])
def create_venue():
    add_venue = AddVenue()
    if add_venue.validate_on_submit():
        new_venue = Venues(
            venue_name = add_venue.venue_name.data,
            capacity = add_venue.capacity.data,
            location = add_venue.location.data,
            venue_tags = add_venue.tags.data
        )
        db.session.add(new_venue)
        db.session.commit()

        return redirect(url_for('admin_controls.venues'))
    return render_template('add_venue.html.jinja2', form=add_venue)
