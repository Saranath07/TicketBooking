from flask_restful import Resource, marshal_with, fields
from flask import request, jsonify
from .database import db
import uuid
from .models import Users,ShowVenue, Bookings, Shows, Venue
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import decode_token


class TicketDetails(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        
        decoded_token = decode_token(token)
        if 'user' in decoded_token['role']:
            user = Users.query.filter_by(public_id = current_user).first()
            print(user)
            if not user:
                return jsonify({"message" : "User not found"}), 400
            bookings = Bookings.query.filter_by(user_id = current_user).all()
            
            result = []
            booking_ids = []
            for booking in bookings:
                if booking.booking_id in booking_ids:
                    for i in result:
                        if i['booking_id'] == booking.booking_id:
                            i['list_of_seats'].append(booking.seat_number)
                else:
                    show_venue = ShowVenue.query.filter_by(showvenue_id = booking.showvenue_id).first()
                    show = Shows.query.filter_by(show_id = show_venue.show_id).first()
                    venue = Venue.query.filter_by(venue_id = show_venue.venue_id).first()
                    result.append({
                        'booking_id' : booking.booking_id,
                        'show_name' : show.show_name,
                        'show_pic' : show.show_pic,
                        'list_of_seats' : [booking.seat_number],
                        'venue_name' : venue.venue_name
                    })
                    booking_ids.append(booking.booking_id)
            # print(jsonify(result))
            return result, 200
        return {'message' : "You are not Authorized to perform this action"}, 400