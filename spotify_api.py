import os
import re

import requests
import spotipy

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials


# =========================================================
# ENVIRONMENT / SPOTIFY SETUP
# =========================================================

load_dotenv()


spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)


# =========================================================
# CUSTOM ALBUMS
# Albums that are not available through Spotify.
# =========================================================

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
    },

    "lost_files_4": {
            "name": "lost files 4",
            "artist": "Ken Carson",
            "release_date": "2023-01-03",
            "total_tracks": 8,
            "url": "",
            "art": "/static/images/lost_files_4.JPG",
            "id": "lost_files_4"
        }
}


# =========================================================
# SPOTIFY FUNCTIONS
# =========================================================

def get_album(album_id):
    """Get album information from Spotify or the custom album list."""

    # Check custom albums first.
    if album_id in CUSTOM_ALBUMS:
        return CUSTOM_ALBUMS[album_id]

    # Get album information from Spotify.
    album = spotify.album(album_id)

    album_name = album["name"]
    album_artist = format_artists(album["artists"])
    album_release_date = album["release_date"]
    album_total_tracks = album["total_tracks"]
    album_url = album["external_urls"]["spotify"]
    album_art = album["images"][0]["url"]
    album_id = album["id"]

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
    """Search Spotify for albums and include matching custom albums."""

    results = spotify.search(
        q=query,
        type="album",
        limit=10
    )

    album_results = results["albums"]["items"]

    seen = set()
    albums = []

    for album in album_results:

        album_name = album["name"]
        album_artist = format_artists(album["artists"])

        # Stop duplicate albums, such as clean and explicit versions.
        key = (
            album_name.lower(),
            album_artist.lower()
        )

        if key in seen:
            continue

        seen.add(key)

        album_release_date = album["release_date"]
        album_total_tracks = album["total_tracks"]
        album_url = album["external_urls"]["spotify"]
        album_art = album["images"][0]["url"]
        album_id = album["id"]

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

    # Add matching custom albums to the search results.
    for album in CUSTOM_ALBUMS.values():

        if (
            query_lower in album["name"].lower()
            or query_lower in album["artist"].lower()
        ):
            albums.append(album)

    return albums


def format_artists(artists):
    """Format a list of Spotify artists into a readable string."""

    names = [artist["name"] for artist in artists]

    if len(names) == 1:
        return names[0]

    elif len(names) == 2:
        return f"{names[0]} & {names[1]}"

    else:
        return ", ".join(names[:-1]) + f" & {names[-1]}"


# =========================================================
# APPLE MUSIC FUNCTIONS
# =========================================================

def get_apple_music_url(album_name, artist):
    """Find the Apple Music URL for an album."""

    url = "https://itunes.apple.com/search"

    searches = [
        f"{album_name} {artist}",
        album_name
    ]

    for search_term in searches:

        params = {
            "term": search_term,
            "entity": "album",
            "limit": 10
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            continue

        results = response.json()["results"]

        normalized_album = normalize_album_title(album_name)
        requested_artist = artist.lower().strip()

        matches = []

        for result in results:

            result_album = normalize_album_title(
                result.get("collectionName", "")
            )

            result_artist = result.get(
                "artistName",
                ""
            ).lower().strip()

            if (
                result_album == normalized_album
                and result_artist == requested_artist
            ):
                matches.append(result)

        if matches:

            # Prefer the explicit version when available.
            for result in matches:

                if result.get("contentAdvisoryRating") == "Explicit":
                    return result.get("collectionViewUrl")

            # Fall back to the first matching result.
            return matches[0].get("collectionViewUrl")

    return "NOT_FOUND"


def normalize_album_title(title):
    """Normalize album titles to make Apple Music matching easier."""

    title = title.lower().strip()

    # Remove common version labels.
    title = re.sub(
        r'\s*\((deluxe|deluxe edition|deluxe version|original|remastered|expanded edition)\)\s*$',
        '',
        title
    )

    # Remove punctuation.
    title = re.sub(r'[^\w\s]', '', title)

    # Collapse multiple spaces.
    title = re.sub(r'\s+', ' ', title)

    return title.strip()