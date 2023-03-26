from flask import Blueprint, Flask, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from ... import db, csrf
import os
from flask_bootstrap import Bootstrap
from ...models.models import Venues, Shows, User
from .admin_forms import VenueForm, ShowForm
from werkzeug.utils import secure_filename
from flask_restful import Api
from ...resources.shows.ShowsApi import ShowAPI
from ...resources.venues.venueapi import VenueApi
from ..auth import admin_required
import requests


admin_controls = Blueprint('admin_controllers', __name__, url_prefix='/admin')
# url_prefix='/admin'
admin_apis = Api(admin_controls)
bootstrap = Bootstrap()


@admin_controls.route("/", methods=['GET', 'POST'])
@admin_required
@login_required
def adminhome():
    users = User.query.all()
    return render_template("admin/admin_index.html.jinja2", users=users)


"""
##############################################
venue manager
##############################################
"""

admin_apis.add_resource(VenueApi, '/api/v1/venues/')


@admin_controls.route("/venue_mgmt", methods=['GET', 'POST'])
@admin_required
@login_required
def venue_mgmt():
    # http://127.0.0.1:5000/api/shows
    # response = requests.get("http://127.0.0.1:5000/admin/api/v1/venues")

    venues = Venues.query.all()
    return render_template("admin/venues/venuemgmt.html.jinja2", venues=venues)


@admin_controls.route('/create_venue', methods=['GET', 'POST'])
@admin_required
@login_required
def create_venue():
    add_venue = VenueForm()
    if add_venue.validate_on_submit():
        new_venue = Venues(
            venue_name=add_venue.venue_name.data,
            capacity=add_venue.capacity.data,
            street=add_venue.street.data,
            city=add_venue.city.data,
            state=add_venue.state.data,
            venue_tags=add_venue.tags.data
        )
        db.session.add(new_venue)
        db.session.commit()

        flash('Venue created successfully!')

        return redirect(url_for('admin_controllers.venue_mgmt'))

    return render_template('admin/venues/addvenueform.html.jinja2', form=add_venue)


@admin_controls.route('/edit_venue/<venue_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_venue(venue_id):
    venue = Venues.query.get_or_404(venue_id)
    edit_form = VenueForm(obj=venue)
    if edit_form.validate_on_submit():
        edit_form.populate_obj(venue)
        db.session.commit()
        return redirect(url_for('admin_controllers.venue_mgmt'))

    return render_template('admin/venues/venue_edit_form.html.jinja2', form=edit_form)


@admin_controls.route('/delete_venue/<venue_id>', methods=['GET', 'POST'])
@admin_required
@login_required
@csrf.exempt
def delete_venue(venue_id):
    try:
        venue = Venues.query.get_or_404(venue_id)
        db.session.delete(venue)
        db.session.commit()

        return redirect(url_for('admin_controllers.venue_mgmt'))
    except:
        db.session.rollback()
        return redirect(url_for('admin_controllers.venue_mgmt'))


"""# ###########################################
# show manager
#########################################"""
"""_summary_
    testing shows api
    Returns:
        json: working status , ok , 200
"""

admin_apis.add_resource(ShowAPI, '/api/v1/shows/<int:show_id>')


@admin_controls.route("/show_mgmt", methods=['GET', 'POST'])
@admin_required
@login_required
def show_mgmt():
    shows = Shows.query.all()
    return render_template("admin/shows/showmgmt.html.jinja2", shows=shows)


@admin_controls.route("/add_show", methods=['GET', 'POST'])
@admin_required
@login_required
def add_show():
    addshow_form = ShowForm()
    addshow_form.venue_name.choices = [
        (venue.venue_name) for venue in Venues.query.all()]
    if addshow_form.validate_on_submit():
        venue_name = ",".join(addshow_form.venue_name.data)

        poster = addshow_form.poster_file.data
        postername = secure_filename(poster.filename)
        if poster:            
            poster.save(os.path.join('app/static/images', postername))
        new_show = Shows(
            show_name=addshow_form.show_name.data,
            venue_name=venue_name,
            ticket_price=addshow_form.ticket_price.data,
            premiere_date=addshow_form.premiere_date.data,
            rating=addshow_form.rating.data,
            tags=addshow_form.tags.data,
            show_description=addshow_form.show_description.data,
            cast=addshow_form.cast.data,
            poster_filename=postername
        )
        db.session.add(new_show)
        db.session.commit()
        return redirect(url_for("admin_controllers.show_mgmt"))
    return render_template("admin/shows/addshowform.html.jinja2", form=addshow_form)


@admin_controls.route('/edit_show/<int:show_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_show(show_id):
    show = Shows.query.get_or_404(show_id)
    form = ShowForm(obj=show)
    form.venue_name.choices = [(venue.venue_name)
                               for venue in Venues.query.all()]
    if form.validate_on_submit():
        poster = form.poster_file.data
        
        if poster:
            postername = secure_filename(poster.filename)
            poster.save(os.path.join('app/static/images', postername))
        form.populate_obj(show)
        show.venue_name = ",".join(form.venue_name.data)
        show.poster_filename=postername
        db.session.commit()
        return redirect(url_for('admin_controllers.show_mgmt'))

    return render_template('admin/shows/edit_show.html.jinja2', form=form, show=show)


@admin_controls.route('/delete_show/<int:show_id>', methods=['DELETE', 'POST'])
@admin_required
@login_required
def delete_show(show_id):
    show = Shows.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('admin_controllers.show_mgmt'))
