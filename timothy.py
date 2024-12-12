import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

@app.route('/compare-shoes', methods=['GET'])
def process_data():
    try:
        # Load the CSV file
        df = pd.read_csv('./shoes.csv')
        # Convert to JSON and return the response
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
