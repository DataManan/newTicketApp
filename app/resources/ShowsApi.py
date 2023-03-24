from flask import jsonify
from flask_restful import Resource
# from .resources.shows import Shows, Show
from ..models import Shows
from .. import db

class ShowsAPI(Resource):
    def get(self):
        shows = Shows.query.all()
        showsdata = []
        for show in shows:
            tempshow = {
                "showname" : show.show_name, 
                "ticket_price": show.ticket_price,
                "premiere_date":show.premiere_date,
                "show_ratings":show.rating,
                "show_tags":show.tags,
                "show_description": show.show_description,
                "show_cast": show.cast,
                "show_poster": show.poster_filename
            }
            showsdata.append(tempshow)
        return jsonify(showsdata)