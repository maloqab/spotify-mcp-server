---
name: now-playing
description: Show what's currently playing on Spotify
allowed-tools: Bash
user-invocable: true
---

# Now Playing

Run this command to check what's currently playing on Spotify:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import get_current_track; print(get_current_track())"
```

The `SPOTIFY_MCP_DIR` environment variable should point to the spotify-mcp-server directory. If it's not set, use the plugin's own directory by finding where this skill lives.

Present the result in a clean, concise format showing the track name, artist, album, and playback progress.
