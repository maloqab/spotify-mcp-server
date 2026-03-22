---
name: search
description: Search Spotify for tracks, albums, artists, or playlists
argument-hint: [query]
allowed-tools: Bash
user-invocable: true
---

# Search Spotify

Search for music on Spotify.

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import search; print(search('QUERY', 'track', 10))"
```

Replace `QUERY` with the user's search terms. You can change the second argument to `album`, `artist`, `playlist`, or a comma-separated combination like `track,album`.

Present results in a clean table format showing name, artist, album, and URI.
