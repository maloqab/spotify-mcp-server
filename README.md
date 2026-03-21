# Spotify MCP Server

A Spotify MCP server for Claude, built with [FastMCP](https://github.com/modelcontextprotocol/python-sdk). Works with both Claude Desktop and Claude Code.

## Features

16 tools for full Spotify control:

- **Playback**: get current track, play, pause, skip, previous, volume
- **Search**: tracks, albums, artists, playlists
- **Queue**: view queue, add tracks
- **Playlists**: list, view tracks, create, add/remove tracks
- **Info**: track details, recently played

## Prerequisites

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)
2. Create an app
3. Set redirect URI to `http://127.0.0.1:8080/callback`
4. Copy your Client ID and Client Secret

## Claude Desktop (one-click install)

1. Download `spotify-mcp-server-0.1.0.mcpb` from [Releases](https://github.com/maloqab/spotify-mcp-server/releases)
2. Double-click the file
3. Claude Desktop will prompt you for your Spotify Client ID and Client Secret
4. Done — tools appear immediately

## Claude Desktop (manual config)

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "spotify": {
      "command": "uv",
      "args": ["run", "--directory", "/absolute/path/to/spotify-mcp-server", "python", "server.py"],
      "env": {
        "SPOTIFY_CLIENT_ID": "your_id",
        "SPOTIFY_CLIENT_SECRET": "your_secret",
        "SPOTIFY_REDIRECT_URI": "http://127.0.0.1:8080/callback"
      }
    }
  }
}
```

## Claude Code

```bash
git clone https://github.com/maloqab/spotify-mcp-server.git
cd spotify-mcp-server
uv sync
```

Authenticate (run once):

```bash
SPOTIFY_CLIENT_ID="your_id" SPOTIFY_CLIENT_SECRET="your_secret" SPOTIFY_REDIRECT_URI="http://127.0.0.1:8080/callback" uv run python -c "from server import get_spotify; get_spotify(); print('Done')"
```

Add to Claude Code:

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

## Requirements

- Python 3.10+
- [uv](https://docs.astral.sh/uv/)
- Spotify Premium (for playback control)
