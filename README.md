# hci-proto

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

-----------------------------------------------
# Flask Shoe Tracking Application

This is a Flask-based web application for managing user shoe data, including tracking mileage and cushioning percentage, connecting with Strava, and performing user authentication with JWT. The application uses SQLite as the database.

---

## Features

- User authentication (registration, login, logout) with JWT
- Manage user shoes: add, remove, and set main shoe
- Track mileage and cushioning percentage for shoes
- Strava integration for fetching activity data
- Fetch and compare shoe data from a CSV file

---

## Prerequisites

- Python 3.x
- Virtual environment (recommended)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/TimothySchuur/HCI.git
cd HCI
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

#### Create the Database and Tables:

```bash
flask db upgrade
```

#### Populate the Database:


```bash
python populate_db.py
```

### 5. Run the Application

Start the Flask app:

```bash
python app.py
```