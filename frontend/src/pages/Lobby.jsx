import { useParams } from "react-router-dom"
import Header from "../components/Header"
import SongDisplay from "../components/SongDisplay";


export default function Lobby() {
    let { session_id } = useParams();

    return(
        <div className="flex h-screen w-screen content-center">
        <Header/>
        <SongDisplay/>
        </div>
    )
}