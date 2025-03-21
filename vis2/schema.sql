-- SQLite schema for flask app

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Optional: Add some sample users for testing
-- In a real app, you would hash the passwords
INSERT INTO users (username, password) VALUES ('admin', 'admin123');
INSERT INTO users (username, password) VALUES ('test', 'test123');