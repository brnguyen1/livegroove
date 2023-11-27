from flask import Flask, request, jsonify
from flask_cors import CORS
# import sqlite3

app = Flask(__name__)
CORS(app)
# SQLite database setup
# DATABASE = "database.db"

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # Create tables if they don't exist
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS sessions (
#         session_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         session_name TEXT NOT NULL
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS ratings (
#         user_id INTEGER,
#         session_id INTEGER,
#         song_id INTEGER,
#         rating INTEGER,
#         PRIMARY KEY (user_id, session_id, song_id)
#     )
#     """)

#     conn.commit()
#     conn.close()

# # Initialize the database
# init_db()

# API endpoints

@app.route('/sessions', methods=['POST'])
def create_session():
    # Create a new session
    data = request.get_json()
    session_name = data.get('session_name')
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sessions (session_name) VALUES (?)", (session_name,))
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return jsonify({'session_id': session_id})

@app.route('/sessions/<int:session_id>', methods=['GET'])
def join_session(session_id):
    # Join a session
    # Add your logic to keep track of user info
    return jsonify({'message': 'Joined session successfully'})

@app.route('/sessions/<int:session_id>', methods=['POST'])
def start_session(session_id):
    # Start a session
    # Add your logic for starting a session
    return jsonify({'message': 'Session started successfully'})

# @app.route('/ratings', methods=['POST'])
# def add_rating():
#     # Add or update a rating
#     data = request.get_json()
#     user_id = data.get('user_id')
#     session_id = data.get('session_id')
#     song_id = data.get('song_id')
#     rating = data.get('rating')

#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT OR REPLACE INTO ratings (user_id, session_id, song_id, rating)
#         VALUES (?, ?, ?, ?)
#     """, (user_id, session_id, song_id, rating))
#     conn.commit()
#     conn.close()

#     return jsonify({'message': 'Rating added/updated successfully'})

# @app.route('/ratings/<int:session_id>', methods=['GET'])
# def get_rating_vectors(session_id):
#     # Get rating vectors for the specified session
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT user_id, song_id, rating
#         FROM ratings
#         WHERE session_id = ?
#     """, (session_id,))
#     rating_vectors = cursor.fetchall()
#     conn.close()

#     return jsonify({'rating_vectors': rating_vectors})

# Add more endpoints as needed

if __name__ == '__main__':
    app.run(debug=True)
