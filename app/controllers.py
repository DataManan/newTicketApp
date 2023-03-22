from crypt import methods
from dataclasses import dataclass
from flask import Blueprint, redirect, render_template, request, flash
from flask.helpers import url_for
from flask_login import login_required, current_user
from .models import Shows, User, TicketsBooked, Venues
from .forms import BookShowForm, get_venue_choices, SearchForm
from . import db
from sqlalchemy import or_

controllers = Blueprint('controllers', __name__)


@controllers.route('/')
def index():
    if not current_user.is_authenticated:
        movies = Shows.query.all()
        return render_template('index.html.jinja2', SHOWS=movies, current_user=current_user)

    return redirect(url_for('controllers.user_loggedin', user_id=current_user.user_id))


@controllers.route('/<user_id>')
@login_required
def user_loggedin(user_id):
    movies = Shows.query.all()
    return render_template('index.html.jinja2', SHOWS=movies, current_user=current_user, user_id=user_id)

# seacrh bar


@controllers.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()

    
    search_term = form.search.data

    shows = Shows.query.filter(or_(
        Shows.show_name.ilike(f'%{search_term}%'),
        Shows.rating.ilike(f'%{search_term}%'),
        Shows.tags.ilike(f'%{search_term}%')
    )).all()

    return render_template('search_results.html.jinja2', shows=shows)

    


 # shows = Shows.query.filter((Shows.show_name.like(f'%{search_term}%')) | (
    #     Shows.rating.like(f'%{search_term}%')) | (Shows.tags.like(f'%{search_term}%'))).all()
    # print(shows)

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
    user = User.query.get_or_404(user_id)
    show = Shows.query.get_or_404(show_id)
    form.username.data = user.username
    form.showname.data = show.show_name
    form.venuename.choices = get_venue_choices(show.show_name)
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
