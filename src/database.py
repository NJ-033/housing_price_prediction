import sqlite3
import os

DB_NAME = 'data/housing_data.db'

def get_connection():
    try:
        os.makedirs('data', exist_ok=True)
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # To return dictionary-like objects
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite: {e}")
        return None

def initialize_database():
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        
        # Create default admin user if not exists
        cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin123')")
        
        # Create Predictions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                bedrooms INTEGER,
                bathrooms INTEGER,
                floor_area REAL,
                land_size REAL,
                subdivision TEXT,
                build_year INTEGER,
                predicted_price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        return False

def authenticate_user(username, password):
    conn = get_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        query = "SELECT id, username FROM users WHERE username = ? AND password = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return dict(user)
        return None
    except sqlite3.Error as e:
        print(f"Error authenticating: {e}")
        return None

def save_prediction(user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price):
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO predictions 
            (user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (user_id, bedrooms, bathrooms, floor_area, land_size, subdivision, build_year, predicted_price))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error saving prediction: {e}")
        return False

def get_user_predictions(user_id):
    conn = get_connection()
    if not conn:
        return []
    
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        records = [dict(row) for row in cursor.fetchall()]
        cursor.close()
        conn.close()
        return records
    except sqlite3.Error as e:
        print(f"Error fetching predictions: {e}")
        return []

def delete_prediction(prediction_id):
    conn = get_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        query = "DELETE FROM predictions WHERE id = ?"
        cursor.execute(query, (prediction_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"Error deleting prediction: {e}")
        return False
