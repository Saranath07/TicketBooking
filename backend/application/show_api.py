from flask_restful import Resource, marshal_with, fields
from flask import request
from .database import db
import uuid
from .models import Users, Shows, Venue, ShowVenue, Bookings
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity
from flask_jwt_extended.utils import decode_token
import os
from sqlalchemy import func

show_fields = {
    "show_id" : fields.String,
    "show_name" : fields.String,
    "show_pic" : fields.String,
    "ratings" :fields.String,
    "tags" :fields.String,
    "price" : fields.Integer,
    "admin_id" : fields.String,
    "language" : fields.String
 }

class ShowApi(Resource):
    @jwt_required()
    @marshal_with(show_fields)
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if 'admin' in decoded_token['role']:
            # user = Users.query.filter_by(public_id = current_user).first()
            shows = Shows.query.filter_by(admin_id = current_user).all()
            return shows
        elif 'user' in decoded_token['role']:
            shows = Shows.query.order_by(Shows.id.desc()).all()
            
            return shows
        return {'message' : "You are not Authorized to perform this action"}, 400
    
    @jwt_required()
    
    def post(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  


        decoded_token = decode_token(token)
       
        if 'admin' in decoded_token['role']:
            
            show_name = request.form.get('show_name')
            ratings = request.form.get('ratings')
            timings = request.form.get('timings')
            price = request.form.get('price')
            tags = request.form.get('tags')
            show_description = request.form.get('description')
            venues = request.form.get('venues')
            language = request.form.get('lang')
            image_name = request.files['show_pic'].filename
            folder_path = f'static/shows/{current_user}'
            venues = venues.split(",")
            try:
                os.makedirs(folder_path, exist_ok=True)
                request.files['show_pic'].save(os.path.join(folder_path, image_name))
            except:
                return 'Invalid file type', 400

            # admin_name = data.get('username')
            # admin = Users.query.filter_by(name = admin_name).first()
            # user = Users.query.filter_by(public_id = current_user).first()
            show = Shows(show_name = show_name, show_id = str(uuid.uuid4()), ratings = ratings, 
                           admin_id = current_user, tags = tags.lower(),
                           show_description = show_description, show_pic = f"/{current_user}/{image_name}",
                           language = language, K = 0)
            db.session.add(show)
            for venueId in venues:
                venue = Venue.query.filter_by(venue_id = venueId).first()
                previous_shows = ShowVenue.query.filter_by(venue_id = venue.id).all()
                new_start_time, new_end_time = timings.split(' - ')
                for prev_show in previous_shows:
                    show_start_time, show_end_time = prev_show.timings.split(' - ')

                    # Check for clash in timings
                    if new_start_time < show_end_time and new_end_time > show_start_time:
                        movie = Shows.query.filter_by(id = prev_show.show_id).first()
                        return {"message" :f"Clash in timings with existing show '{movie.show_name}'"}, 403
                
                showvenue = ShowVenue(showvenue_id = str(uuid.uuid4()), show_id = show.show_id, venue_id = venue.venue_id, timings = timings, available_seats = venue.capacity, price = price )

                venue.showvenues.append(showvenue)
                
            db.session.commit()
            return {"message" : "Show created and added to respective venues Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
    
    @jwt_required()
    def put(self, show_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
        
        if 'admin' in decoded_token['role']:
            
            # return "hello", 200
            show = Shows.query.filter_by(show_id = show_id).first()
            # return show.show_name, 200
            show_name = request.form.get('show_name')
            
            description = request.form.get('description')
            
            show_pic = request.files.get('show_pic')
            
            venues = request.form.get('venues')
            timings = request.form.get('timings')
            venues = venues.split(",")
            price = request.form.get('price')
            
            print(venues)
            
            
            if show_name:
                show.show_name = show_name
            
            if description:
                show.show_description = description
            
            if show_pic:
                image_name = request.files['show_pic'].filename
                folder_path = f'static/shows/{current_user}'
                try:
                    os.makedirs(folder_path, exist_ok=True)
                    request.files['show_pic'].save(os.path.join(folder_path, image_name))
                except:
                    return 'Invalid file type', 400
                show.show_pic = f"/{current_user}/{image_name}"
            print(show.show_name)
            print(timings)
            if price:
                show.price = price
            print(venues)
            if venues != [''] and venues:
                if timings != " - ":
                    
                    for venueId in venues:
                        venue = Venue.query.filter_by(venue_id = venueId).first()
                        previous_shows = ShowVenue.query.filter_by(venue_id = venue.venue_id).all()
                        new_start_time, new_end_time = timings.split(' - ')
                        for prev_show in previous_shows:
                            show_start_time, show_end_time = prev_show.timings.split(' - ')

                            # Check for clash in timings
                            if new_start_time < show_end_time and new_end_time > show_start_time:
                                movie = Shows.query.filter_by(id = prev_show.show_id).first()
                                return {"message" :f"Clash in timings with existing show '{movie.show_name}'"}, 403
                        showvenue = ShowVenue(showvenue_id = str(uuid.uuid4()), show_id = show.show_id, venue_id = venue.venue_id, timings = timings, available_seats = venue.capacity, price = price )

                        venue.showvenues.append(showvenue)
                else:
                    return {"message" : "Venue and timings are to be given."}, 400
            db.session.commit()
            return {"message" : "Show Updated Successfully"}, 200
        return {'message' : "You are not Authorized to perform this action"}, 400

    @jwt_required()
    def delete(self, show_id):
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        
        print(token)
        decoded_token = decode_token(token)
        
        if 'admin' in decoded_token['role']:
            show = Shows.query.filter_by(show_id = show_id).first()
            print(show)
            showvenues = ShowVenue.query.filter_by(show_id = show.show_id).all()
            for showvenue in showvenues:
                bookings = Bookings.query.filter_by(showvenue_id = showvenue.showvenue_id).all()
                for booking in bookings:
                    db.session.delete(booking)
            db.session.delete(show)

            db.session.commit()
            return {"message" : "Show Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400


class ShowAnalyticsApi(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        token = request.headers.get('Authorization').split()[1]  
        decoded_token = decode_token(token)
        if 'admin' in decoded_token['role']:
            results = db.session.query(Shows.show_name, func.count(Bookings.id)).\
                join(ShowVenue, Shows.show_id == ShowVenue.show_id).\
                join(Bookings, ShowVenue.showvenue_id == Bookings.showvenue_id).\
                group_by(Shows.show_name).all()

            show_names = [show_name for (show_name, count) in results]
            show_counts = [count for (show_name, count) in results]

            return {"movies" : show_names, "viewers" : show_counts}, 200
                


               
            
            


        return {'message' : "You are not Authorized to perform this action"}, 400