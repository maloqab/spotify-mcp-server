import json
import os
import sys
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("spotify")

SCOPES = ",".join([
    "user-read-playback-state",
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-library-read",
    "user-library-modify",
    "user-read-recently-played",
    "user-top-read",
    "playlist-read-private",
    "playlist-read-collaborative",
    "playlist-modify-private",
    "playlist-modify-public",
])

_sp: spotipy.Spotify | None = None


def get_spotify() -> spotipy.Spotify:
    global _sp
    if _sp is None:
        _sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.environ["SPOTIFY_CLIENT_ID"],
            client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
            redirect_uri=os.environ.get("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8080/callback"),
            scope=SCOPES,
            cache_path=os.path.join(os.path.dirname(__file__), ".cache"),
        ))
    return _sp


# ── Playback ──────────────────────────────────────────────

@mcp.tool()
def get_current_track() -> str:
    """Get the currently playing track on Spotify."""
    sp = get_spotify()
    current = sp.current_playback()
    if not current or not current.get("item"):
        return "Nothing is currently playing."
    item = current["item"]
    artists = ", ".join(a["name"] for a in item["artists"])
    progress_s = (current.get("progress_ms") or 0) // 1000
    duration_s = (item.get("duration_ms") or 0) // 1000
    return json.dumps({
        "name": item["name"],
        "artist": artists,
        "album": item["album"]["name"],
        "uri": item["uri"],
        "is_playing": current["is_playing"],
        "progress": f"{progress_s // 60}:{progress_s % 60:02d}",
        "duration": f"{duration_s // 60}:{duration_s % 60:02d}",
    }, indent=2)


@mcp.tool()
def play(uri: Optional[str] = None) -> str:
    """Start or resume Spotify playback. Optionally pass a Spotify URI to play a specific track, album, artist, or playlist."""
    sp = get_spotify()
    if uri:
        if ":track:" in uri:
            sp.start_playback(uris=[uri])
        else:
            sp.start_playback(context_uri=uri)
    else:
        sp.start_playback()
    return "Playback started."


@mcp.tool()
def pause() -> str:
    """Pause Spotify playback."""
    sp = get_spotify()
    sp.pause_playback()
    return "Playback paused."


@mcp.tool()
def skip(num_skips: int = 1) -> str:
    """Skip to the next track. Set num_skips to skip multiple tracks."""
    sp = get_spotify()
    for _ in range(num_skips):
        sp.next_track()
    return f"Skipped {num_skips} track(s)."


@mcp.tool()
def previous() -> str:
    """Go back to the previous track."""
    sp = get_spotify()
    sp.previous_track()
    return "Playing previous track."


@mcp.tool()
def set_volume(volume: int) -> str:
    """Set Spotify playback volume (0-100)."""
    sp = get_spotify()
    sp.volume(max(0, min(100, volume)))
    return f"Volume set to {volume}."


# ── Search ────────────────────────────────────────────────

@mcp.tool()
def search(query: str, search_type: str = "track", limit: int = 10) -> str:
    """Search Spotify for tracks, albums, artists, or playlists. search_type can be: track, album, artist, playlist, or a comma-separated combination."""
    sp = get_spotify()
    results = sp.search(q=query, type=search_type, limit=limit)
    output = []
    for category in results:
        for item in results[category]["items"]:
            entry = {"name": item["name"], "uri": item["uri"], "type": item["type"]}
            if "artists" in item:
                entry["artist"] = ", ".join(a["name"] for a in item["artists"])
            if "album" in item:
                entry["album"] = item["album"]["name"]
            output.append(entry)
    return json.dumps(output, indent=2)


# ── Queue ─────────────────────────────────────────────────

