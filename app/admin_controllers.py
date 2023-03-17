from crypt import methods
from dataclasses import dataclass
from flask import Blueprint, Flask, render_template, url_for, redirect, flash
from . import db
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Email, Length, DataRequired
from .models import Venues, Shows, Shows_in_Venues, User

admin_controls = Blueprint('admin_controllers', __name__, url_prefix='/admin')
# url_prefix='/admin'
bootstrap = Bootstrap()


class AddVenue(FlaskForm):
    venue_name = StringField('venue name', validators=[
                             InputRequired(), Length(min=3, max=256)])

    capacity = IntegerField('capacity', validators=[InputRequired()])
    location = StringField('location', validators=[
                           InputRequired(), Length(min=8, max=256)])
    tags = StringField('tags', validators=[InputRequired()])


class AddShow(FlaskForm):
    show_name = StringField('Show Name', validators=[
                            InputRequired(), Length(min=3, max=256)])
    release_date = StringField('Release Date', validators=[
                               InputRequired(), Length(min=3, max=256)])
    rating = DecimalField('Ratings', places=2,validators=[InputRequired()])
    tags = StringField('Tags', validators=[
                       InputRequired(), Length(min=3, max=256)])
    show_descp = StringField('Show Description', validators=[
                             InputRequired(), Length(min=3, max=1024)])
    cast = StringField('Cast')
    poster_link = StringField('Poster Link')


class ShowForm(FlaskForm):
    show_name = StringField('Show Name', validators=[
                            DataRequired(), Length(max=150)])
    release_date = StringField('Release Date', validators=[
                               DataRequired(), Length(max=150)])
    rating = DecimalField('Rating', places=1)
    tags = StringField('Tags')
    show_description = StringField('Show Description')
    cast = StringField('Cast')
    poster_link = StringField('Poster Link')


@admin_controls.route("/", methods=['GET', 'POST'])
def adminhome():
    users = User.query.all()
    return render_template("admin/admin_index.html.jinja2", users=users)

"""
##############################################
venue manager
##############################################
"""

@admin_controls.route("/venue_mgmt", methods=['GET', 'POST'])
def venue_mgmt():
    venues = Venues.query.all()
    return render_template("admin/venuemgmt.html.jinja2", venues=venues)


@admin_controls.route('/create_venue', methods=['GET', 'POST'])
def create_venue():
    add_venue = AddVenue()
    if add_venue.validate_on_submit():
        new_venue = Venues(
            venue_name=add_venue.venue_name.data,
            capacity=add_venue.capacity.data,
            location=add_venue.location.data,
            venue_tags=add_venue.tags.data
        )
        db.session.add(new_venue)
        db.session.commit()

        flash('Venue created successfully!')

        return redirect(url_for('admin_controllers.venue_mgmt'))

    return render_template('admin/addvenueform.html.jinja2', form=add_venue)

"""# ###########################################
# show manager
#########################################"""

@admin_controls.route("/show_mgmt", methods=['GET', 'POST'])
def show_mgmt():
    shows = Shows.query.all()
    return render_template("admin/showmgmt.html.jinja2", shows=shows)


@admin_controls.route("/add_show", methods=['GET', 'POST'])
def add_show():
    addshow_form = AddShow()
    if addshow_form.validate_on_submit():
        new_show = Shows(
            show_name=addshow_form.show_name.data,
            release_date=addshow_form.release_date.data,
            rating=addshow_form.rating.data,
            tags=addshow_form.tags.data,
            show_description=addshow_form.show_descp.data,
            cast=addshow_form.cast.data,
            poster_link=addshow_form.poster_link.data
        )
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin_controllers.show_mgmt"))
    return render_template("admin/addshowform.html.jinja2", form=addshow_form)


@admin_controls.route('/edit_show/<int:show_id>', methods=['GET', 'POST'])
def edit_show(show_id):
    show = Shows.query.get_or_404(show_id)
    form = ShowForm(obj=show)
    if form.validate_on_submit():
        form.populate_obj(show)
        db.session.commit()
        return redirect(url_for('admin_controllers.show_mgmt'))

    return render_template('admin/edit_show.html.jinja2', form=form, show=show)


@admin_controls.route('/delete_show/<int:show_id>', methods=['DELETE', 'POST'])
def delete_show(show_id):
    show = Shows.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('admin_controllers.show_mgmt'))
