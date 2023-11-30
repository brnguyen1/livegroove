from flask import Flask, request, jsonify, make_response, render_template
from flask_cors import CORS
from collections import defaultdict
import psycopg2
import numpy as np
from psycopg2 import sql
import os
from spotify_api import get_all_playlist_tracks, read_playlist_sp
from itertools import islice

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
rated_songs = []
top_songs = {}

@app.route('/sessions', methods=['POST'])
def create_session():
    # Create a new session
    data = request.get_json()
    session_name = data.get('session_name')

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO sessions (session_name) VALUES (%s) RETURNING session_id""", (session_name,))
    session_id = cursor.fetchall()[0][0]
    conn.commit()
    conn.close()

    global active_sessions
    active_sessions[session_id[0]] = False

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
    
    global rated_songs
    rated_songs.append(int(song_id))


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

    
    
    cursor.execute("SELECT rating FROM ratings WHERE session_id = (%s) AND song_id = (%s)", (session_id,song_id,))
    ratings = cursor.fetchall()
    song_recommend = {}

    if any(0 in item for item in ratings):
        # Dont do math yet
        print("Still waiting on other users in session to rate song...")
    else:
        # Do Math
        # AVG RATING
        average_rating = 0
        for i in range(0, len(ratings)):
            average_rating += int(ratings[i][0])
        average_rating = float(average_rating)/float(len(ratings))
        # r_u,j ->
        print("AVERAGE:::", average_rating)
        # -----------------------------------------------------------------------------------------
        #COS SIM
        # rated_songs.append(song_id)
        catalog_rated = []
        # get list of song_ids in session, loop through to get ratings of that is not equal to song_id
        cursor.execute("SELECT DISTINCT song_id FROM ratings")
        song_ids = cursor.fetchall()
        for i in range(0, len(song_ids)):
            if song_ids[i][0] not in rated_songs:
                catalog_rated.append(song_ids[i])

        compare_ratings = []
        cursor.execute("SELECT rating FROM ratings WHERE song_id = (%s)", (song_id))
        current_song_ratings = cursor.fetchall()


        the_song = np.array(current_song_ratings).T

        for i in range(0, len(catalog_rated)):
            cursor.execute("SELECT rating FROM ratings WHERE song_id = (%s)", (catalog_rated[i],))
            catalog_ratings = cursor.fetchall()

            comp_song = np.array(catalog_ratings)
            
            song_recommend[catalog_rated[i]] = np.dot(the_song, comp_song) / np.linalg.norm(the_song) * np.linalg.norm(comp_song)
    
    sorted_song_recommend =  dict(sorted(song_recommend.items(), key=lambda item: item[1], reverse=True))
    global top_songs
    top_songs = dict(islice(sorted_song_recommend.items(),3))

    print("TOP 3 SONGS::", top_songs)
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
    # needs testing
    have_not_listened = {}
    for i in range(0, len(all_songs)):
        if not any(i in item for item in array_songs):
            have_not_listened[i] = all_songs[i]
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
    global top_songs

     
    global have_not_listened
    for key in have_not_listened:
        if key == song_id:
            del have_not_listened[key]
    return jsonify({'message': "Song marked as listened to!"})

@app.route('/recommendations', methods=['GET'])
def get_recs():

    global top_songs
    # getting ints already sorted name, image, and artist of the top 3 tracks
    return jsonify({'top3': top_songs})



@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    conn.close()



if __name__ == '__main__':
    app.run(debug=True)