@mcp.tool()
def get_queue() -> str:
    """Get the current Spotify playback queue."""
    sp = get_spotify()
    queue = sp.queue()
    items = []
    if queue.get("currently_playing"):
        cp = queue["currently_playing"]
        items.append({
            "position": "now_playing",
            "name": cp["name"],
            "artist": ", ".join(a["name"] for a in cp["artists"]),
            "uri": cp["uri"],
        })
    for i, track in enumerate(queue.get("queue", [])[:20]):
        items.append({
            "position": i + 1,
            "name": track["name"],
            "artist": ", ".join(a["name"] for a in track["artists"]),
            "uri": track["uri"],
        })
    return json.dumps(items, indent=2)


@mcp.tool()
def add_to_queue(uri: str) -> str:
    """Add a track to the Spotify playback queue by URI."""
    sp = get_spotify()
    sp.add_to_queue(uri)
    return f"Added to queue: {uri}"


# ── Playlists ─────────────────────────────────────────────

@mcp.tool()
def get_my_playlists(limit: int = 20) -> str:
    """Get the current user's Spotify playlists."""
    sp = get_spotify()
    results = sp.current_user_playlists(limit=limit)
    playlists = []
    for p in results["items"]:
        playlists.append({
            "name": p["name"],
            "id": p["id"],
            "uri": p["uri"],
            "tracks": p["tracks"]["total"],
            "public": p["public"],
        })
    return json.dumps(playlists, indent=2)


@mcp.tool()
def get_playlist_tracks(playlist_id: str) -> str:
    """Get all tracks in a Spotify playlist."""
    sp = get_spotify()
    results = sp.playlist_tracks(playlist_id)
    tracks = []
    for item in results["items"]:
        t = item["track"]
        if t:
            tracks.append({
                "name": t["name"],
                "artist": ", ".join(a["name"] for a in t["artists"]),
                "uri": t["uri"],
                "album": t["album"]["name"],
            })
    return json.dumps(tracks, indent=2)


@mcp.tool()
def create_playlist(name: str, description: str = "", public: bool = True) -> str:
    """Create a new Spotify playlist."""
    sp = get_spotify()
    user_id = sp.current_user()["id"]
    playlist = sp.user_playlist_create(user_id, name, public=public, description=description)
    return json.dumps({"name": playlist["name"], "id": playlist["id"], "uri": playlist["uri"]}, indent=2)


@mcp.tool()
def add_tracks_to_playlist(playlist_id: str, track_uris: list[str]) -> str:
    """Add tracks to a Spotify playlist. track_uris should be a list of Spotify track URIs."""
    sp = get_spotify()
    sp.playlist_add_items(playlist_id, track_uris)
    return f"Added {len(track_uris)} track(s) to playlist."


@mcp.tool()
def remove_tracks_from_playlist(playlist_id: str, track_uris: list[str]) -> str:
    """Remove tracks from a Spotify playlist. track_uris should be a list of Spotify track URIs."""
    sp = get_spotify()
    sp.playlist_remove_all_occurrences_of_items(playlist_id, track_uris)
    return f"Removed {len(track_uris)} track(s) from playlist."


# ── Info ──────────────────────────────────────────────────

@mcp.tool()
def get_track_info(uri: str) -> str:
    """Get detailed info about a Spotify track by URI."""
    sp = get_spotify()
    track_id = uri.split(":")[-1]
    t = sp.track(track_id)
    return json.dumps({
        "name": t["name"],
        "artist": ", ".join(a["name"] for a in t["artists"]),
        "album": t["album"]["name"],
        "duration": f"{t['duration_ms'] // 60000}:{(t['duration_ms'] // 1000) % 60:02d}",
        "uri": t["uri"],
        "popularity": t["popularity"],
    }, indent=2)


@mcp.tool()
def get_recently_played(limit: int = 10) -> str:
    """Get recently played tracks on Spotify."""
    sp = get_spotify()
    results = sp.current_user_recently_played(limit=limit)
    tracks = []
    for item in results["items"]:
        t = item["track"]
        tracks.append({
            "name": t["name"],
            "artist": ", ".join(a["name"] for a in t["artists"]),
            "uri": t["uri"],
            "played_at": item["played_at"],
        })
    return json.dumps(tracks, indent=2)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
