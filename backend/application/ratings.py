from flask import jsonify, request
from flask import current_app as app
from flask_cors import cross_origin
from flask_restful import Resource
from flask import request
from .models import Users, Shows
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from .database import db



@app.route("/ratings/<show_id>", methods=["PUT"])
@jwt_required()
def ratings(show_id):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        
        
        decoded_token = decode_token(token)
        if decoded_token:
            show = Shows.query.filter_by(show_id = show_id).first()
            data = request.get_json()
            # ratings = float(request.form.get('ratings'))
            ratings = float(data["ratings"])
            K = show.K + 1
            print(K)
            
            if K == 0:
                  show.ratings = round(ratings, 2) 
            else:
                show.ratings = round(show.ratings + (1 / K)*(ratings - show.ratings), 2)
            show.K = show.K + 1
            db.session.commit()

  
            return {"message" : "Thanks for your feedback"}, 201
        
        return {'message' : "You are not Authorized to perform this action"}, 400