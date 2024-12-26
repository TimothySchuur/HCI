import csv
from app import db
from app import Shoes
from flask import Flask

# Flask app context setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hci.db'  # Update with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def import_shoes_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)  # Read CSV as a dictionary for easy mapping
        shoes_list = []
        
        for row in reader:
            shoe = Shoes(
                shoe_brand=row['shoe_brand'],
                model_name=row['model_name'],
                price=float(row['price']),
                mileage=int(row['mileage']),
                main_focus=row['main_focus'],
                eco_friendly=row['eco_friendly'].lower() == 'true',
                foot_type=row['foot_type'],
                cushioning_rate=int(row['cushioning_rate']),
                durability_rate=int(row['durability_rate']),
                pace_rate=int(row['pace_rate']),
                gender=row['gender']
            )
            shoes_list.append(shoe)
        
        try:
            db.session.bulk_save_objects(shoes_list)  # Bulk insert for better performance
            db.session.commit()
            print(f"Successfully imported {len(shoes_list)} shoes into the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error importing shoes: {e}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure tables are created
        import_shoes_from_csv('shoes.csv')  # Replace with the path to your CSV file
