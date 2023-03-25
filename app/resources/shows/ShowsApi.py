from flask import jsonify
from flask_restful import Resource
# from .resources.shows import Shows, Show
from ...models import Shows
from ... import db
from flask_login import login_required
from ...auth import admin_required

class ShowsAPI(Resource):
    def get(self):
        shows = Shows.query.all()
        showsdata = []
        for show in shows:
            tempshow = {
                "show_id": show.show_id,
                "show_name": show.show_name,
                "ticket_price": show.ticket_price,
                "premiere_date": show.premiere_date,
                "show_ratings": show.rating,
                "show_tags": show.tags,
                "show_description": show.show_description,
                "show_cast": show.cast,
                "show_poster": show.poster_filename
            }
            showsdata.append(tempshow)
        return jsonify(showsdata)
    
class ShowAPI(Resource):
    # @admin_required
    # @login_required
    def get(self, show_id):
        show = Shows.query.get_or_404(show_id)

        try :
            showdata = {
                "show_id": show.show_id,
                "show_name": show.show_name,
                "ticket_price": show.ticket_price,
                "premiere_date": show.premiere_date,
                "show_ratings": show.rating,
                "show_tags": show.tags,
                "show_description": show.show_description,
                "show_cast": show.cast,
                "show_poster": show.poster_filename
            }
            return jsonify(showdata)
        except:
            return {"error":"show doesn\'t exist"}, 404


    def post(self, show_obj):
        pass