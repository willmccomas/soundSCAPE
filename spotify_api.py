import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

load_dotenv()

# Dictionary for albums not on spotify

CUSTOM_ALBUMS = {
    "owl_pharaoh": {
        "name": "Owl Pharaoh",
        "artist": "Travis Scott",
        "release_date": "2013-05-21",
        "total_tracks": 14,
        "url": "",
        "art": "/static/images/owl_pharaoh.jpg",
        "id": "owl_pharaoh"
    },

    "nostalgia_ULTRA": {
        "name": "nostalgia, ULTRA",
        "artist": "Frank Ocean",
        "release_date": "2011-02-16",
        "total_tracks": 14,
        "url": "",
        "art": "/static/images/nostalgia_ULTRA.jpg",
        "id": "nostalgia_ULTRA"
    },

    "see_u_soon": {
        "name": "see u soon </3",
        "artist": "Destroy Lonely",
        "release_date": "2025-06-05",
        "total_tracks": 5,
        "url": "",
        "art": "/static/images/see_u_soon.jpg",
        "id": "see_u_soon"
    },

    "2_much_music": {
        "name": "2 much music </3",
        "artist": "Destroy Lonely",
        "release_date": "2025-09-28",
        "total_tracks": 5,
        "url": "",
        "art": "/static/images/2_much_music.jpeg",
        "id": "2_much_music"
    }
}

spotify = spotipy.Spotify(
    auth_manager = SpotifyClientCredentials(
        client_id = os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)

def get_album(album_id):
    if album_id in CUSTOM_ALBUMS:
        return CUSTOM_ALBUMS[album_id]

    album = spotify.album(album_id)

    album_name = album['name']
    album_artist = format_artists(album["artists"])
    album_release_date = album['release_date']
    album_total_tracks = album['total_tracks']
    album_url = album['external_urls']['spotify']
    album_art = album['images'][0]['url']
    album_id = album['id']

    return {
        "name": album_name,
        "artist": album_artist,
        "release_date": album_release_date,
        "total_tracks": album_total_tracks,
        "url": album_url,
        "art": album_art,
        "id": album_id
    }

def search_albums(query):
    results = spotify.search(q=query, type="album", limit=10)
    album_results = results['albums']['items']
    seen = set()
    albums = []

    for album in album_results:
        album_name = album['name']
        album_artist = format_artists(album["artists"])

        # Stops duplicate albums (ex. clean and explicit versions)
        key = (album_name.lower(), album_artist.lower())

        if key in seen:
            continue

        seen.add(key)

        album_release_date = album['release_date']
        album_total_tracks = album['total_tracks']
        album_url = album['external_urls']['spotify']
        album_art = album['images'][0]['url']
        album_id = album['id']
        albums.append({
            "name": album_name,
            "artist": album_artist,
            "release_date": album_release_date,
            "total_tracks": album_total_tracks,
            "url": album_url,
            "art": album_art,
            "id": album_id
        })

        query_lower = query.lower()

    for album in CUSTOM_ALBUMS.values():
        if (
            query_lower in album["name"].lower()
            or query_lower in album["artist"].lower()
        ):
            albums.append(album)

    return albums

def format_artists(artists):
    names = [artist["name"] for artist in artists]
    if len(names) == 1:
        return names[0]
    elif len(names) == 2:
        return f"{names[0]} & {names[1]}"
    else:
        return ", ".join(names[:-1]) + f" & {names[-1]}"