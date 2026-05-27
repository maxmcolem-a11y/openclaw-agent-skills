---
name: youtube-ngrok-share
description: Download a YouTube video at the highest practical quality and return a temporary public ngrok link instead of an in-chat attachment. Use when a user sends a YouTube URL and wants the file delivered by download link, especially when the file is too large for Telegram or another chat provider.
---

# YouTube ngrok share

## Overview

Use this skill for on-demand YouTube delivery by temporary link. Prefer it when chat upload limits would force heavy downscaling or when the user explicitly wants the highest quality download.

## Prerequisites

Confirm these tools are available before starting:

- `yt-dlp`
- `ffmpeg`
- `ngrok`
- an authenticated ngrok config on this machine

If `ngrok http <port>` fails with `ERR_NGROK_4018`, stop and ask the user for an authtoken or the command they want to run locally.

## Workflow

### 1. Prepare the download and share directory

Run:

```bash
python3 skills/youtube-ngrok-share/scripts/prepare_share.py '<youtube-url>'
```

This script:

- downloads the video with `yt-dlp` using `bv*+ba/b`
- merges to MP4 when possible
- creates a random share slug under `artifacts/ngrok-share/`
- symlinks the downloaded file into that share directory
- prints JSON with the downloaded file path, share directory, and relative public path

Keep the JSON output. You need:

- `shareDir`
- `relativePath`
- `downloadedFile`
- `fileSizeBytes`

### 2. Choose a free local port

Run:

```bash
python3 skills/youtube-ngrok-share/scripts/get_free_port.py
```

Use the returned port for both the local file server and ngrok tunnel.

### 3. Start the local file server

Start a background server with a generous timeout, for example 2 hours:

```bash
python3 -m http.server <port> --bind 127.0.0.1 --directory '<shareDir>'
```

Use the `exec` tool in background mode so you can later kill the server session for cleanup.

### 4. Start ngrok

Start a second background process:

```bash
ngrok http <port> --log stdout
```

Again, keep the session so you can shut it down later.

### 5. Resolve the public URL

Run:

```bash
python3 skills/youtube-ngrok-share/scripts/get_tunnel_url.py <port>
```

Build the final download URL as:

```text
<public-url><relativePath>
```

Example:

```text
https://example.ngrok-free.dev/My_video_[abc123].mp4
```

### 6. Verify before replying

Send a `HEAD` request to the final URL and confirm:

- status `200`
- `Content-Length` is present or plausible
- the URL resolves to the expected file

If verification fails, fix the server or tunnel before replying.

### 7. Reply with the link and a short warning

Tell the user:

- the link
- approximate file size
- that the link is public to anyone who has it
- that you can shut it down after they are done

Keep the reply short.

### 8. Clean up

When the user is done, kill both background sessions:

- the local `http.server`
- the `ngrok` tunnel

Also clean up proactively if the user asks you to revoke the link.

## Defaults and adjustments

- Default to `bv*+ba/b` for highest practical quality.
- If the user asks for audio only, pass an audio-oriented yt-dlp format instead of the default.
- If the user asks for a smaller or faster transfer, lower the format selection intentionally rather than relying on chat upload limits.
- Prefer one active ngrok share per request. Clean up old test sessions before creating a new link.

## Scripts

- `scripts/prepare_share.py`: download the file and prepare a random public path
- `scripts/get_free_port.py`: choose a free localhost port
- `scripts/get_tunnel_url.py`: read the ngrok inspector API and return the public URL for a given local port
