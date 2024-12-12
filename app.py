from flask import Flask, jsonify, request, render_template, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from stravalib import Client
# from __future__ import print_statement
import time
# import swagger_client
# from swagger_client.rest import ApiException
from pprint import pprint
import pandas as pd
import os

# Flask app initialization
app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')  # Allow all origins
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')  # Allow these headers
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')  # Allow these methods
    return response

# Database configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'postgresql://reinierbos:password@localhost:5432/hci_db'  # Default for local development
)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    strava_connected = db.Column(db.Boolean, default=False)

# Updated Shoes model
class Shoes(db.Model):
    __tablename__ = 'shoes'
    id = db.Column(db.Integer, primary_key=True)
    shoe_brand = db.Column(db.String(100), nullable=False)
    model_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    mileage = db.Column(db.Float, nullable=False)
    main_focus = db.Column(db.String(100), nullable=False)
    eco_friendly = db.Column(db.Boolean, nullable=False)
    foot_type = db.Column(db.String(100), nullable=False)
    cushioning_rate = db.Column(db.Integer, nullable=False)  # New column for cushioning rate
    durability_rate = db.Column(db.Integer, nullable=False)  # New column for durability rate
    pace_rate = db.Column(db.Integer, nullable=False)        # New column for pace rate
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Foreign key

    user = db.relationship('Users', backref='shoes')  # Establish relationship with User


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Check if email already exists
    if Users.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = Users(username=data['username'], email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'})


@app.route('/login_page', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data)
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Find the user by email
    user = Users.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Store the user ID in the session
    session['user_id'] = user.id

    return jsonify({'message': 'Login successful', 'username': user.username})


client_secret = "b3cdf712eff0cf8fef5332ba80012b6cf1fff435"

# Initialize the Strava client
client = Client()

# Replace with your application's Client ID and desired redirect URI
client_id = '140518'
redirect_uri = "http://127.0.0.1:5000/authorize"  # Must match Strava's settings

@app.route('/check_strava', methods=['GET'])
def check_strava_page():
    return render_template('check_strava.html')

@app.route('/connect_strava', methods=['GET'])
def connect_strava():
    authorize_url = client.authorization_url(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope="read_all"
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
    access_token = client.exchange_code_for_token(client_id=client_id, client_secret=client_secret, code=code)
    client.access_token = access_token['access_token']

    athlete = client.get_athlete()
    print(
    "For {id}, I now have an access token {token}".format(
        id=athlete.id, token=access_token
        )
    )
    # Mark the user as connected to Strava
    if 'user_id' in session:
        user = Users.query.get(session['user_id'])
        if user:
            user.strava_connected = True
            db.session.commit()

    return redirect('http://localhost:8081/')

# Route to display homepage information
@app.route('/profile', methods=['GET'])
def profile():
    # Assume 'client' is initialized and authenticated
    curr_athlete = client.get_athlete()
    
    # Extract relevant data from the athlete object
    athlete_data = {
        'id': curr_athlete.id,
        'firstname': curr_athlete.firstname,
        'lastname': curr_athlete.lastname,
    }

    return jsonify(athlete_data)

@app.route('/activities', methods=['GET'])
def activities():
    try:
        # Fetch the athlete's activities (limit to 10 for example)
        activities = client.get_activity()
        return jsonify(activities)
    except Exception as e:
        print(f"Error fetching activities: {e}")
        return jsonify({'error': 'Failed to fetch activities'}), 500


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
