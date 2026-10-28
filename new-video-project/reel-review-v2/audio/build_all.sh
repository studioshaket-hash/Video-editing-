#!/bin/bash
# Rebuild the REVIEW V2 soundtrack and MP4 from scratch (needs: ffmpeg, fluidsynth + fluid-soundfont-gm,
# python3 + numpy, the per-shot working copies in ../reel-review-v1/assets/media/, the CC0 Foley in audio/src/foley/,
# and the V1 render ../reel-review-v1/renders/REVIEW_V1_reel_1080x1920.mp4 whose video stream is copied untouched).
set -e
cd "$(dirname "$0")/score"
python3 stem_dialogue.py      # production dialogue/ambience per shot, sample-identical to V1
python3 score_music.py        # original score (MIDI -> FluidSynth FluidR3_GM)
python3 derive.py             # whisper textures, low texture, sub drop, processed gun (from production audio)
python3 stems_fx.py           # ambience + foley stems
python3 mix.py                # ducking + premaster
cd ../stems
ffmpeg -v error -nostdin -i premaster.wav -af "volume=5.8dB,alimiter=limit=0.6918:attack=1:release=60:level=false:latency=1:asc=1" -c:a pcm_f32le -y master_raw.wav
python3 -c "
import sys; sys.path.insert(0,'../score')
from lib import *
m=load('master_raw.wav')[:N]; m=np.pad(m,((0,N-len(m)),(0,0))); k0,k1=sec(59.90),sec(59.95)
m[k0:k1]*=np.linspace(1,0,k1-k0)[:,None]; m[k1:]=0.0; save('master.wav', m)"
ffmpeg -v error -nostdin -i ../../../reel-review-v1/renders/REVIEW_V1_reel_1080x1920.mp4 -i master.wav -map 0:v:0 -map 1:a:0 -c:v copy -c:a aac -b:a 256k -ar 48000 -shortest -movflags +faststart -y ../../renders/REVIEW_V2_SOUNDTRACK.mp4
cd ../score && python3 hf_index.py
echo "done: renders/REVIEW_V2_SOUNDTRACK.mp4"
