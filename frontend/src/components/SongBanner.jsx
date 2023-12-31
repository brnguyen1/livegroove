import SampleInfo from "../assets/sample_info.json"

export default function SongBanner(props){
    let { image_url, song_name, artist, onQueue, selected } = props

    let border = selected ? "-2" : ""

    return(
    <div className={"flex border" + border + " rounded h-12 w-4/5 m-auto"}>
        <div className="bg-green-700 w-1/5 h-full mr-auto" >
            <img className="object-cover h-full w-full" src={image_url}/>
        </div>
            
        <div className="flex w-4/5">
            <div className="flex w-5/6 m-auto">
                <span className="m-auto">
                    {song_name + " by " + artist}
                </span>
            </div>
            
            <div className="flex w-1/6 m-auto" onClick={onQueue}>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-8 m-auto" viewBox="0 0 448 512"><path d="M0 64C0 46.3 14.3 32 32 32H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32C14.3 96 0 81.7 0 64zM192 192c0-17.7 14.3-32 32-32H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H224c-17.7 0-32-14.3-32-32zm32 96H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H224c-17.7 0-32-14.3-32-32s14.3-32 32-32zM0 448c0-17.7 14.3-32 32-32H416c17.7 0 32 14.3 32 32s-14.3 32-32 32H32c-17.7 0-32-14.3-32-32zM127.8 268.6L25.8 347.9C15.3 356.1 0 348.6 0 335.3V176.7c0-13.3 15.3-20.8 25.8-12.6l101.9 79.3c8.2 6.4 8.2 18.9 0 25.3z"/>
                </svg>
            </div>

        </div>
    </div>
    )
}