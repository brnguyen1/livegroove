from flask import Flask, request, jsonify
from flask_cors import CORS
from collections import defaultdict
import sqlite3

app = Flask(__name__)
CORS(app)
# SQLite database setup
DATABASE = "database.db"

# def init_db():
#     conn = sqlite3.connect(DATABASE)
#     cursor = conn.cursor()

#     # Create tables if they don't exist
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS sessions (
#         session_id SERIAL PRIMARY KEY,
#         session_name VARCHAR
#     )
#     """)

#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS users (
#         user_id SERIAL PRIMARY KEY
#     )
#     """)
    
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS ratings (
#         user_id SERIAL,
#         session_id SERIAL,
#         song_id INTEGER,
#         rating INTEGER,
#         CONSTRAINT fk_sessions
#         FOREIGN KEY(session_id) 
# 	      REFERENCES sessions(sessions_id),
#         CONSTRAINT fk_users
#         FOREIGN KEY(user_id)
#         REFERENCES users(user_id)
#     )
#     """)

#     conn.commit()
#     conn.close()

# # Initialize the database
# init_db()

# API endpoints

# am i allowed global variables here?
active_sessions = {}
session_users = defaultdict(int)
session_ids = defaultdict(str)
session_names = defaultdict(int)
user_ids_sessions = {}
session_id = 0
user_id = 0

@app.route('/sessions', methods=['POST'])
def create_session():
    # Create a new session
    session_id += 1
    data = request.get_json()
    session_name = data.get('session_name')
    # error handling
    session_names[session_name] = session_id
    try:
        user_id = request.cookies.get('user_id')
        user_ids_sessions[session_id] = [user_id]
    except:
        user_id += 1
        reponse = Flask.make_response()
        reponse.set_cookies('user_id', value=user_id)
        user_ids_sessions[session_id] = [user_id]
    # conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO sessions (session_name) VALUES (?)", (session_name,))
    # session_id = cursor.lastrowid
    # conn.commit()
    # conn.close()
    
    active_sessions[session_id] = False

    return jsonify({'session_id': session_id})

@app.route('/sessions/<int:session_id>', methods=['GET'])
def join_session(session_id):
    # Join a session
    # Add your logic to keep track of user info

    # Once user joins the session, add a user id
    # how to assign rating to a user?

    # When the user presses a button and uses the add rating call, 
    # their user id needs to be present

    # conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO user (user_id) VALUES ('DEFAULT')")
    # user_id = cursor.lastrowid
    # conn.commit()
    # conn.close()
    
    session_users[session_id] += 1
    user_id = session_users[session_id]

    # send user id and status in message
    # need to keep track of this user id in the browser and attach it to the button event
    # when button is clicked, send user_id as part of adding rating
    return jsonify({'message': 'Joined session successfully', 'user_id': user_id, 'session_status': active_sessions[session_id]})

@app.route('/sessions/<int:session_id>', methods=['POST'])
def start_session(session_id):
    # Start a session
    # Add your logic for starting a session
    active_sessions[session_id] = True
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

@app.route('/sessions/songs', methods=['GET'])
def display_songs():
    # used to display info of songs that haven't been played
    return 0

@app.route('/sessions/<int:session_id>/ratings/<int:song_id>', methods=['POST','PUT'])
def update_songs_cf(session_id, song_id):
    # update song in session ratings vector
    # update user-user CF model every x requests
    return 0

@app.route('/sessions/<int:session_id>/select-song/<int:song_id>', methods=['POST'])
def select_song(session_id, song_id):
    # select song that will play next
    # used to track history of songs played to avoid redunant recommendations
    return 0

if __name__ == '__main__':
    app.run(debug=True)
