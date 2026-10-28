# How to resume this project

**Repository and branch:**
- Repository: `studioshaket-hash/Video-editing-`
- Branch: `claude/new-video-source-index`

## What is in git
| Path | Contents |
|---|---|
| `_index/` | The source footage index (shot index, transcripts, notes) |
| `edit_plan/` | `EDIT_PLAN_v1.md` and `AUDIO_CUE_SHEET_V2.md` |
| `reel-review-v1/` | REVIEW V1 HyperFrames project (`build/build.py` generates `index.html` + captions; `REVIEW.md`, `TIMELINE.md`) |
| `reel-review-v2/` | REVIEW V2 (soundtrack only): `audio/score/*.py` (score, Foley, derived sounds, mix), `audio/build_all.sh`, `REVIEW_V2.md`, `audio/FOLEY_SOURCES.json` |

## What is NOT in git (large media, lost when the cloud session is reclaimed)
- The 4K per-shot working copies: `reel-review-v1/assets/media/*.mp4`.
- The renders: `REVIEW_V1_*.mp4` and `REVIEW_V2_SOUNDTRACK.mp4`.
- The audio stems and the CC0 Foley WAVs.

**Keep the two MP4s by downloading them from the chat.**

The original footage stays on Google Drive:
- Folder A replacement copies: https://drive.google.com/drive/folders/1UYks6-eGCG7J0wAXD4co-uT8YHVmgpYp. The file IDs are in `new-video-project/_meta/folderA_replacement_ids.tsv` (in git).
- Folder B: https://drive.google.com/drive/folders/15_2_O8XtF0afq1O8xwGnTJhdU6ktmEb1

## Resume in a new Claude Code session
1. Start a session on the repository and branch above, and ask Claude to read `new-video-project/RESUME.md`, `reel-review-v1/REVIEW.md` and `reel-review-v2/REVIEW_V2.md`.
2. **If the media is gone**, rebuild the working copies. The steps:
   - fetch only each shot's byte range (shot ±1.5 s) from the Drive originals, using the source/in/out table in `reel-review-v1/build/build.py`;
   - cut 4K 25 fps CRF 12 H.264 copies, starting at `MEZZ_T0`, into `reel-review-v1/assets/media/<shot>.mp4`;
   - tone-map the iPhone clips (IMG_3153, IMG_3156) from HLG to Rec.709 (zscale + mobius).
3. Install the tools: `apt-get install -y fluidsynth fluid-soundfont-gm` and `pip install numpy faster-whisper`. The HyperFrames CLI is `npx --yes hyperframes@0.8.202` and the skills are installed with `npx hyperframes skills update hyperframes hyperframes-cli media-use`.
4. **V1:** `cd reel-review-v1 && python3 build/build.py && npx --yes hyperframes@0.8.202 check && npx --yes hyperframes@0.8.202 render -o renders/REVIEW_V1_reel_1080x1920.mp4 -q delivery --fps 25 --sdr`. Then apply the audio loudnorm step described in `reel-review-v1/REVIEW.md`.
5. **V2:** re-download the CC0 Foley listed in `reel-review-v2/audio/FOLEY_SOURCES.json` into `reel-review-v2/audio/src/foley/<key>.wav` (48 kHz stereo WAV), then run `reel-review-v2/audio/build_all.sh`.
