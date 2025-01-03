-----------------------------------------------
# Flask Shoe Tracking Application

This is a Flask-based web application for managing user shoe data, including tracking mileage and cushioning percentage, connecting with Strava, and performing user authentication with JWT. The application uses SQLite as the database.

---

## Features

- User authentication (registration, login, logout) with JWT
- Manage user shoes: add, remove, and set main shoe
- Track mileage and cushioning percentage for shoes
- Strava integration for fetching activity data
- Fetch and compare shoe data

---

## Prerequisites

- Python 3.x

---

## Setup Instructions

### 1. Clone the Repository (not necessary if you have the files locally)

```
git clone https://github.com/TimothySchuur/HCI.git
cd HCI
```

### 2. Create and Activate a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Set Up the Database

#### Create the Database and Tables:

```
flask db upgrade
```

#### Populate the Database:


```
python populate_db.py
```

### 5. Run the Application

Start the Flask app:

```
python app.py
```

## Vue setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve -- --port 8081
```

## visite website in your browser
http://localhost:8081/login

 ---IMPORTANT---
 In your browser, view the page in devmode with the dimension of an Iphone 12 pro
