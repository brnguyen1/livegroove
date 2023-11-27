import { useParams } from "react-router-dom"
import Header from "../components/Header"
import SongDisplay from "../components/SongDisplay";
import { useEffect, useState } from "react";


export default function Lobby() {
    const { session_id } = useParams();
    const [user_id, setUserId] = useState();

    useEffect(() => {
        
    })

    return(
        <div className="flex h-screen w-screen content-center">
        <Header/>
        <SongDisplay session_id={session_id}/>
        </div>
    )
}