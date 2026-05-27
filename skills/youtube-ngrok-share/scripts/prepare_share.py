#!/usr/bin/env python3
import argparse
import json
import os
import secrets
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def fail(message: str, code: int = 1) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def require_command(name: str) -> None:
    if shutil.which(name) is None:
        fail(f"Missing required command: {name}")


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def choose_downloaded_file(run_dir: Path) -> Path:
    files = [p for p in run_dir.iterdir() if p.is_file() and p.name != "metadata.json"]
    if not files:
        fail(f"No downloaded file found in {run_dir}")
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Download a YouTube video and prepare a shareable ngrok directory.")
    parser.add_argument("url", help="YouTube URL to download")
    parser.add_argument("--downloads-root", default="artifacts/youtube-downloads/skill-runs", help="Root directory for downloaded files")
    parser.add_argument("--share-root", default="artifacts/ngrok-share", help="Root directory for the shareable symlink")
    parser.add_argument("--format", default="bv*+ba/b", help="yt-dlp format selector")
    parser.add_argument("--slug", default="", help="Optional fixed slug for the public path")
    args = parser.parse_args()

    require_command("yt-dlp")
    require_command("ffmpeg")

    workspace = Path.cwd()
    downloads_root = (workspace / args.downloads_root).resolve() if not os.path.isabs(args.downloads_root) else Path(args.downloads_root).resolve()
    share_root = (workspace / args.share_root).resolve() if not os.path.isabs(args.share_root) else Path(args.share_root).resolve()

    video_id = run([
        "yt-dlp",
        "--no-playlist",
        "--get-id",
        args.url,
    ]).stdout.strip().splitlines()[-1].strip()
    if not video_id:
        fail("Could not determine video id")

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = downloads_root / f"{stamp}-{video_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    output_template = str(run_dir / "%(title).120B_[%(id)s].%(ext)s")
    subprocess.run(
        [
            "yt-dlp",
            "--no-playlist",
            "--restrict-filenames",
            "--merge-output-format",
            "mp4",
            "-f",
            args.format,
            "-o",
            output_template,
            args.url,
        ],
        check=True,
    )

    downloaded = choose_downloaded_file(run_dir)
    slug = args.slug or secrets.token_urlsafe(12).replace("-", "").replace("_", "")[:16]
    share_dir = share_root / slug
    share_dir.mkdir(parents=True, exist_ok=True)

    public_name = downloaded.name
    public_path = share_dir / public_name
    if public_path.exists() or public_path.is_symlink():
        public_path.unlink()
    public_path.symlink_to(downloaded)

    data = {
        "url": args.url,
        "videoId": video_id,
        "downloadedFile": str(downloaded),
        "fileName": downloaded.name,
        "fileSizeBytes": downloaded.stat().st_size,
        "runDir": str(run_dir),
        "shareDir": str(share_dir),
        "shareSlug": slug,
        "relativePath": f"/{public_name}",
        "preparedAt": stamp,
        "format": args.format,
    }

    (run_dir / "metadata.json").write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
