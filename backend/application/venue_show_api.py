from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
from flask_cors import cross_origin
import uuid
from .models import Users, Venue, ShowVenue, Shows
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token

class VenueShowApi(Resource):
    @jwt_required()
    def get(self, venue_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if decoded_token:
            shows = Shows.query \
                .join(ShowVenue) \
                .filter(ShowVenue.venue_id == venue_id) \
                .all()

            venue_data = {
                "venue_id": venue_id,
                "shows": []
            }

            for show in shows:
                show_data = {
                    "show_id" : show.show_id,
                    "show_name" : show.show_name,
                    "show_pic" : show.show_pic,
                    "ratings" : show.ratings,
                    "tags" : show.tags,
                    "price" : show.price,
                    "admin_id" : show.admin_id
                }

                venue_data["shows"].append(show_data)

            return venue_data, 200
        return {'message': "You are not authorized to perform this action"}, 400
