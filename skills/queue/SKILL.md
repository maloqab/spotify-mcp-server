---
name: queue
description: View or add tracks to the Spotify playback queue
argument-hint: [track name or URI to add]
allowed-tools: Bash
user-invocable: true
---

# Queue

## View the current queue

If no argument is provided, show the queue:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import get_queue; print(get_queue())"
```

## Add a track to the queue

If the user provides a Spotify URI, add it directly:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "from server import add_to_queue; print(add_to_queue('SPOTIFY_URI'))"
```

If the user provides a song name, search first, then add the top result:

```bash
uv run --directory "$SPOTIFY_MCP_DIR" python -c "
from server import search, add_to_queue
import json
results = json.loads(search('QUERY', 'track', 1))
if results:
    uri = results[0]['uri']
    add_to_queue(uri)
    print(f'Added to queue: {results[0][\"name\"]} by {results[0].get(\"artist\", \"Unknown\")}')
else:
    print('No results found.')
"
```

Present the queue in a numbered list format.
