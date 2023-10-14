from flask_restful import Resource, marshal_with, fields
from flask import request, jsonify
from .database import db
import uuid
from .models import Users,ShowVenue, Bookings, Shows, Venue
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from sqlalchemy import func
from sqlalchemy import or_

class RegionApi(Resource):
    def get(self):
        venues = Venue.query.all()
        regions = set()
        for venue in venues:
            regions.add(venue.region)
        return list(regions)
    
class LanguageApi(Resource):
    def get(self):
        shows = Shows.query.all()
        langs = set()
        for show in shows:
            langs.add(show.language)
        return list(langs)
