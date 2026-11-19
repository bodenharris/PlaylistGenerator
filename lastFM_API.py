import os
import sys
import time

import requests

# Set LASTFM_API_KEY and LASTFM_USER as environment variables (never commit the key).
API_KEY = os.environ.get("LASTFM_API_KEY")
USER = os.environ.get("LASTFM_USER")  # Last.fm username
if not API_KEY or not USER:
    sys.exit("Set the LASTFM_API_KEY and LASTFM_USER environment variables first.")
NUM_ARTISTS = 100 # number of user’s top artists
NUM_TRACKS = 1 # number of user’s top tracks per artist
MAX_TRACKS_PER_PAGE = 1000

def get_top_artists(user, limit):
    url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={user}&api_key={API_KEY}&format=json&limit={limit}"
    response = requests.get(url)
    data = response.json()
    return [artist["name"] for artist in data["topartists"]["artist"]]

def get_all_user_top_tracks(user, max_pages=10):
    """Fetch all top tracks for a user with pagination (up to ~10,000)."""
    all_tracks = []
    for page in range(1, max_pages + 1):
        url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={user}&api_key={API_KEY}&format=json&limit={MAX_TRACKS_PER_PAGE}&page={page}"
        response = requests.get(url)
        data = response.json()
        if "toptracks" not in data or not data["toptracks"]["track"]:
            break
        page_tracks = [
            {
                "artist": t["artist"]["name"],
                "track": t["name"],
                "playcount": int(t["playcount"])
            }
            for t in data["toptracks"]["track"]
        ]
        all_tracks.extend(page_tracks)
        time.sleep(0.2)  # polite delay
    return all_tracks

def find_user_top_track_for_artist(artist, user_tracks):
    """Find the user's most listened tracks for a specific artist."""
    artist_lower = artist.lower()
    matches = [t for t in user_tracks if artist_lower in t["artist"].lower()]
    if not matches:
        return []
    # sort by playcount descending
    matches.sort(key=lambda x: x["playcount"], reverse=True)
    return matches[:NUM_TRACKS]

# Fetch data
top_artists = get_top_artists(USER, NUM_ARTISTS)
print(f"🎶 Found {len(top_artists)} top artists for {USER}")

user_tracks = get_all_user_top_tracks(USER)
print(f"🎧 Retrieved {len(user_tracks)} user top tracks")

# Write results
with open("top_artists.txt", "w", encoding="utf-8") as f:
    for i, artist in enumerate(top_artists, 1):
        best_tracks = find_user_top_track_for_artist(artist, user_tracks)
        f.write(f"{i}. {artist}\n")
        if best_tracks:
            for j, track in enumerate(best_tracks, 1):
                f.write(f"   → Top Track {j}: {track['track']}\n")
        else:
            f.write("   → Top Track 1: N/A\n")
        f.write("\n")

print(f"✅ Top {NUM_ARTISTS} artists and their top {NUM_TRACKS} tracks saved to top_artists.txt")
