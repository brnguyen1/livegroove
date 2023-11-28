import { useParams } from "react-router-dom"
import Header from "../components/Header"
import SongDisplay from "../components/SongDisplay";
import { useEffect, useState } from "react";
import { getSessions, startSession } from "../api/api";
import LobbyWaiting from "../components/LobbyWaiting";


export default function Lobby() {
    const { session_id } = useParams();
    const [sessionStart, setSessionStart] = useState(false);
    const [user_id, setUserId] = useState();

    useEffect(() => {
        getSessions(session_id).then(data => {
            setUserId(data["data"]["user_id"]);
            setSessionStart(data["data"]["session_status"]);
        })
    }, [session_id])

    const onStart = () => {
        startSession(session_id);
        setSessionStart(true);
    }

    return(
        <div className="flex h-screen w-screen content-center">
        <Header/>
        {sessionStart ? <SongDisplay session_id={session_id}/> : <LobbyWaiting onStart={onStart}/>}
        </div>
    )
}