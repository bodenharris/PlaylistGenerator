# PlaylistGenerator

Turns your Last.fm listening history into a Spotify playlist.

1. `lastFM_API.py` pulls your top 100 artists and up to 10,000 of your top tracks from Last.fm, then writes each artist's most-played track to `top_artists.txt`.
2. `playlistMaker.py` searches Spotify for each of those tracks and adds them to a new public playlist.

## Setup

```
pip install requests spotipy
```

Get a Last.fm API key at <https://www.last.fm/api/account/create> and create a Spotify app at <https://developer.spotify.com/dashboard> with the redirect URI `http://localhost:8080`. Then set these environment variables (PowerShell shown):

```powershell
$env:LASTFM_API_KEY = "your-lastfm-key"
$env:LASTFM_USER = "your-lastfm-username"
$env:SPOTIPY_CLIENT_ID = "your-spotify-client-id"
$env:SPOTIPY_CLIENT_SECRET = "your-spotify-client-secret"
```

## Run

```
python lastFM_API.py
python playlistMaker.py
```

The first Spotify run opens a browser to log in. Spotipy caches the resulting token in `.cache`, which is git-ignored. Never commit it.
