from flask import Blueprint, json, redirect, render_template, flash, jsonify
from flask_login import login_required, current_user
from ...models.models import Shows, User, TicketsBooked
from .forms import BookShowForm, get_venue_choices
from ... import db
from sqlalchemy import or_, true
from ...resources.shows.ShowsApi import ShowsAPI
from flask_restful import Api
import requests

controllers = Blueprint('controllers', __name__)

Uapi = Api(controllers)
Uapi.add_resource(ShowsAPI, "/api/shows")


@controllers.route('/')
def index():

    # response = requests.get("http://127.0.0.1:5000/api/shows")
    shows = Shows.query.order_by(Shows.show_id.desc()).all()
    shows
    return render_template('user/index.html.jinja2', SHOWS=shows, current_user=current_user)


@controllers.route("/book_tickets/<show_id>")
@login_required
def book_tickets(show_id):
    show = Shows.query.filter_by(show_id=show_id).first()
    return render_template("user/booking/bookshow.html.jinja2", show=show)


@controllers.route("/booknow/<show_id>", methods=['GET', 'POST'])
@login_required
def booknow(show_id):
    form = BookShowForm()
    show = Shows.query.get_or_404(show_id)
    form.username.data = current_user.username
    form.showname.data = show.show_name
    form.venuename.choices = get_venue_choices(show_id)
    if form.validate_on_submit():
        new_booking = TicketsBooked(
            username=form.username.data,
            showname=form.showname.data,
            venuename=form.venuename.data,
            totalticket=form.totaltickets.data,
            reservation_date=form.show_date.data
        )
        db.session.add(new_booking)
        db.session.commit()
        return render_template("user/booking/showsuccess.html", booking=new_booking)

    return render_template("user/booking/bookshowform.html.jinja2", show=show, form=form)


@controllers.route("/user_profile", methods=['GET', 'POST'])
@login_required
def get_user_profile():
    # user = User.query.get_or_404(current_user.user_id)
    userdata = {
        "username": current_user.username,
        "first name": current_user.first_name,
        "last name": current_user.last_name,
        "email": current_user.email
    }
    return jsonify(userdata)
