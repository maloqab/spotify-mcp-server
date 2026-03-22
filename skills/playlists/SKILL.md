---
name: playlists
description: View your Spotify playlists or get tracks from a specific playlist
argument-hint: [playlist name]
allowed-tools: Bash
user-invocable: true
---

# Playlists

## List all playlists

If no argument is provided, list the user's playlists:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import get_my_playlists; print(get_my_playlists())"
```

## Get tracks from a specific playlist

If the user specifies a playlist name, first list playlists to find the matching ID, then get its tracks:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import get_playlist_tracks; print(get_playlist_tracks('PLAYLIST_ID'))"
```

Present playlists as a table with name, track count, and public/private status. Present tracks as a numbered list with name and artist.
