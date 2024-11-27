from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
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

with app.app_context():
    db.create_all()

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
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Find the user by email
    user = Users.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful', 'username': user.username})


@app.route('/shoes', methods=['GET'])
def get_running_shoes():
    # Query all running shoes
    shoes = Shoes.query.all()

    # Format the data as a list of dictionaries
    shoe_data = [
        {
            "id": shoe.id,
            "shoe_brand": shoe.shoe_brand,
            "model_name": shoe.model_name,
            "price": shoe.price,
            "mileage": shoe.mileage,
            "main_focus": shoe.main_focus,
            "eco_friendly": shoe.eco_friendly,
            "foot_type": shoe.foot_type,
        }
        for shoe in shoes
    ]

    return jsonify({"shoes": shoe_data})

# Route to display homepage information
@app.route('/home', methods=['GET'])
def homepage():
    # For the sake of this example, assume a user with id 1 is logged in
    logged_in_user_id = 1  # Replace this with session management in a real app

    # Fetch user details
    user = User.query.get(logged_in_user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Fetch shoes associated with the user (assumes a relationship exists)
    # Adjust the database model if needed to include a relationship between User and Shoes
    shoes = Shoes.query.filter_by(user_id=logged_in_user_id).first()  # Assumes one shoe per user

    if not shoes:
        return jsonify({'error': 'Shoes not found for user'}), 404

    # Sample running data (replace with actual logic to fetch from the database)
    total_km_run = 256  # Example data, replace with real value
    remaining_km = shoes.mileage - total_km_run

    # Construct the response
    homepage_data = {
        'user': {
            'username': user.username,
            'email': user.email,
        },
        'shoes': {
            'brand': shoes.shoe_brand,
            'model': shoes.model_name,
            'remaining_km': remaining_km,
            'total_km_run': total_km_run,
        },
    }

    return jsonify(homepage_data)

@app.route('/associate_shoe', methods=['POST'])
def associate_shoe():
    data = request.json
    if not data or 'user_id' not in data or 'shoe_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Verify user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Verify shoe exists
    shoe = Shoes.query.get(data['shoe_id'])
    if not shoe:
        return jsonify({'error': 'Shoe not found'}), 404

    # Check if the shoe is already associated with another user
    if shoe.user_id:
        return jsonify({'error': 'Shoe is already associated with a user'}), 409

    # Associate shoe with the user
    shoe.user_id = data['user_id']
    db.session.commit()

    return jsonify({'message': f'Shoe "{shoe.model_name}" successfully associated with user {user.username}!'})



if __name__ == '__main__':
    # Ensure the database tables are created before starting the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
