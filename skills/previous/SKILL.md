---
name: previous
description: Go back to the previous track on Spotify
allowed-tools: Bash
user-invocable: true
---

# Previous

Go back to the previous track:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import previous; print(previous())"
```

After going back, show what's now playing by calling `get_current_track`.
