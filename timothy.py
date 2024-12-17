import pandas as pd
from flask import Flask, jsonify, render_template, redirect
from flask_cors import CORS
from requests_oauthlib import OAuth2Session
from oauthlib.oauth2 import BackendApplicationClient

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Replace with your application's Client ID and Client Secret
client_id = '140518'
client_secret = 'your_client_secret'
redirect_uri = "http://127.0.0.1:5000/authorize"  # Must match Strava's settings

# Create OAuth2 session
client = OAuth2Session(client_id, redirect_uri=redirect_uri)

@app.route('/compare', methods=['GET'])
def process_data():
    try:
        # Load the CSV file
        df = pd.read_csv('./shoes.csv')
        # Convert to JSON and return the response
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/check_strava', methods=['GET'])
def check_strava_page():
    return render_template('check_strava.html')

@app.route('/connect_strava', methods=['GET'])
def connect_strava():
    # Get authorization URL from Strava API
    authorize_url, state = client.authorization_url('https://www.strava.com/oauth/authorize')
    print(authorize_url)
    return redirect(authorize_url)

if __name__ == "__main__":
    app.run(debug=True)
