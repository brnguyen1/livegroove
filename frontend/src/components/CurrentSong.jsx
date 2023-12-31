import { useState } from "react";
import { Rating } from "@mui/material";

export default function CurrentSong(props) {
    let {onRate, onNext, image_url, song_name, artist} = props;
    const [rating, setRating] = useState(0)

    return(
            <div className="border w-full h-3/5">
                <div className="bg-green-100 h-4/5 w-full">
                    <img className="object-cover h-full w-full" src={image_url} />
                    <div className="flex h-1/8 w-max m-auto">
                        {song_name + " by " + artist}
                    </div>
                </div>
                <div className="grid grid-cols-11 h-1/5">
                    <div className="flex col-start-5 col-span-3 m-auto">
                        <Rating
                            value={rating}
                            onChange={(event, new_rating) => {
                                setRating(new_rating);
                                onRate(new_rating);
                            }}
                            size="large"
                        />
                    </div>
                    <div className="flex col-start-10 m-auto" onClick={() => {
                        setRating(0);
                        onNext();
                        }}>
                        <svg className="h-12" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 512">
                            <path d="M52.5 440.6c-9.5 7.9-22.8 9.7-34.1 4.4S0 428.4 0 416V96C0 83.6 7.2 72.3 18.4 67s24.5-3.6 34.1 4.4l192 160L256 241V96c0-17.7 14.3-32 32-32s32 14.3 32 32V416c0 17.7-14.3 32-32 32s-32-14.3-32-32V271l-11.5 9.6-192 160z"/>
                        </svg>
                    </div>
                    
                </div>
            </div>
    )
}