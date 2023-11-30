import Header from "../components/Header";
import {createSession} from "../api/api"
import { useNavigate } from "react-router-dom";

export default function Home(){
    const navigate = useNavigate();

    const onCreateRoom = async () => {
        await createSession().then(data => {
            navigate("/" + data["data"]["session_id"])
        })
    }

    return(
        <div className="flex h-screen w-screen">
            <Header/>
            
            <div className="flex flex-col border border-2 h-2/3 w-1/2 m-auto">
                <div className="flex h-max w-full m-auto">
                    <button className="bg-green-500 hover:bg-green-700 text-white font-bold py-4 px-10 rounded m-auto" onClick={onCreateRoom}>
                        Create a room
                    </button>
                </div>
                {/* <div className="flex h-max w-full m-auto">
                    <button className="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-auto">
                        Join a room
                    </button>
                </div> */}

            </div>
        </div>
    )
}