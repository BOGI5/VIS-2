from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json
import os
import sqlite3
from datetime import datetime
from functools import wraps
import secrets
import subprocess

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# SQLite Database
DATABASE = 'flask_app.db'

# JSON file to store table data
TABLE_DATA_FILE = 'table_data.json'
INFO_FILE = "agent/info.json"

# Check if JSON file exists, create if not
if not os.path.exists(TABLE_DATA_FILE):
    with open(TABLE_DATA_FILE, 'w') as f:
        json.dump([], f)

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create users table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Insert sample users if none exist
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('admin', 'admin123'))
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('test', 'test123'))
    
    conn.commit()
    conn.close()

# Initialize database when the app starts
init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Database connection
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Routes
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return render_template('login.html')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            cursor.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            
            if user and user['password'] == password:  # In a real app, use password hashing
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash('Login successful', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password', 'danger')
            
            conn.close()
        except sqlite3.Error as err:
            flash(f'Database error: {err}', 'danger')
        
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not username or not password or not confirm_password:
            flash('Please fill out all fields', 'danger')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if username already exists
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                flash('Username already exists', 'danger')
                conn.close()
                return render_template('signup.html')
            
            # Insert new user
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                          (username, password))  # In a real app, hash the password
            conn.commit()
            
            flash('Account created successfully. Please login.', 'success')
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.Error as err:
            flash(f'Database error: {err}', 'danger')
        
    return render_template('signup.html')

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        with open(TABLE_DATA_FILE, 'r') as f:
            table_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        table_data = []
    
    return render_template('dashboard.html', username=session.get('username'), table_data=table_data)

@app.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    name = request.form.get('name')
    entry_id = request.form.get('id')
    money = request.form.get('money')
    
    if not name or not entry_id or not money:
        flash('Please fill all fields', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        money = float(money)
    except ValueError:
        flash('Money must be a number', 'danger')
        return redirect(url_for('dashboard'))
    
    try:
        with open(TABLE_DATA_FILE, 'r') as f:
            table_data = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        table_data = []
    
    # Check if ID already exists
    for entry in table_data:
        if entry['id'] == entry_id:
            flash('ID already exists', 'danger')
            return redirect(url_for('dashboard'))
    
    # Add new entry
    new_entry = {
        'name': name,
        'id': entry_id,
        'money': money,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    table_data.append(new_entry)
    
    with open(TABLE_DATA_FILE, 'w') as f:
        json.dump(table_data, f, indent=4)

    with open(INFO_FILE, 'w') as f:
        json.dump(new_entry, f, indent=4)
    
    flash('Entry added successfully', 'success')

    agent_script_path = os.path.join(os.path.dirname(__file__), 'agent', 'app.py')
    try:
        subprocess.run(
            ["conda", "run", "-n", "vis2", "python", agent_script_path],
            check=True
        )
    except subprocess.CalledProcessError as e:
        flash(f'Error running agent/app.py: {e}', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/remove_entry/<entry_id>', methods=['POST'])
@login_required
def remove_entry(entry_id):
    try:
        with open(TABLE_DATA_FILE, 'r') as f:
            table_data = json.load(f)
        
        # Filter out the entry to remove
        updated_data = [entry for entry in table_data if entry['id'] != entry_id]
        
        if len(updated_data) == len(table_data):
            flash('Entry not found', 'danger')
        else:
            with open(TABLE_DATA_FILE, 'w') as f:
                json.dump(updated_data, f, indent=4)
            flash('Entry removed successfully', 'success')
    except (json.JSONDecodeError, FileNotFoundError):
        flash('Error processing data file', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)