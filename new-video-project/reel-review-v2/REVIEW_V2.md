# REVIEW V2: soundtrack-only revision of REVIEW V1

**Output:** `renders/REVIEW_V2_SOUNDTRACK.mp4` (not in git, 231 MB).
- 60.48 s, 1080×1920, 25 fps.
- Video stream copied from V1 bit-for-bit (video packet MD5 `dd657c32b6f13da031700208f84c7839`, identical to V1).
- V1 files are untouched.

**Measured on the final MP4:**

| Check | Result |
|---|---|
| Integrated loudness | −16.2 LUFS |
| True peak | −3.1 dBFS (ceiling −1.5) |
| LRA | 13.2 LU |
| Audio/video sync | 0.00 ms at six checkpoints |
| Music at the stare (52.80 s) | Cuts to digital zero |
| Black tail (60.00–60.48 s) | Exact digital silence |
| Dialogue | All checked lines transcribe from the final mix as they do from the production audio |

The mix was **measured, not heard.**

## Stems (`audio/stems/`, not in git; rebuild with `audio/build_all.sh`)
| Stem | Contents |
|---|---|
| `dialogue.wav` | Production audio of every shot, placed exactly as V1 |
| `music.wav` / `music_ducked.wav` | Original score: composed note by note and rendered with FluidSynth + FluidR3_GM samples (MIT) |
| `ambience.wav` / `ambience_ducked.wav` | Production room tone; derived low texture + sub drop; CC0 fluorescent hum |
| `foley.wav` / `foley_ducked.wav` | CC0 Freesound Foley (rug friction, carpet brushing, rope/drape for the yarn, one creak); derived whisper textures and processed tufting gun |
| `premaster.wav`, `master.wav` | The summed mix and the mastered mix |

## Licences
- **Music:** generated here from FluidR3_GM (MIT).
- **Foley:** all CC0 1.0 (Freesound via Openverse). Creators and links are in `audio/FOLEY_SOURCES.json`.
- **Derived sounds:** made from the production's own recordings.
- **Not used:** no commercial recordings, no Pixabay library sounds, no MusicGen.

## Deviations and limitations
- **Music quality:** a General MIDI sample mock-up, not a recorded orchestra.
- **Whisper textures:** made from M1's own whispered take, granulated so that Whisper large-v3 only "hears" its standard hallucinations over non-speech ("תודה", "Thank you for watching"). No words.
- **Stare room tone:** it fades over 59.90–59.95 so the AAC encoder's spill can't reach the black frame.
- **Opening subtitle on shot 18:** the "הם" at the start of the subtitle (40.4 s) may not be spoken. The burst before "בכלל" is rhythmic tufting-gun clicks. Check by ear.
- **HyperFrames project:** `index.html` here plays the four stems at +5.8 dB with no limiter, so it's an edit/audition version. The delivered MP4 is the mastered mux built by `audio/build_all.sh`.
