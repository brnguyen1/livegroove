import axios from "axios";

// SESSIONS

function createSession() {
    return axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions", {"session_name": 1}, {headers: {'Content-Type': 'application/json'}});    
}

function getSessions(session_id) {
    return axios.get(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id, {headers: {'Content-Type': 'application/json'}});
}

function startSession(session_id) {
    return axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id, {headers: {'Content-Type': 'application/json'}});
}

// SONGS
function selectSong(session_id, song_id){
    return axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id + "/select-song/" + song_id, {headers: {'Content-Type': 'application/json'}})
}

function sendRating(session_id, user_id, song_id, rating) {
    return axios.post(import.meta.env.VITE_BACKEND_URL + "/ratings", {"session_id": session_id, "user_id":user_id, "song_id":song_id, "rating": rating});
}

function getRemainingSongInfo(session_id){
    return axios.get(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id + "/songs")
}

export {createSession, getSessions, startSession, selectSong, sendRating, getRemainingSongInfo}