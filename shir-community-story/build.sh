#!/usr/bin/env bash
# Builds the 9:16 story: trims the source, adds punch-in zooms, overlays the animated
# captions and normalizes loudness for Instagram.
#   ./build.sh <source.mp4> [out.mp4]
set -euo pipefail
cd "$(dirname "$0")"
SRC="$1"
OUT="${2:-../output/shir-community-story.mp4}"
FRAMES="${FRAMES_DIR:-/tmp/story-overlay-frames}"
START=1.4   # keep in sync with TRIM in captions.js
DUR=51.6

[ -f "$FRAMES/f00000.png" ] || node render-overlay.mjs "$FRAMES" 30

# Punch-in zoom per moment (source-time windows). T = output time, so source time = T+START.
s="(t+$START)"
Z="1+0.10*between($s,5.83,7.40)+0.08*between($s,16.09,16.75)+0.12*between($s,22.59,24.20)"
Z="$Z+0.06*between($s,42.01,42.90)+0.09*between($s,42.91,43.78)+0.12*between($s,43.79,45.60)"
Z="$Z+0.10*between($s,48.17,48.80)"

ffmpeg -y -ss $START -t $DUR -i "$SRC" -framerate 30 -i "$FRAMES/f%05d.png" \
  -filter_complex "\
[0:v]fps=30,scale=w='trunc(1080*($Z)/2)*2':h=-2:eval=frame:flags=lanczos,\
crop=1080:1920:x='(iw-1080)/2':y='(ih-1920)*0.6',setsar=1,\
eq=saturation=1.08:contrast=1.03[v];\
[v][1:v]overlay=0:0:shortest=1,format=yuv420p[out];\
[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map "[out]" -map "[a]" \
  -c:v libx264 -preset slow -crf 20 -profile:v high -c:a aac -b:a 192k \
  -movflags +faststart "$OUT"
echo "wrote $OUT"
