from flask import Blueprint
from flask_msearch import Search
from flask_whooshee import Whooshee

fts = Blueprint('full_text_search', __name__)

fts_search = Search()