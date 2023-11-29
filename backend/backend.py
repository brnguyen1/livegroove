from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from collections import defaultdict
import psycopg2
from psycopg2 import sql
import os
from spotify_api import get_all_playlist_tracks, read_playlist_sp

app = Flask(__name__)
CORS(app)
# SQLite database setup

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host="dpg-cldohdvgsrdc73flft6g-a.ohio-postgres.render.com",
            database="livegroove_sessions",
            user="livegroove_sessions_user",
            password=os.getenv("DB_PASS")
        )
        print("Connection Successful")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        print("Connection not Successful")
        return None
    # conn = sqlite3.connect(DATABASE)
    # cursor = conn.cursor()

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


@app.route('/sessions', methods=['POST'])
def create_session():
    # Create a new session
    data = request.get_json()
    session_name = data.get('session_name')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO sessions (session_name) VALUES (%s) RETURNING session_id""", (session_name,))
    session_id = cursor.fetchall()[0]
    conn.commit()
    conn.close()
    # error handling
    cookie_user_id = request.cookies.get('user_id')
    if not (cookie_user_id is None):
        #This is an old user
        print("COOKIEEE", cookie_user_id)
    else:
        #This is a new user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (DEFAULT) RETURNING user_id")
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        response = make_response('Resposne')
        response.set_cookie('user_id', value=str(user_id))
        print("USER ID", user_id)
        #initialize ratings for user
        conn = get_db_connection()
        cursor = conn.cursor()
        for i in range(0, 123):
            cursor.execute("""INSERT INTO ratings(user_id, song_id, rating, session_id) VALUES (%s, %s, %s, %s)""", (user_id, i, 0, session_id,))
        conn.commit()
        conn.close()




    global active_sessions
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

    cookie_user_id = request.cookies.get('user_id')
    if not (cookie_user_id is None):
        #This is an old user
        print("COOKIE", cookie_user_id)
    else:
        #This is a new user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (user_id) VALUES (DEFAULT) RETURNING user_id")
        user_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        response = make_response('Resposne')
        response.set_cookie('user_id', value=str(user_id))
        print("USER ID", user_id)
        #initialize ratings for user
        conn = get_db_connection()
        cursor = conn.cursor()
        for i in range(0, 123):
            cursor.execute("""INSERT INTO ratings(user_id, song_id, rating, session_id) VALUES (%s, %s, %s, %s)""", (user_id, i, 0, session_id,))
        conn.commit()
        conn.close()

    


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

@app.route('/ratings', methods=['POST'])
def add_rating():
    # Add or update a rating
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    song_id = data.get('song_id')
    rating = data.get('rating')


    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ratings WHERE user_id = (%s) AND song_id = (%s)", (user_id, song_id,))
    try:
        isDup = cursor.fetchall()[0]
    except:
        isDup = None
    
    if isDup:
        cursor.execute("UPDATE ratings SET user_id = (%s), session_id = (%s), song_id = (%s), rating = (%s) WHERE user_id = (%s) AND song_id = (%s)", (user_id, session_id,song_id,rating,user_id,song_id,))
    else:
        cursor.execute("INSERT INTO ratings (user_id, session_id, song_id, rating) VALUES (%s,%s,%s,%s)", (user_id,session_id,song_id,rating,))

    # cursor.execute("INSERT INTO ratings (user_id, session_id, song_id, rating) VALUES (%s,%s,%s,%s) ON CONFLICT (user_id, session_id, song_id) DO UPDATE SET user_id = EXCLUDED.user_id, session_id = EXCLUDED.session_id, song_id = EXCLUDED.song_id, rating = EXCLUDED.rating", (user_id,session_id,song_id,rating,) )


    # update recommendation vector
    # vector of vectors of all user ratings in session
    # calculate average rating of song just played (the songid attached to the rating)
    # by taking the sum of all vector entries at songid (the current vec of vecs is array and not dict)
    # have to check if all users rated before playing next song or indices won't line up.


    # check if song has been played

    # 
    cursor.execute("SELECT DISTINCT user_id FROM ratings WHERE session_id = (%s)", (session_id,))
    array_users = cursor.fetchall()

    for i in range(0, len(array_users)):
        cursor.execute("SELECT * FROM ratings WHERE user_id = (%s) AND session_id = (%s)", (array_users[i], session_id,))
        user_ratings.append(cursor.fetchall())
    print(user_ratings)
    # user_ratings is an array of arrays of length 123 containing all ratings for that user 


    conn.commit()
    conn.close()

    # return recommendation vector
    return jsonify({'message': 'Rating added/updated successfully'})

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

# @app.route('/sessions/songs', methods=['GET'])
@app.route('/sessions/<int:session_id>/songs', methods=['GET'])
def display_songs(session_id):
    # used to display info of songs that haven't been played
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT song_id FROM ratings WHERE session_id = (%s)", (session_id,))
    array_songs = cursor.fetchall()
    conn.commit()
    conn.close()
    

    all_songs = get_all_playlist_tracks(read_playlist_sp(), "spotify:playlist:6wj42BHCJPop77cj6JgfLH")
    have_not_listened = []
    for i in range(0, len(all_songs)):
        if not any(i in item for item in array_songs):
            have_not_listened.append(all_songs[i])
    return jsonify({'songs_left': have_not_listened})

# @app.route('/sessions/<int:session_id>/ratings/<int:song_id>', methods=['POST','PUT'])
@app.route('/sessions/<int:session_id>/ratings', methods=['POST','PUT'])
# def update_songs_cf(session_id):
#     # update song in session ratings vector
#     #create a user-item matrix
#     #
#     user_ratings = []
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     # getting all rating of a user from a session
#     cursor.execute("SELECT DISTINCT user_id FROM ratings WHERE session_id = (%s)", (session_id,))
#     array_users = cursor.fetchall()

#     for i in range(0, len(array_users)):
#         cursor.execute("SELECT * FROM ratings WHERE user_id = (%s) AND session_id = (%s)", (array_users[i], session_id,))
#         user_ratings.append(cursor.fetchall())
#     print(user_ratings)

#     conn.commit()
#     conn.close()
#     return 0

@app.route('/sessions/<int:session_id>/select-song/<int:song_id>', methods=['POST'])
def select_song(session_id, song_id):
    # select song that will play next
    # used to track history of songs played to avoid redunant recommendations
    # only modify has_not_been_listened
    return jsonify({'message': "Song marked as listened to!"})

@app.route('/recommendations', methods=['GET'])
def get_recs():


    # return jsonify({'top_3': })
    return 0



@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    conn.close()



if __name__ == '__main__':
    app.run(debug=True)
