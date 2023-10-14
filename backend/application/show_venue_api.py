from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
from flask_cors import cross_origin
import uuid
from .models import Users, Venue, ShowVenue
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token


class ShowVenueApi(Resource):
    @jwt_required()
    def get(self, show_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if decoded_token:
            venues = Venue.query \
                .join(ShowVenue) \
                .filter(ShowVenue.show_id == show_id) \
                .all()

            show_data = []
            for venue in venues:
                show_venues = ShowVenue.query \
                    .filter_by(show_id=show_id, venue_id=venue.venue_id) \
                    .all()

                venue_data = {
                    "venue_id": venue.venue_id,
                    "venue_name": venue.venue_name,
                    "location": venue.region,
                    "capacity": venue.capacity,
                    "venue_description": venue.venue_description,
                    "timings": [],
                    
                }
                print(show_venues)
                for show_venue in show_venues:
                    available_seats = show_venue.available_seats
                    timing = {
                        "timing_id": show_venue.showvenue_id,
                        "timing": show_venue.timings,
                        "available_seats": available_seats,
                        "price" : show_venue.price
                    }
                    venue_data["timings"].append(timing)

                show_data.append(venue_data)

            return show_data, 200
        return {'message' : "You are not Authorized to perform this action"}, 400