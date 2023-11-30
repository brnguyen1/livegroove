import { useParams } from "react-router-dom"
import Header from "../components/Header"
import { useEffect, useState } from "react";
import { getSessions, sendRating, startSession } from "../api/api";
import LobbyWaiting from "../components/LobbyWaiting";
import CurrentSong from "../components/CurrentSong";
import SongBanner from "../components/SongBanner";
import SampleInfo from "../assets/sample_info.json";


export default function Lobby() {
    const { session_id } = useParams();
    const [sessionStart, setSessionStart] = useState(false);
    const [user_id, setUserId] = useState(null);
    const [song_id, setSongId] = useState(null);
    const [recommendedSongs, setRecommendedSongs] = useState([]);
    const [queuedSong, setQueuedSong] = useState(null)

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
            setRecommendedSongs(res["data"]["top_songs"])
            console.log(recommendedSongs)
        })
    }

    const onNext = () => {
        if(queuedSong) {
            setSongId(queuedSong)
            setQueuedSong(null)
            setRecommendedSongs(null)
        }
    }

    // Song Display
    let song_display =
    <div className="flex flex-col h-5/6 w-2/3 border my-24 m-auto">
        
        {song_id ? <CurrentSong onRate={onRate} onNext={onNext} song_name={SampleInfo[song_id]["track"]} image_url={SampleInfo[song_id]["image"]} artist={SampleInfo[song_id]["artist"]}/> : null}
        <div className="flex flex-col my-auto gap-y-5">
                {recommendedSongs ? recommendedSongs.map(song => {
                    return <SongBanner key={song} song_name={SampleInfo[song]["track"]} image_url={SampleInfo[song]["image"]} artist={SampleInfo[song]["artist"]} onQueue={() => setQueuedSong(song)} selected={queuedSong === song}/>
                }) : null}
        </div>

    </div>
 
    return(
        <div className="flex h-screen w-screen content-center">
        <Header/>
        {sessionStart ? song_display : <LobbyWaiting onStart={onStart}/>}
        </div>
    )
}