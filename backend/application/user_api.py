from flask_restful import Resource
from flask import request
from .models import Users
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended.utils import decode_token
from .database import db

class UserApi(Resource):
    
    @jwt_required()
    
    def get(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  


        decoded_token = decode_token(token)
       
        
        user = Users.query.filter_by(public_id = current_user).first()

        return {'message': "You are Logged in", 'username' : user.name, 
                "role" : user.role, 
                "profile_pic" : user.profile_pic,
                "user_id" : current_user}, 200

    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        

        decoded_token = decode_token(token)
        if decoded_token:
            user = Users.query.filter_by(public_id = current_user).first()
            name = request.form.get('username')
            lang = request.form.get('lang')
            region = request.form.get('region')
            print(user, name, lang)


            if name:
                user.name = name
            
            if lang:
                user.lang = lang.lower()
            
            if region:
                user.region = region.lower()
            db.session.commit()
            return {"message" : "User Details Updated Successfully",
                    "username" : user.name,
                    "role" : user.role}, 200
        return {'message' : "You are not Authorized to perform this action"}, 400
    
    @jwt_required()
    def delete(self):
        current_user = get_jwt_identity()
        token = request.headers.get('Authorization').split()[1]  
        
        
        decoded_token = decode_token(token)
        if decode_token:
            user = Users.query.filter_by(public_id = current_user).first()
            db.session.delete(user)
            db.session.commit()
            return {"message" : "User Deleted Successfully"}, 200
        else:
            return {'message' : "You are not Authorized to perform this action"}, 400
            
    
        
            