from flask import Blueprint, Flask, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from ... import db, csrf
import os
from flask_bootstrap import Bootstrap
from ...models.models import Venues, Shows, User, ShowsInVenues
from .admin_forms import VenueForm, ShowForm
from werkzeug.utils import secure_filename
from flask_restful import Api
from ...resources.shows.ShowsApi import ShowAPI
from ...resources.venues.venueapi import VenueApi
from ..auth import admin_required
from flask import current_app


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
    venues = []
    for show in shows:
        venue_shows = ShowsInVenues.query.filter_by(show_id=show.show_id).all()
        current_app.logger.info(venue_shows)
        for venue_show in venue_shows:
            venue = Venues.query.filter_by(venue_id=venue_show.venue_id).first()
            venues.append(str(venue.venue_name))
    current_app.logger.info(venues)
    return render_template("admin/shows/showmgmt.html.jinja2", shows=shows, venues=venues)


@admin_controls.route("/add_show", methods=['GET', 'POST'])
@admin_required
@login_required
def add_show():
    addshow_form = ShowForm()
    addshow_form.venues.choices = [(venue.venue_name)
                                   for venue in Venues.query.all()]
    if addshow_form.validate_on_submit():   

        poster = addshow_form.poster_file.data
        postername = secure_filename(poster.filename)
        if poster:
            poster.save(os.path.join('app/static/images', postername))
        new_show = Shows(
            show_name=addshow_form.show_name.data,
            ticket_price=addshow_form.ticket_price.data,
            premiere_date=addshow_form.premiere_date.data,
            end_date=addshow_form.end_date.data,
            rating=addshow_form.rating.data,
            tags=addshow_form.tags.data,
            show_description=addshow_form.show_description.data,
            cast=addshow_form.cast.data,
            poster_filename=postername
        )

        db.session.add(new_show)
        db.session.commit()
        for venue_name in addshow_form.venues.data:
            venue = Venues.query.filter_by(venue_name=venue_name).first()
            new_show_in_venue = ShowsInVenues(
                show_id=new_show.show_id,
                venue_id=venue.venue_id,
            )
            db.session.add(new_show_in_venue)
            db.session.commit()
        return redirect(url_for("admin_controllers.show_mgmt"))
    return render_template("admin/shows/addshowform.html.jinja2", form=addshow_form)


@admin_controls.route('/edit_show/<int:show_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit_show(show_id):
    show = Shows.query.get_or_404(show_id)
    form = ShowForm(obj=show)
    form.venues.choices = [(venue.venue_name)
                           for venue in Venues.query.all()]
    if form.validate_on_submit():
        poster = form.poster_file.data
        postername = secure_filename(poster.filename)
        if poster:

            poster.save(os.path.join('app/static/images', postername))
        form.populate_obj(show)
        # show.venue_name = ",".join(form.venue_name.data)
        show.poster_filename = postername

        db.session.commit()
        venue_id_list = [show_in_venue.venue_id for show_in_venue in ShowsInVenues.query.filter_by(show_id=show.show_id)]
        """venue_id_list is the list of all venues that were allocated while creating the show"""
        current_app.logger.info("venue_id_list")
        current_app.logger.info(venue_id_list)

        venue_ids = [] 
        """A list of all venues that admin is passing through the edit show form"""
        for venue_name in form.venues.data:
            venue = Venues.query.filter_by(venue_name=venue_name).first()
            venue_ids.append(venue.venue_id) # appends all the venue_id in venue_ids


        for venue_name in form.venues.data: # venues passed by user
            
            current_app.logger.info("venue_ids")
            current_app.logger.info(venue_ids)
            venue = Venues.query.filter_by(venue_name=venue_name).first()
            for venue_id in venue_id_list:
                current_app.logger.info(venue_id)
                current_app.logger.info(venue.venue_id)
                if venue_id not in venue_ids:
                    row_to_delete = ShowsInVenues.query.filter_by(show_id=show.show_id, venue_id=venue_id).first()
                    current_app.logger.info(row_to_delete)
                    if row_to_delete:
                        db.session.delete(row_to_delete)
                        db.session.commit()
                        break
            if venue.venue_id not in venue_id_list:
                new_show_in_venue = ShowsInVenues(
                    show_id=show.show_id,
                    venue_id=venue.venue_id
                )
                db.session.add(new_show_in_venue)
                db.session.commit()
                venue_id_list.append(venue.venue_id)

            # current_app.logger.info(venue_id)
            current_app.logger.info("venue.venue_id")

            current_app.logger.info(venue.venue_id)
            # if venue_id != venue.venue_id:
                # rows_to_delete = ShowsInVenues.query.filter_by(
                #     show_id=show_id, venue_id=venue_id)
                # db.session.delete(rows_to_delete)
                # db.session.commit()

            # if venue_id != venue.venue_id:
            #     new_show_in_venue = ShowsInVenues(
            #         show_id=show.show_id,
            #         venue_id=venue.venue_id
            #     )
            #         db.session.add(new_show_in_venue)
            #         db.session.commit()

                
                    

        return redirect(url_for('admin_controllers.show_mgmt'))

    return render_template('admin/shows/edit_show.html.jinja2', form=form, show=show)


@admin_controls.route('/delete_show/<int:show_id>', methods=['DELETE', 'POST'])
@admin_required
@login_required
# @csrf.exempt
def delete_show(show_id):
    show = Shows.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()
    return redirect(url_for('admin_controllers.show_mgmt'))
