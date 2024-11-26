from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os

# Flask app initialization
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8080"}})

# Database configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URI',
    'postgresql://reinierbos:password@localhost:5432/hci_db'  # Default for local development
)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

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

# Route to get data (example API endpoint)
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({'message': 'Hello from Flask backend!'})

# Route to submit data
@app.route('/api/submit', methods=['POST'])
def submit_data():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Example of processing submitted data
    return jsonify({'received': data})

# Route to register a new user
@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if not data or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Check if email already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 409

    # Hash the password and create a new user
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'})

# Route to log in a user
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    # Find the user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    return jsonify({'message': 'Login successful', 'username': user.username})

@app.route('/api/shoes', methods=['GET'])
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


if __name__ == '__main__':
    # Ensure the database tables are created before starting the app
    with app.app_context():
        db.create_all()
    app.run(debug=True)
