from flask import Flask, jsonify, request, render_template, session, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from stravalib import Client
import time
import pandas as pd
from dotenv import load_dotenv
from flask_jwt_extended import jwt_required, get_jwt_identity


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://reinierbos:password@localhost:5432/hci_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hci.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

@app.before_request
def enable_foreign_keys():
    db.session.execute('PRAGMA foreign_keys = ON;')

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

    user_shoes = UserShoes.query.filter_by(user_id=user.id).all()
    main_shoe = UserShoes.query.filter_by(id=user.main_shoe_id).first() if user.main_shoe_id else None

    user_shoes_data = [
        {
            'id': shoe.id,
            'shoe_brand': shoe.shoe.shoe_brand,
            'model_name': shoe.shoe.model_name,
            'mileage_run': shoe.mileage_run,
            'mileage_remaining': shoe.mileage_remaining,
            'cushioning_percentage': (shoe.mileage_remaining / shoe.total_mileage_allowed) * 100
        }
        for shoe in user_shoes
    ]

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

    return jsonify({
        'username': user.username,
        'mainShoe': main_shoe_data,
        'userShoes': user_shoes_data
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
        activities = client.get_activities(limit=10)
        print(activities)
        
        # Extract relevant information and preprocess distance
        activities_list = []
        for activity in activities:
            activities_list.append({
                'id': activity.id,  # Add the unique ID of the activity
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
    # Get the data from the request
    data = request.get_json()
    activity_id = data.get('activity_id')

    if not activity_id:
        return jsonify({'error': 'Missing activity_id'}), 400

    try:
        # Fetch activities from the client
        activities = client.get_activities(limit=10)
        
        # Find the activity with the given activity_id
        selected_activity = next((a for a in activities if a.id == activity_id), None)

        if not selected_activity:
            return jsonify({'error': 'Activity not found'}), 404

        # Extract the distance from the selected activity
        distance = selected_activity.distance.magnitude if hasattr(selected_activity.distance, 'magnitude') else 0
        distance_km = distance / 1000  # Convert to kilometers
        print(f"Selected activity distance (km): {distance_km}")

        # Get the current user from the JWT token
        current_user_email = get_jwt_identity()
        user = Users.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Get the user's shoe
        user_shoe = (
            UserShoes.query.filter_by(id=user.main_shoe_id).first() or
            UserShoes.query.filter_by(user_id=user.id).first()
        )

        if not user_shoe:
            return jsonify({'error': 'No shoe found for the user'}), 404

        # Update mileage_run
        user_shoe.mileage_run += distance_km
        print(f"Updated mileage_run: {user_shoe.mileage_run}")

        # Calculate remaining mileage and update the mileage_remaining field
        user_shoe.mileage_remaining = max(0, user_shoe.total_mileage_allowed - user_shoe.mileage_run)
        print(f"Updated mileage_remaining: {user_shoe.mileage_remaining}")

        # Commit changes to the database
        db.session.commit()

        return jsonify({'mileage_remaining': user_shoe.mileage_remaining}), 200

    except Exception as e:
        print(f"Error updating activities: {e}")
        return jsonify({'error': 'Failed to update activity'}), 500


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

    shoe_id = request.json.get('shoe_id')
    shoe = Shoes.query.get(shoe_id)

    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    user_shoe = UserShoes(
        user_id=user.id,
        shoe_id=shoe.id,
        mileage_run=0,
        mileage_remaining=shoe.mileage,
        total_mileage_allowed=shoe.mileage
    )
    db.session.add(user_shoe)
    db.session.commit()

    return jsonify({'message': f'Shoe {shoe.shoe_brand} - {shoe.model_name} added to user'}), 200


@app.route('/user/set-main-shoe', methods=['POST'])
@jwt_required()
def set_main_shoe():
    data = request.get_json()
    model_name = data.get('model_name')

    if not model_name:
        return jsonify({'error': 'Model name is required'}), 400

    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Find the shoe_id for the given model_name
    shoe = Shoes.query.filter_by(model_name=model_name).first()

    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    # Find the user_shoe entry with the corresponding shoe_id
    user_shoe = UserShoes.query.filter_by(user_id=user.id, shoe_id=shoe.id).first()

    if not user_shoe:
        return jsonify({'error': 'User does not own this shoe'}), 400

    # Set the main shoe
    user.main_shoe_id = user_shoe.id
    db.session.commit()

    return jsonify({'message': 'Main shoe set successfully'}), 200




@app.route('/user/mileage-run', methods=['GET'])
@jwt_required()
def get_mileage_run():
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Get the user's shoe data
    user_shoe = (
            UserShoes.query.filter_by(id=user.main_shoe_id).first() or
            UserShoes.query.filter_by(user_id=user.id).first()
        )
    print(user_shoe)

    if not user_shoe:
        return jsonify({'error': 'No shoe data found for user'}), 404

    return jsonify({
        'mileage_run': user_shoe.mileage_run,
        'mileage_remaining': user_shoe.mileage_remaining,  # Include total_mileage_allowed
    }), 200


@app.route('/user/remove-shoe/<int:shoe_id>', methods=['DELETE'])
@jwt_required()
def remove_shoe(shoe_id):
    current_user_email = get_jwt_identity()
    user = Users.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    user_shoe = UserShoes.query.filter_by(id=shoe_id, user_id=user.id).first()

    if not user_shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    # Check if the shoe to be removed is the main shoe
    if user.main_shoe_id == shoe_id:
        # Unset the main shoe before removing it
        user.main_shoe_id = None
        db.session.commit()

    try:
        # Delete the shoe from user_shoes
        db.session.delete(user_shoe)
        db.session.commit()
        return jsonify({'message': 'Shoe removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


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