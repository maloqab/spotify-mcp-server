# Spotify MCP Server

A Spotify MCP server for Claude Code, built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk).

## Features

16 tools for full Spotify control:

- **Playback**: get current track, play, pause, skip, previous, volume
- **Search**: tracks, albums, artists, playlists
- **Queue**: view queue, add tracks
- **Playlists**: list, view tracks, create, add/remove tracks
- **Info**: track details, recently played

## Setup

### 1. Spotify API Credentials

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Set redirect URI to `http://127.0.0.1:8080/callback`
4. Copy your Client ID and Client Secret

### 2. Install

```bash
git clone https://github.com/maloqab/spotify-mcp-server.git
cd spotify-mcp-server
uv sync
```

### 3. Authenticate

Run once to complete the OAuth flow:

```bash
SPOTIFY_CLIENT_ID="your_id" \
SPOTIFY_CLIENT_SECRET="your_secret" \
SPOTIFY_REDIRECT_URI="http://127.0.0.1:8080/callback" \
uv run python -c "from server import get_spotify; get_spotify(); print('Done')"
```

This opens your browser to authorize with Spotify. The token is cached locally.

### 4. Add to Claude Code

```bash
claude mcp add-json "spotify" '{
  "command": "uv",
  "args": ["run", "--directory", "/absolute/path/to/spotify-mcp-server", "python", "server.py"],
  "env": {
    "SPOTIFY_CLIENT_ID": "your_id",
    "SPOTIFY_CLIENT_SECRET": "your_secret",
    "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8080/callback"
  }
}'
```

Restart Claude Code and the tools will be available.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Spotify Premium (for playback control)
