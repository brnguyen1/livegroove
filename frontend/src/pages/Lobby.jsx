import { useParams } from "react-router-dom"
import Header from "../components/Header"
import SongDisplay from "../components/SongDisplay";
import { useEffect, useState } from "react";
import { getSessions, sendRating, startSession } from "../api/api";
import LobbyWaiting from "../components/LobbyWaiting";


export default function Lobby() {
    const { session_id } = useParams();
    const [sessionStart, setSessionStart] = useState(false);
    const [user_id, setUserId] = useState(null);
    const [song_id, setSongId] = useState(null);
    const [recommendedSongs, setRecommendedSongs] = useState(null);
    useEffect(() => {
        getSessions(session_id).then(data => {
            setUserId(data["data"]["user_id"]);
            setSessionStart(data["data"]["session_status"]);
        })
    }, [session_id])

    // ONCLICK EVENTS
    const onStart = () => {
        startSession(session_id);
        setSongId(Math.floor(Math.random()*123))
        setSessionStart(true);
    }

    const onRate = (rating) => {
        sendRating(session_id, user_id, song_id, rating).then(res => {
            console.log(res)
        })
    }

    return(
        <div className="flex h-screen w-screen content-center">
        <Header/>
        {sessionStart ? <SongDisplay session_id={session_id} onRate={onRate}/> : <LobbyWaiting onStart={onStart}/>}
        </div>
    )
}