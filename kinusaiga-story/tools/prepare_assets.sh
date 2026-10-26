#!/usr/bin/env bash
# Recreate the project's media from the untouched originals in media/source/.
# The originals are never modified.
set -euo pipefail
cd "$(dirname "$0")/.."
SRC=../media/source
mkdir -p assets
# V2 is already 720x1280 (9:16); used as-is (hard link, no re-encode).
ln -f "$SRC/VID-20261026-WA0015.mp4" assets/v2.mp4
# V1 is 480x854: one careful Lanczos upscale to 1080x1920, no sharpening, audio copied untouched.
ffmpeg -v error -y -i "$SRC/VID-20261026-WA0012.mp4" -map 0:v -map 0:a \
  -vf "scale=1080:1920:flags=lanczos+accurate_rnd+full_chroma_int,setsar=1" \
  -c:v libx264 -preset slow -crf 14 -pix_fmt yuv420p -c:a copy -movflags +faststart assets/v1_1080.mp4
echo "assets ready"
