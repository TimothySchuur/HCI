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
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8081"}})

load_dotenv()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all origins
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')  # Allow these headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')  # Allow these methods
    return response

# Database configuration
app.config['SECRET_KEY'] = "your_secret_key"
app.config['JWT_SECRET_KEY'] = "your_jwt_secret_key"
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://reinierbos:password@localhost:5432/hci_db'

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# User model
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    strava_connected = db.Column(db.Boolean, default=False)

    # Relationship to UserShoes
    user_shoes = db.relationship(
        'UserShoes',
        back_populates='user',
        foreign_keys='UserShoes.user_id',  # Specify the foreign key explicitly
        cascade='all, delete-orphan'
    )

    # Relationship for main_shoe (optional, one-to-one relationship)
    main_shoe_id = db.Column(db.Integer, db.ForeignKey('user_shoes.id'), nullable=True)
    main_shoe = db.relationship(
        'UserShoes',
        foreign_keys='Users.main_shoe_id',
        uselist=False
    )

# Shoes table (static shoe data)
class Shoes(db.Model):
    __tablename__ = 'shoes'
    
    # Columns matching your table structure
    id = db.Column(db.Integer, primary_key=True)  # Primary Key
    shoe_brand = db.Column(db.String(100), nullable=False)  # Brand of the shoe
    model_name = db.Column(db.String(100), nullable=False)  # Model of the shoe
    price = db.Column(db.Float, nullable=False)  # Price of the shoe
    mileage = db.Column(db.Integer, nullable=False)  # Maximum mileage of the shoe
    main_focus = db.Column(db.String(100), nullable=False)  # Main focus (e.g., speed, durability)
    eco_friendly = db.Column(db.Boolean, nullable=False)  # Eco-friendly status (True/False)
    foot_type = db.Column(db.String(100), nullable=False)  # Foot type compatibility
    cushioning_rate = db.Column(db.Integer, nullable=False)  # Cushioning rate
    durability_rate = db.Column(db.Integer, nullable=False)  # Durability rate
    pace_rate = db.Column(db.Integer, nullable=False)  # Pace rate
    gender = db.Column(db.String(50), nullable=False)  # Gender (e.g., Men, Women, Unisex)

    # Relationship to UserShoes (if needed)
    user_shoes = db.relationship('UserShoes', back_populates='shoe')

