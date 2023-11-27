import axios from "axios";

// SESSIONS

async function createSession() {
    return await axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions");    
}

function getSessions(session_id) {
    axios.get(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id);
}

function startSession(session_id) {
    axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id);
}

// SONGS
function selectSong(session_id, song_id){
    axios.post(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id + "/select-song/" + song_id)
}

function sendRating(session_id, song_id, rating) {
    axios.put(import.meta.env.VITE_BACKEND_URL + "/sessions/" + session_id + "/ratings/" + song_id, {"rating": rating});
}

export {createSession, getSessions, startSession, selectSong, sendRating}