---
name: pause
description: Pause Spotify playback
allowed-tools: Bash
user-invocable: true
---

# Pause

Pause the current Spotify playback:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import pause; print(pause())"
```
