---
name: volume
description: Set Spotify playback volume (0-100)
argument-hint: [level 0-100]
allowed-tools: Bash
user-invocable: true
---

# Volume

Set the Spotify playback volume:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import set_volume; print(set_volume(LEVEL))"
```

Replace `LEVEL` with the volume level (0-100). If the user says something like "turn it up" or "louder", use 80. "Turn it down" or "quieter", use 30. "Mute", use 0. "Max", use 100.
