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

# HELPER FUNCTIONS (cos_sim, etc.) 
def get_sim_scores_to_song(item_session_matrix, song: int):
    res = [] 

    itemA = item_session_matrix[song]

    # Compute all similarity scores and append similaritiy scores that user has rated
    for i, song_scores in enumerate(item_session_matrix):
        if i == song:
            continue

        itemB = np.array(song_scores)
        res.append([i, np.dot(itemA, itemB) / (np.linalg.norm(itemA) * np.linalg.norm(itemB))])
    
    return res

def calc_missing_ratings(item_session_matrix, session: int):
    res = []

    # Predict scores for missing ratings
    for i in range(123):
        rating = item_session_matrix[i][session]
        if rating > 0:
            continue

        # Get similarity from users that HAVE rated missing items
        sim_scores = get_sim_scores_to_song(item_session_matrix, i)

        prediction = 0
        sim_sum = 0
        for item_j, sim in sim_scores:
            if item_session_matrix[item_j][session] == 0:
                continue
            prediction += sim * item_session_matrix[item_j][session]
            sim_sum += abs(sim)
        
        if sim_sum == 0:
            prediction = 3    
        else:
            prediction = prediction / sim_sum
        res.append((prediction, i))

    return res

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

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO sessions (session_name) VALUES (%s) RETURNING session_id""", (session_name,))
    sql_data = cursor.fetchall()[0]
    session_id = sql_data[0]
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
        stmt = "INSERT INTO ratings(user_id, song_id, rating, session_id) VALUES "
        for i in range(0, 123):
            stmt += f"({user_id}, {i}, 0, {session_id})"
            if i < 122:
                stmt += ", "
        # print(stmt)
        cursor.execute(stmt)
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
    user_id = int(data.get('user_id'))
    session_id = int(data.get('session_id'))
    song_id = int(data.get('song_id'))
    rating = int(data.get('rating'))
    
    global rated_songs
    rated_songs.append(int(song_id))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ratings SET user_id = (%s), session_id = (%s), song_id = (%s), rating = (%s) WHERE user_id = (%s) AND song_id = (%s)", (user_id, session_id,song_id,rating,user_id,song_id,))

    cursor.execute("SELECT rating FROM ratings WHERE session_id = (%s) AND song_id = (%s) AND rating > 0", (session_id,song_id,))
    ratings = cursor.fetchall()

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
    cursor.execute("SELECT session_id, song_id, rating FROM ratings")
    ratings_stmt_ret = cursor.fetchall()
    cursor.execute("SELECT MAX(session_id) from sessions")
    sessions_cnt = cursor.fetchall()[0][0] + 1
    song_session_matrix = [[0] * sessions_cnt for i in range(123)]
    
    for ses_id, sng_id, r in ratings_stmt_ret:
        song_session_matrix[sng_id][ses_id] = r
    
    predictions = calc_missing_ratings(song_session_matrix, session_id)
    print(len(predictions))
    
    predictions.sort(key = lambda x: x[0], reverse=True)
    # global top_songs
    top_songs = predictions[0:3]
    print("TOP 3 SONGS::", top_songs)
    conn.commit()
    conn.close()

    # return recommendation vector
    return jsonify({'top_songs': [i for pred, i in top_songs]})

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
    print(all_songs)
    # needs testing
    have_not_listened = {}
    for i in range(0, len(all_songs)):
        if not any(i in item for item in array_songs):
            have_not_listened[i] = all_songs[i]
    return jsonify({'songs_left': have_not_listened})

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
