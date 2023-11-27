import { startSession } from "../api/api"

export default function LobbyWaiting(props){
    let { session_id } = props

    const onStart = () => {
        startSession(session_id)
    }

    return(
        <div className="flex flex-col border border-2 h-2/3 w-1/2 m-auto">
            <div className="flex h-max w-full m-auto">
                <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-4 px-10 rounded m-auto" onClick={onStart}>
                    Start
                </button>
            </div>
        </div>
    )
}