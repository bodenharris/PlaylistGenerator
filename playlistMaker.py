import os
import re
import sys

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# --- Spotify authentication ---
# Credentials come from environment variables so they never live in the repo:
#   SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET (and optionally SPOTIPY_REDIRECT_URI)
missing = [v for v in ("SPOTIPY_CLIENT_ID", "SPOTIPY_CLIENT_SECRET") if not os.environ.get(v)]
if missing:
    sys.exit(f"Set these environment variables first: {', '.join(missing)}")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-public",
    redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI", "http://localhost:8080"),
))

# --- Create a playlist ---
playlist_Title = "My Playlist" # You can change the playlist title here
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user_id, playlist_Title, public=True)

# --- Parse top_artists.txt ---
tracks = []

with open("top_artists.txt", "r", encoding="utf-8") as f:
    artist = None
    songs = []
    for line in f:
        line = line.strip()
        if not line:
            continue
        # Artist line: starts with number + period
        artist_match = re.match(r"^\d+\.\s*(.*)", line)
        if artist_match:
            if artist and songs:
                tracks.append((artist, songs))
            artist = artist_match.group(1)
            songs = []
        # Song line: starts with arrow
        song_match = re.match(r"^→.*:\s*(.*)", line)
        if song_match:
            song_name = song_match.group(1)
            # Remove "Top Track X:" if present
            song_name = re.sub(r"^Top Track \d+:\s*", "", song_name)
            songs.append(song_name)
    # Add last artist
    if artist and songs:
        tracks.append((artist, songs))

# --- Search and add tracks to playlist ---
uris = []
for artist, songs in tracks:
    for song in songs:
        query = f"track:{song} artist:{artist}"
        result = sp.search(query, type="track", limit=1)
        items = result["tracks"]["items"]
        if items:
            uris.append(items[0]["uri"])
            print(f"✅ Added: {song} by {artist}")
        else:
            print(f"❌ Could not find: {song} by {artist}")

# --- Add tracks to playlist ---
if uris:
    sp.playlist_add_items(playlist["id"], uris)
    print("✅ Playlist created:", playlist["external_urls"]["spotify"])
else:
    print("⚠️ No tracks found to add.")
