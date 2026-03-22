---
name: skip
description: Skip to the next track on Spotify
argument-hint: [number of tracks]
allowed-tools: Bash
user-invocable: true
---

# Skip

Skip to the next track. Optionally specify how many tracks to skip (default: 1).

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import skip; print(skip(NUM))"
```

Replace `NUM` with the number of tracks to skip. After skipping, show what's now playing by calling `get_current_track`.
