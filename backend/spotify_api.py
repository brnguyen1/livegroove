import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os

# Set up your credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
redirect_uri = 'http://localhost:8000/'

# Set up Spotify API connection
def get_all_playlist_tracks(sp, playlist_id):
    offset = 0
    limit = 100
    all_tracks = []

    while True:
        results = sp.playlist_items(playlist_id, fields='items(track(name,album))', limit=limit, offset=offset)
        tracks = results.get('items', [])

        if not tracks:
            break
        
        for track in tracks:
            all_tracks.extend((track['track']['name'], track['track']['album']['images'][2]['url']))

        offset += limit

    return all_tracks


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-read-private'))


playlist_id="spotify:playlist:6wj42BHCJPop77cj6JgfLH"
fields='items(track(name))'


tracks = get_all_playlist_tracks(sp, playlist_id)
print(len(tracks))
for i in range(len(tracks)):
    print(tracks[i])