class UserShoes(db.Model):
    __tablename__ = 'user_shoes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # ForeignKey links to Users table
    shoe_id = db.Column(db.Integer, db.ForeignKey('shoes.id'), nullable=False)
    mileage_run = db.Column(db.Float, default=0.0, nullable=False)
    mileage_remaining = db.Column(db.Integer, nullable=False)
    total_mileage_allowed = db.Column(db.Float, nullable=False)

    # Relationships
    user = db.relationship(
        'Users',
        back_populates='user_shoes',
        foreign_keys=[user_id]  # Explicit foreign key specification
    )
    shoe = db.relationship(
        'Shoes',
        back_populates='user_shoes'
    )

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

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error during registration: {e}")
        return jsonify({'error': 'Internal server error, please try again later'}), 500


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

    # Fetch main shoe from Users table
    main_shoe = UserShoes.query.filter_by(id=user.main_shoe_id).first() if user.main_shoe_id else None

    main_shoe_data = None
    if main_shoe:
        main_shoe_data = {
            'id': main_shoe.id,
            'shoe_brand': main_shoe.shoe.shoe_brand,
            'model_name': main_shoe.shoe.model_name,
            'mileage_run': main_shoe.mileage_run,
            'mileage_remaining': main_shoe.mileage_remaining,
            'cushioning_percentage': (main_shoe.mileage_remaining / main_shoe.total_mileage_allowed) * 100
        }

    user_shoes = UserShoes.query.filter_by(user_id=user.id).all()
    shoes_data = [
        {
            'id': user_shoe.id,
            'shoe_brand': user_shoe.shoe.shoe_brand,
            'model_name': user_shoe.shoe.model_name,
            'mileage_run': user_shoe.mileage_run,
            'mileage_remaining': user_shoe.mileage_remaining,
            'cushioning_percentage': (user_shoe.mileage_remaining / user_shoe.total_mileage_allowed) * 100
        }
        for user_shoe in user_shoes
    ]

    return jsonify({
        'username': user.username,
        'mainShoe': main_shoe_data,
        'userShoes': shoes_data,
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

# Initialize the Strava client
client = Client()

# Replace with your application's Client ID and desired redirect URI
client_id = 143329
client_secret = "b9154a522c6b3e5fc1aa607054a08c0cc8994627"
redirect_uri = "http://127.0.0.1:5000/authorize"

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
        activities = client.get_activities(limit=1)
        print(activities)
        
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
    
@app.route('/update-activities', methods=['POST'])
@jwt_required()
def update_activities():
    # Fetch activities from the client
    activities = client.get_activities(limit=1)
    activities_list = []
    for activity in activities:
        activities_list.append({
            'distance': activity.distance.magnitude if hasattr(activity.distance, 'magnitude') else None,  # Extract numeric value
        })
    
    # Convert the distance to kilometers
    distance = activities_list[0]['distance'] / 1000
    print(f"Distance (km): {distance}")

    # Get the current user from the JWT token
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get the user's shoe
    user_shoe = UserShoes.query.filter_by(user_id=user.id).first()

    if not user_shoe:
        return jsonify({'error': 'No shoe found for the user'}), 404

    # Update mileage_run
    user_shoe.mileage_run += distance
    print(f"Updated mileage_run: {user_shoe.mileage_run}")

    # Calculate remaining mileage and update the mileage_remaining field
    user_shoe.mileage_remaining = max(0, user_shoe.total_mileage_allowed - user_shoe.mileage_run)
    print(f"Updated mileage_remaining: {user_shoe.mileage_remaining}")

    # Commit changes to the database
    db.session.commit()

    return jsonify({'mileage_remaining': user_shoe.mileage_remaining}), 200


@app.route('/cushioning-percentage', methods=['GET'])
@jwt_required()
def get_cushioning_percentage():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_shoe = UserShoes.query.filter_by(user_id=user.id).first()
    if not user_shoe:
        return jsonify({'error': 'No shoe found for the user'}), 404

    percentage = (user_shoe.mileage_remaining / user_shoe.total_mileage_allowed) * 100
    percentage = round(max(0, min(percentage, 100)))  # Ensure it's between 0 and 100
    print(round(percentage))
    return jsonify({'cushioning_percentage': percentage}), 200


@app.route('/user/add-shoe', methods=['POST'])
@jwt_required()
def add_shoe():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    shoe_id = data.get('shoe_id')

    shoe = Shoes.query.get(shoe_id)
    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    new_user_shoe = UserShoes(
        user_id=user.id,
        shoe_id=shoe_id,
        mileage_run=0,
        mileage_remaining=shoe.mileage,
        total_mileage_allowed=shoe.mileage
    )
    db.session.add(new_user_shoe)
    db.session.commit()

    return jsonify({'message': 'Shoe added successfully'}), 201


@app.route('/user/set-main-shoe', methods=['POST'])
@jwt_required()
def set_main_shoe():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    shoe_id = data.get('shoe_id')

    # Check if the shoe belongs to the user
    user_shoe = UserShoes.query.filter_by(user_id=user.id, shoe_id=shoe_id).first()
    if not user_shoe:
        return jsonify({'error': 'Shoe not associated with user'}), 400

    user.main_shoe_id = shoe_id
    db.session.commit()

    return jsonify({'message': 'Main shoe updated successfully'}), 200


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
        'mileage_remaining': user_shoe.mileage_remaining,  # Include total_mileage_allowed
    }), 200


@app.route('/compare', methods=['GET'])
def process_data():
    try:
        # Load the CSV file
        df = pd.read_csv('./shoes.csv')
        # Convert to JSON and return the response
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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


if __name__ == '__main__':
    # Ensure the database tables are created before starting the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
