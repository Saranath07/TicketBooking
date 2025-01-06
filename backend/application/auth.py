from flask import jsonify, request
from flask import current_app as app
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from .database import db
from .models import Users
from flask_jwt_extended import  create_access_token
from flask import send_from_directory
import time

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/register/user', methods=['POST'])
@cross_origin()
def signup_user(): 
   data = request.get_json() 

   print(data)
   print("\n\n\n")
   old_user = Users.query.filter_by(email = data['email']).first()
   if old_user:
       return {"error" : "User with same email already exist"}, 409
   hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
   public_id = str(uuid.uuid4())

    
   if data['email'] and data['password']:
      data['region'] = 'Chennai'
      new_user = Users(public_id = public_id, name = data['username'], 
                     password = hashed_password, role = 'user',
                     email = data['email'], language = data['lang'].lower(), region = data['region'].lower())
      db.session.add(new_user) 
      
         
      db.session.commit() 
      return jsonify({'message': 'User registered successfully'}), 201
   return {"error" : "Insufficient credentials"}, 400

@app.route('/register/admin', methods=['POST'])
@cross_origin()
def signup_admin(): 
   data = request.get_json() 
   print(data)

   print("\n\n\n")
   old_user = Users.query.filter_by(email = data['email']).first()
   if old_user:
       return {"error" : "User with same email already exist"}, 409
   hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
   
   if data['email'] and data['password']:
   
      new_admin = Users(public_id=str(uuid.uuid4()), name=data['username'], 
                        password=hashed_password, role = 'admin',
                        email = data['email'], language=data['lang'].lower(), 
                        region = data['region'].lower(),
                        )
      db.session.add(new_admin)
         
      
      db.session.commit()   
      return jsonify({'message': 'Admin registered successfully'}), 201
   return {"error" : "Insufficient credentials"}, 400




@app.route('/api/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = Users.query.filter_by(email=email).first()  
 
    # Check if user exists and password is correct
    if user and check_password_hash(user.password, password):
        
        user.lastseen = time.time()
        db.session.commit()
        access_token = create_access_token(identity=user.public_id, 
                                        additional_claims={'role': user.role})
        return jsonify({'access_token': access_token, 
                        'username' : user.name,
                        'role' : user.role,}), 200
        
            
    return jsonify({'error' : 'Invalid credentials'}), 403
    

