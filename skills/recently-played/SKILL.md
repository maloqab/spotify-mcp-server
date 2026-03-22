---
name: recently-played
description: Show recently played tracks on Spotify
allowed-tools: Bash
user-invocable: true
---

# Recently Played

Get the user's recently played tracks:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import get_recently_played; print(get_recently_played())"
```

Present results as a numbered list with track name, artist, and when it was played.
