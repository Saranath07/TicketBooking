from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users,ShowVenue, Bookings
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from datetime import datetime

bookings_fields = {
    "booking_id" : fields.String,
    "user_id" : fields.String,
    "seat_number" : fields.String

}

class BookingApi(Resource):
    @marshal_with(bookings_fields)
    @jwt_required()
    def get(self, showvenue_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        
        if token:
            
            bookings = Bookings.query.filter_by(showvenue_id =showvenue_id).all()
            # print(bookings)
            return bookings, 200
        return {'message' : "You are not Authorized to perform this action"}, 400
    
    @jwt_required()
    
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  


        decoded_token = decode_token(token)
       
        if 'user' in decoded_token['role']:
            data = request.get_json() 
            print(data)
            showvenue_id = data['showvenue_id']
            seat_numbers = data['seat_numbers']
            print(seat_numbers)
            error_message = ""
            
            user = Users.query.filter_by(public_id = current_user).first()
            showvenue = ShowVenue.query.filter_by(showvenue_id = showvenue_id).first()
            if showvenue.available_seats == 0:
                error_message = f"No seats available for this movie. House Full!!"
            booking_id = str(uuid.uuid4())
            time = datetime.utcnow()
            for seat_number in seat_numbers:
                existing_booking = Bookings.query.filter_by(showvenue_id=showvenue.showvenue_id, seat_number=seat_number).first()
                if existing_booking:
                    error_message = f"Seat {seat_number} is already booked for this show."
                    break
                booking = Bookings(booking_id = booking_id,user_id = user.public_id, showvenue_id = showvenue.showvenue_id, 
                                   seat_number = seat_number, time = time)
                showvenue.available_seats -= 1
                db.session.add(booking)
            if error_message:
                db.session.rollback()
                return {"message": error_message}, 400
            db.session.commit()
            return {"message" : "Your Show is booked Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    
    
