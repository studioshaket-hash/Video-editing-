# REVIEW V2: audio cue sheet (for approval)
**Scope:** soundtrack-only revision of REVIEW V1. Picture, timing, captions, grade and length (60.48 s) are unchanged.

**Source labels used below:**

| Label | Meaning |
|---|---|
| **PROD** | Production audio from the shoot, used as recorded |
| **DERIVED** | Made from production recordings by processing (pitch, time-stretch, reverse, filtering, granular scrambling) |
| **MIDI** | Original music I compose note by note, rendered with FluidSynth + the FluidR3_GM sampled instrument set (MIT licence) |
| **OV-CC0 / OV-BY** | Foley recordings from Openverse/Freesound under CC0 or CC BY. CC BY items get credited in `CREDITS.md` |

## Tools actually available
| Tool | Status | Use |
|---|---|---|
| FluidSynth 2.3.4 + FluidR3_GM.sf2 | Installed and test-rendered | Music. Sampled General MIDI instruments (pizzicato strings, contrabass, bassoon, clarinet, celesta, music box, timpani, string ensembles, low percussion). **Mock-up quality, not a recorded orchestra**: limited articulations, no live performance nuance |
| ffmpeg 6.1 (filters) | Installed | Processing, derived textures, reverb, sidechain ducking, loudness |
| Openverse API (Freesound) | Reachable, slow (~40 s per search, 200 searches/day) | Textile/yarn/friction Foley, CC0 preferred |
| Bundled Pixabay SFX (19 files) | Available | Generic UI/whoosh/glitch/riser sounds. **Not planned** (they don't fit the brief) |
| HeyGen music catalog | Not available (no account) | – |
| Google Lyria | Not available (no API key) | – |
| MusicGen | Installable, **not recommended**: model weights are CC-BY-NC-4.0 (non-commercial) | – |
| Commercial sample libraries / DAW | None | – |

## Cue sheet
Times are REVIEW V1 timeline seconds.

### 0:00–0:17.9 · Absurd investigation (shots 1–8)
**Music: MIDI "detective" cue, ~100 BPM, D minor.**
- Pizzicato strings and a walking pizzicato contrabass.
- Light brushed percussion: side-stick, closed hi-hat, shaker.
- A sly staccato bassoon/clarinet line.
- Small rising "question" figures, pizzicato or bassoon, land at the end of each "זה עבודת יד?": ≈0.9, 2.5, 3.9, 5.7, 7.1 and 9.9 s.
- The clerk's glance (7.4 s) gets one muted low-clarinet "hm?" note.
- "Scusi, this handjob?" (≈10.9 s) gets a held, suspended chord. The worker's smile lands on a dry pizzicato button.
- The door opens (12.5 s): the music drops to a half-time bass + soft timpani roll.
- "אני לא יוצא מפה בלי תשובות" (16.4 s): one held bass note under the line.

**Ambience / Foley:**
- **PROD:** supermarket and shop ambience from each clip; the door and handle at 12.5 s.
- **OV-CC0:** door creak/handle sweetener only if the production sound is too thin.
- **No boings or cartoon effects.**

### 0:17.9–0:24.1 · The warning (yarn shot, then the label)
**Music (MIDI):** the detective figure repeats, but it slows, detunes (drifts flat about 30–50 cents) and loses its percussion. The pizzicato thins out.

**Foley:**
- **OV-CC0:** close yarn/thread pulls and fibre slithering as the yarn emerges (18.6–20.5 s).
- **OV-CC0:** subtle fabric scrape.
- **DERIVED:** an unnatural low texture. The yarn sound slowed about 4× and reversed, over the V1 room-tone bed pitched down two octaves.

**Rupture at the label cut (20.52 s), one hit only:**
- **MIDI:** music cuts dead; timpani + low dissonant string cluster + contrabass.
- **DERIVED:** a sub-bass drop made from room tone.
- The cluster decays under the slow push-in.
- No library stinger.

### 0:24.1–0:40.4 · The rugs awaken (shots 11–17)
**Music: MIDI, minimal.**
- A low cello/contrabass pedal and slow string sustains.
- From 29 s, a second voice a semitone away tightens the harmony.
- A celesta fragment of the detective motif, now slow and in a minor mode.
- Manic hug (33.7 s): the motif becomes a music box, slightly detuned. Absurd and unsettling.
- The music box **stops mid-phrase** on the cut to the woman (36.0 s), leaving drone only.
- Red gallery (38.6 s): the drone thickens.

**Foley:**
- **OV-CC0:** fibres, fabric tension, friction and pile rubbing, synced to his hands and face on the rug (24–31 s) and the rug hug (33.7–36 s).
- **OV-CC0:** an electrical hum flickering with the red light (38.6–40.4 s).

**Breath / whisper textures (DERIVED):**
- Made from M1's own whispered takes in P1060579, reversed, granularly scrambled, pitch/formant-shifted and low-passed. **They contain no recognisable words**; I'll check them with Whisper and reject anything it can transcribe.
- Placed only between spoken lines: ≈28.7–29.5 s, under the head lift (31.3–33.7 s, the empty rug-whisper slot), and very low under 36–40 s.

### 0:40.4–0:52.8 · Losing control (shots 18–22)
**Music: MIDI, building.**
- Deep pulses (timpani, low drum and contrabass) accelerate from about 60 to 84 BPM.
- A string cluster crescendo with tremolo.
- Dissonant low brass/strings from 45.7 s.

**Foley / effects:**
- **DERIVED:** the tufting gun's motor, taken from production audio of the tufting shots (P1060605 handles). It's pitch-shifted, reverbed and gated to the pulse.
- **DERIVED:** one processed gun burst synced to the fibres hitting the lens (≈49.1 s).
- **PROD:** M1's laugh (50.7–52.8 s) stays dominant, with the music ducked under it.

### 0:52.8–1:00.0 · The stare
- **Music and all effects cut on the frame** (52.80 s).
- **PROD:** only the stare shot's own near-silent room sound.
- **OV-CC0:** one barely audible fibre creak (≈57.5 s, around −45 dBFS).

### 1:00.0–1:00.48 · Black
Complete digital silence.

## Mix
- **Dialogue:** every one of the 13 spoken lines is kept from production audio, untouched apart from light EQ and level.
- **Ducking:** music and effects are sidechain-ducked about 8–10 dB under speech and the laugh.
- **Dynamics:** quiet stretches stay quiet, to avoid constant loudness.
- **Target:** about −16 LUFS integrated, true peak ≤ −1.5 dBTP, measured on the final file.

## Delivery
- **Picture:** the mixed soundtrack is muxed onto REVIEW V1's video stream **copied bit-for-bit**, so the picture can't change. The file is `REVIEW_V2_SOUNDTRACK.mp4`. The V1 files stay untouched.
- **Editable stems:** stems (dialogue, music, Foley, derived textures) and the MIDI/score scripts go into a `reel-review-v2/` copy of the HyperFrames project.
- **Credits:** any CC BY sounds are listed in `CREDITS.md`.
- **Caveat:** the mix will be measured, not heard.
