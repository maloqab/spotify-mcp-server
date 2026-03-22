---
name: play
description: Play or resume Spotify playback. Can play a song, playlist, album, or artist.
argument-hint: [song/playlist/album name or Spotify URI]
allowed-tools: Bash
user-invocable: true
---

# Play

Resume playback or play a specific track, playlist, album, or artist on Spotify.

## If no argument provided

Resume current playback:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import play; print(play())"
```

## If a Spotify URI is provided (starts with spotify:)

Play it directly:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import play; print(play('SPOTIFY_URI'))"
```

## If a name is provided

First check if it matches one of the user's playlists. If it does, play that playlist. Otherwise search for a track.

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "
from server import get_my_playlists, search, play
import json, re

query = 'QUERY'

def normalize(s):
    return re.sub(r'[^a-z0-9 ]', '', s.lower()).strip()

# Check playlists first (fuzzy match: ignore punctuation)
playlists = json.loads(get_my_playlists(50))
match = None
nq = normalize(query)
for p in playlists:
    np = normalize(p['name'])
    if not np or not nq:
        continue
    if nq in np or np in nq:
        match = p
        break

if match:
    play(match['uri'])
    print(f'Playing playlist: {match[\"name\"]}')
else:
    # Search for tracks
    results = json.loads(search(query, 'track', 1))
    if results:
        uri = results[0]['uri']
        play(uri)
        print(f'Playing: {results[0][\"name\"]} by {results[0].get(\"artist\", \"Unknown\")}')
    else:
        print('No results found.')
"
```

Replace `QUERY` with the user's search query. The `$SPOTIFY_MCP_DIR` env var must point to the spotify-mcp-server directory.
