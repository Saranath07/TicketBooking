from flask_restful import Resource, marshal_with, fields
from flask import request, jsonify
from .database import db
import uuid
from .models import Users,ShowVenue, Bookings, Shows, Venue
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from sqlalchemy import func
from sqlalchemy import or_

movie_fields = {
    "show_id" : fields.String,
    "show_name" : fields.String,
    "show_pic" : fields.String,
    "ratings" :fields.String,
    "tags" :fields.String,
    "price" : fields.Integer,
}
venue_fields = {
    "venue_id": fields.String,
    "venue_name": fields.String,
    "venue_pic": fields.String,
    "region": fields.String,
    "capacity": fields.String,
    "venue_description": fields.String,
    "available_seats": fields.Integer(default=0), 
}

class MovieSearchApi(Resource):
    @marshal_with(movie_fields)
    def get(self):
        tags = request.args.get('tags')
        rating = request.args.get('rating') 
        name = request.args.get('name')
        show = Shows.query.filter_by(show_name = name).first()
        print(name)
        
        movies = Shows.query.filter(or_(Shows.show_name.contains(name), Shows.show_name.is_(None))).all()
        print(movies)
        
        if movies:
            return movies, 200
        movies = Shows.query.order_by(Shows.id.desc()).all()
        filtered_movies = []
        for movie in movies:
            if tags and tags not in movie.tags:
                continue
            if rating and movie.ratings < float(rating):
                continue
            filtered_movies.append({
                'show_name' : movie.show_name,
                'show_pic' : movie.show_pic,
                'show_id' : movie.show_id,
                'ratings' : movie.ratings,
                'price' : movie.price,
                'tags' : movie.tags
            })
        
        print(filtered_movies)
        return filtered_movies, 200

class RegionSearchApi(Resource):
    @marshal_with(venue_fields)
    def get(self, region):
        venues = Venue.query.filter_by(region = region).all()
        return venues

class LanguageSearchApi(Resource):
    @marshal_with(movie_fields)
    def get(self, lang):
        shows = Shows.query.filter_by(language = lang).all()
        return shows
    