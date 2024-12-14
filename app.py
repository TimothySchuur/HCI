from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from stravalib import Client
import time
from pprint import pprint
import pandas as pd
from dotenv import load_dotenv
import os

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
load_dotenv()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all origins
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')  # Allow these headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')  # Allow these methods
    return response

# Database configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# User model
class Users(db.Model):
    __tablename__ = 'users'  # Fixed typo ('sers' -> 'users')
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    strava_connected = db.Column(db.Boolean, default=False)

    # Relationship to UserShoes
    user_shoes = db.relationship('UserShoes', back_populates='user', cascade='all, delete-orphan')

# Shoes table (static shoe data)
class Shoes(db.Model):
    __tablename__ = 'shoes'
    id = db.Column(db.Integer, primary_key=True)
    shoe_brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    main_focus = db.Column(db.String(100), nullable=False)
    eco_friendly = db.Column(db.Boolean, nullable=False)
    foot_type = db.Column(db.String(100), nullable=False)
    cushioning_rate = db.Column(db.Integer, nullable=False)
    durability_rate = db.Column(db.Integer, nullable=False)
    pace_rate = db.Column(db.Integer, nullable=False)

    # Relationship to UserShoes
    user_shoes = db.relationship('UserShoes', back_populates='shoe')

# UserShoes table (junction table with stats)
class UserShoes(db.Model):
    __tablename__ = 'user_shoes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey links to Users table
    shoe_id = db.Column(db.Integer, db.ForeignKey('shoes.id'), nullable=False)
    mileage_run = db.Column(db.Float, default=0.0, nullable=False)
    total_mileage_allowed = db.Column(db.Float, nullable=False)

    # Relationships
    user = db.relationship('Users', back_populates='user_shoes')  # Links back to Users
    shoe = db.relationship('Shoes', back_populates='user_shoes')  # Links back to Shoes

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    try:
        current_user = get_jwt_identity()  # Retrieve the identity from the token
        return jsonify({'message': 'Token is valid', 'user': current_user}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401

# Register endpoint
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    # Check if the email already exists
    existing_user = Users.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400

    # Hash the password and save the new user
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = Users(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = Users.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Generate JWT token
    access_token = create_access_token(identity=email)
    return jsonify({'message': 'Login successful', 'token': access_token}), 200

from flask_jwt_extended import jwt_required, get_jwt_identity

@app.route('/user-profile', methods=['GET'])
@jwt_required()
def user_profile():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_shoe = UserShoes.query.filter_by(user_id=user.id).first()

    shoe_data = None
    mileage_data = None
    if user_shoe:
        shoe = Shoes.query.filter_by(id=user_shoe.shoe_id).first()
        shoe_data = {
            'shoe_brand': shoe.shoe_brand,
            'model_name': shoe.model_name
        }
        mileage_data = {
            'mileage_run': user_shoe.mileage_run,
            'total_mileage_allowed': user_shoe.total_mileage_allowed
        }

    return jsonify({
        'username': user.username,
        'shoe': shoe_data,
        'mileage': mileage_data
    }), 200


revoked_tokens = set()

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in revoked_tokens

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Add the token's jti (JWT ID) to the revoked tokens set
    token_jti = get_jwt_identity()['jti']
    revoked_tokens.add(token_jti)
    return jsonify({'message': 'Successfully logged out'}), 200


client_secret = os.getenv('STRAVA_CLIENT_SECRET')

# Initialize the Strava client
client = Client()

# Replace with your application's Client ID and desired redirect URI
client_id = os.getenv('STRAVA_CLIENT_ID')
redirect_uri = os.getenv('STRAVA_REDIRECT_URI') # Must match Strava's settings

@app.route('/check_strava', methods=['GET'])
def check_strava_page():
    return render_template('check_strava.html')

@app.route('/connect_strava', methods=['GET'])
def connect_strava():
    scope = 'activity:read_all'
    authorize_url = (
        f"https://www.strava.com/oauth/authorize?"
        f"client_id={client_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"approval_prompt=force&"
        f"scope={scope}"
    )
    print(authorize_url)
    return redirect(authorize_url)

@app.route('/authorize', methods=['GET'])
def strava_callback():
    code = request.args.get('code')
    print(f"CODE = {code}")
    if not code:
        return jsonify({'error': 'Strava authorization failed'}), 400

    # Exchange authorization code for access token
    # access_token = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)
    access_token_response = client.exchange_code_for_token(
        client_id=client_id, 
        client_secret=client_secret, 
        code=code
    )
    client.access_token = access_token_response['access_token']
    client.refresh_token = access_token_response['refresh_token']
    client.token_expires_at = access_token_response['expires_at']

    if time.time() > client.token_expires_at:
        refresh_response = client.refresh_access_token(
            client_id=140518, client_secret="b3cdf712eff0cf8fef5332ba80012b6cf1fff435", refresh_token=client.refresh_token
        )
        client.access_token = refresh_response["access_token"]
        client.refresh_token = refresh_response["refresh_token"]
        client.expires_at = refresh_response["expires_at"]

    # Mark the user as connected to Strava
    if 'user_id' in session:
        user = Users.query.get(session['user_id'])
        if user:
            user.strava_connected = True
            db.session.commit()

    return redirect('http://localhost:8081/home')

@app.route('/activities', methods=['GET'])
def activities():
    try:
        # Fetch activities using the Strava client
        activities = client.get_activities(limit=10)
        
        # Extract relevant information and preprocess distance
        activities_list = []
        for activity in activities:
            activities_list.append({
                'name': activity.name,
                'distance': activity.distance.magnitude if hasattr(activity.distance, 'magnitude') else None,  # Extract numeric value
            })


        # Return the preprocessed activities as JSON
        return jsonify(activities_list)
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return jsonify({'error': 'Failed to fetch activities'}), 500


# Endpoint to fetch all shoes
@app.route('/shoes', methods=['GET'])
def get_shoes():
    shoes = Shoes.query.all()
    return jsonify([{
        'id': shoe.id,
        'shoe_brand': shoe.shoe_brand,
        'model_name': shoe.model_name,
        'price': shoe.price,
        'main_focus': shoe.main_focus,
        'eco_friendly': shoe.eco_friendly,
        'foot_type': shoe.foot_type,
        'cushioning_rate': shoe.cushioning_rate,
        'durability_rate': shoe.durability_rate,
        'pace_rate': shoe.pace_rate,
    } for shoe in shoes])

@app.route('/user/add-shoe', methods=['POST'])
@jwt_required()
def add_shoe_to_user():
    data = request.get_json()
    shoe_id = data.get('shoe_id')

    if not shoe_id:
        return jsonify({'error': 'Shoe ID is required'}), 400

    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Check if the shoe exists
    shoe = Shoes.query.get(shoe_id)
    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    # Check if the user already has this shoe
    if UserShoes.query.filter_by(user_id=user.id, shoe_id=shoe.id).first():
        return jsonify({'error': 'Shoe already added'}), 400

    # Add the shoe to the user
    user_shoe = UserShoes(user_id=user.id, shoe_id=shoe.id, total_mileage_allowed=shoe.durability_rate)
    db.session.add(user_shoe)
    db.session.commit()

    return jsonify({'message': 'Shoe added successfully'}), 200 

@app.route('/user/mileage-run', methods=['GET'])
@jwt_required()
def get_mileage_run():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get the user's shoe data
    user_shoe = UserShoes.query.filter_by(user_id=user.id).first()
    print(user_shoe)

    if not user_shoe:
        return jsonify({'error': 'No shoe data found for user'}), 404

    return jsonify({
        'mileage_run': user_shoe.mileage_run,
        'total_mileage_allowed': user_shoe.total_mileage_allowed,  # Include total_mileage_allowed
    }), 200


@app.route('/compare-shoes', methods=['GET'])
def process_data():
    try:
        # Load the CSV file
        df = pd.read_csv('./shoes.csv')
        # Convert to JSON and return the response
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route('/associate_shoe', methods=['POST'])
# def associate_shoe():
#     data = request.json
#     if not data or 'user_id' not in data or 'shoe_id' not in data:
#         return jsonify({'error': 'Invalid data'}), 400

#     # Verify user exists
#     user = Users.query.get(data['user_id'])
#     if not user:
#         return jsonify({'error': 'User not found'}), 404

#     # Verify shoe exists
#     shoe = Shoes.query.get(data['shoe_id'])
#     if not shoe:
#         return jsonify({'error': 'Shoe not found'}), 404

#     # Check if the shoe is already associated with another user
#     if shoe.user_id:
#         return jsonify({'error': 'Shoe is already associated with a user'}), 409

#     # Associate shoe with the user
#     shoe.user_id = data['user_id']
#     db.session.commit()

#     return jsonify({'message': f'Shoe "{shoe.model_name}" successfully associated with user {user.username}!'})



if __name__ == '__main__':
    # Ensure the database tables are created before starting the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
