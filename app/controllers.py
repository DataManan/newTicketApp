from crypt import methods
from dataclasses import dataclass
from flask import Blueprint, render_template, request, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import Shows, User, TicketsBooked
from .forms import BookShowForm
from . import db

controllers = Blueprint('controllers', __name__)



@controllers.route('/')
def index():
    movies = Shows.query.all()
    return render_template('index.html.jinja2', SHOWS=movies, current_user=current_user)

@controllers.route('/<user_id>')
@login_required
def user_loggedin(user_id):
    movies = Shows.query.all()
    return render_template('index.html.jinja2', SHOWS=movies, current_user=current_user, user_id=user_id)


@controllers.route("/book_tickets/<user_id>/<show_id>")
@login_required
def book_tickets(user_id, show_id):
    user = User.query.get_or_404(user_id)
    movie = Shows.query.filter_by(show_id=show_id).first()
    return render_template("bookshow.html.jinja2", SHOW=movie, user=user)


@controllers.route("/booknow/<user_id>/<show_id>", methods=['GET', 'POST'])
@login_required
def booknow(user_id, show_id):
    form = BookShowForm()
    user=User.query.get_or_404(user_id)
    show=Shows.query.get_or_404(show_id)
    form.username.data = user.username
    form.showname.data = show.show_name
    form.venuename.data = show.venue_name
    if form.validate_on_submit():
        new_booking = TicketsBooked(
            username=form.username.data,
            showname=form.showname.data,
            venuename=form.venuename.data,
            totalticket=form.totaltickets.data,
            show_date=form.show_date.data
        )
        db.session.add(new_booking)
        db.session.commit()
        return render_template("showsuccess.html", booking=new_booking, user=user)
   
    return render_template("bookshowform.html.jinja2", user=user, show=show, form=form)