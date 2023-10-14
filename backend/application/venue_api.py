from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
from flask_cors import cross_origin
import uuid
from .models import Users, Venue, ShowVenue, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from sqlalchemy import func

venue_fields = {
    "venue_id": fields.String,
    "venue_name": fields.String,
    "venue_pic": fields.String,
    "region": fields.String,
    "capacity": fields.String,
    "venue_description": fields.String,
    "available_seats": fields.Integer(default=0), 
}

class VenueApi(Resource):

    
    @marshal_with(venue_fields)
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if 'admin' in decoded_token['role']:
            user = Users.query.filter_by(public_id = current_user).first()
            venue_id = request.args.get('venue_id')
            if venue_id:
                
                venues = Venue.query \
                    .join(ShowVenue, Venue.id == ShowVenue.venue_id) \
                    .filter(ShowVenue.venue_id == venue_id, Venue.admin_id == user.id) \
                    .add_columns(Venue.id, Venue.venue_name, Venue.venue_pic, Venue.location, Venue.capacity, Venue.venue_description, ShowVenue.available_seats) \
                    .all()
                if venues:
                     venues_mapped = [{
                            "venue_id": venue.id,
                            "venue_name": venue.venue_name,
                            "venue_pic": venue.venue_pic,
                            "location": venue.region,
                            "capacity": venue.capacity,
                            "venue_description": venue.venue_description
                        } for venue in venues]
                     
                     return venues_mapped
                else:
                    return {'message' : 'No venue alloted for this venue'}, 404
            else:
                
                user = Users.query.filter_by(public_id = current_user).first()
                venues = Venue.query.filter_by(admin_id = user.id).order_by(Venue.id.desc()).all()
                print(venues)
                return venues
        elif 'user' in decoded_token['role']:
            
            user = Users.query.filter_by(public_id = current_user).first()
            venues = Venue.query.order_by(Venue.id.desc()).all()
            print(venues)
            return venues
            # print(venues)
        return {'message' : "You are not Authorized to perform this action"}, 400
    
    
    @jwt_required()
    
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  


        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
            data = request.get_json() 
            print(data)
            venue_name = data.get('venue_name')
            location = data.get('location').lower()
            capacity = data.get('capacity')
            desc = data.get('description')
            user = Users.query.filter_by(public_id = current_user).first()
            venue = Venue(venue_name = venue_name, venue_id = str(uuid.uuid4()), 
                          region = location, capacity = capacity, 
                          admin_id = user.id, venue_description = desc)
            db.session.add(venue)
            db.session.commit()
            return {"message" : "Venue created Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    
    @jwt_required()
    def put(self, venue_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
        print(decoded_token)
        print(decoded_token['role'] == 'admin')
        if decoded_token['role'] == 'admin':
            
            

            venue = Venue.query.filter_by(venue_id = venue_id).first()
            # return venue.venue_name, 200
            venue_name = request.form.get('venue_name')
           
            description = request.form.get('description')
            
            region = request.form.get('region')
           
            print(venue_name)
            
            
           
            
            
            if venue_name:
                venue.venue_name = venue_name
            
            if description:
                venue.venue_description = description
            
            if region:
                venue.region = region
            
            db.session.commit()
            return {"message" : "Venue Updated Successfully"}, 200
        return {'message' : "You are not Authorized to perform this action"}, 400

    @jwt_required()
    
    def delete(self, venue_id):
        # return "Hello", 200
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
            venue = Venue.query.filter_by(venue_id = venue_id).first()
            print(venue)
            
            showvenues = ShowVenue.query.filter_by(venue_id = venue.venue_id).all()
            for showvenue in showvenues:
                bookings = Bookings.query.filter_by(showvenue_id = showvenue.showvenue_id).all()
                for booking in bookings:
                    db.session.delete(booking)
                    db.session.commit()
            db.session.delete(venue)
            db.session.commit()
            return {"message" : "Venue Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
 
class VenueAnalyticsApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if 'admin' in decoded_token['role']:
            results = db.session.query(Venue.venue_name, func.count(Bookings.id)).\
                join(ShowVenue, Venue.venue_id == ShowVenue.venue_id).\
                join(Bookings, ShowVenue.showvenue_id == Bookings.showvenue_id).\
                group_by(Venue.venue_name).all()


            venue_names = [venue_name for (venue_name, count) in results]
            venue_counts = [count for (venue_name, count) in results]

            return {"venues" : venue_names, "viewers" : venue_counts}, 200
                


               
            
            


        return {'message' : "You are not Authorized to perform this action"}, 400