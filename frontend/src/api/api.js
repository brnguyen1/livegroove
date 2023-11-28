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

function sendRating(session_id, song_id, rating) {
    return axios.put(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id + "/ratings/" + song_id, {"rating": rating});
}

export {createSession, getSessions, startSession, selectSong, sendRating}