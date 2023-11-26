import SongBanner from "./SongBanner";

export default function SongDisplay() {
    return(
        <div className="flex flex-col h-5/6 w-2/3 border m-auto">
            <div className="bg-green-100 w-full h-3/5">

            </div>
            <div className="flex flex-col my-auto gap-y-5">
                <SongBanner image="word" song_name="Song1"/>
                <SongBanner image="word" song_name="Song2"/>
                <SongBanner image="word" song_name="Song3"/>

            </div>
        </div>
    )
}