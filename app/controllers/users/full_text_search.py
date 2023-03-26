from flask import Blueprint, render_template, request
from flask_msearch import Search
# from flask_msearch.decorators import min_sized_query
from flask_whooshee import Whooshee
import requests
from ...models.models import Shows, Venues
from ... import db
# import requests
fts = Blueprint('full_text_search', __name__)

fts_search = Search(db=db)

@fts.route('/search')
# @fts_search.search('shows', minimum_match=2)
def fullTextSearch():
    q = request.args.get('q')
    shows = Shows.query.msearch(
        q, fields=['show_name', 'rating', 'tags', 'cast']).all()
    venues = Venues.query.msearch(
        q, fields=['venue_name', 'street', 'city', 'state', 'venue_tags']).all()

    return render_template('user/search_results.html.jinja2', shows=shows, venues=venues, q=q)

# app/templates/user/search_results.html.jinja2
