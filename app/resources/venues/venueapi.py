import json
import re
from flask_login import login_required
from flask_restful import Resource, marshal_with, fields, reqparse
from flask import jsonify
from ...models import Venues
from ... import db

venue_fields = {
    # 'venue_id': fields.Integer,
    'venue_name': fields.String,
    'capacity': fields.Integer,
    'street': fields.String,
    'city': fields.String,
    'state': fields.String,
    'venue_tags': fields.String
    
}

class VenueApi(Resource):

    def get(self):
        """return a list of all venues

        Returns:
            json: all the attributes of venues
        """
        venues = Venues.query.all()
        if venues:
            
            temp_list = []
            temp_data = {}
            for venue in venues:
                temp_data = {
                    "venue_id": venue.venue_id,
                    "venue_name": venue.venue_name,
                    "capacity": venue.capacity,
                    # venue address is divided into three parts, street/city/state
                    "venue_street": venue.street,
                    "venue_city": venue.city,
                    "venue_state": venue.State,
                    # different tags for the venue
                    "venue_tags": venue.venue_tags
                }
                temp_list.append(temp_data)

            return temp_list
       
        return jsonify({"Error":"Requested venue doesn\'t exist"}), 404

    
    @login_required
    @marshal_with(venue_fields)
    def post(self, venue_details):
        if venue_details == {}:
            return 500
        
        parser = reqparse.RequestParser()
        parser.add_argument('venue_name', type=str, required=True,
                            help='Name of the venue is required.')
        parser.add_argument('capacity', type=int, required=True,
                            help='capacity is required.')
        parser.add_argument('street', type=str, required=True,
                            help='street is required.')
        parser.add_argument('city', type=str, required=True, help='city is required.')
        parser.add_argument('state', type=str, required=True,
                            help='state is required.')
        parser.add_argument('venue_tags', type=str, required=True, help='venue tags are required.')

        args = parser.parse_args()
        try:
            new_venue = Venues(
                venue_name=args['venue_name'],
                capacity=args['capacity'],
                street=args['street'],
                city = args['city'],
                state=args['state'],
                venue_tags=args['venue_tags']
                )
        
            db.session.add(new_venue)
            db.session.commit()
            return {"Success": "Venue added succesfully"}, 200
        except:
            db.session.rollback()

            return {"Error": "Cannot add venue"}, 500
        