---
name: play
description: Play or resume Spotify playback. Optionally specify a song to search and play.
argument-hint: [song name or Spotify URI]
allowed-tools: Bash
user-invocable: true
---

# Play

Resume playback or play a specific track on Spotify.

## If no argument provided

Resume current playback:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import play; print(play())"
```

## If a song name is provided

First search for it, then play the top result:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "
from server import search, play
import json
results = json.loads(search('QUERY', 'track', 1))
if results:
    uri = results[0]['uri']
    play(uri)
    print(f'Playing: {results[0][\"name\"]} by {results[0].get(\"artist\", \"Unknown\")}')
else:
    print('No results found.')
"
```

Replace `QUERY` with the user's search query.

## If a Spotify URI is provided (starts with spotify:)

Play it directly:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import play; print(play('SPOTIFY_URI'))"
```
