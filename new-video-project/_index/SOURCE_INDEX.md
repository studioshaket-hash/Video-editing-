# Source Footage Index: Instagram Reel (1080×1920, 9:16, ~60 s)

**Status:** Folder A: 50 of 63 clips indexed, from the replacement folder. Folder B: fully indexed (72 unique files).
Not yet available: **P1060611–P1060623** (13 clips, missing from the replacement folder).
No editing, timeline, shot selection or rendering has been done.

## Files
| File | What it is |
|---|---|
| `SOURCE_INDEX.md` | This summary: overview, categories, strongest moments, dialogue, redundancy, limitations |
| `shot_index_ALL.csv` | **Combined searchable index**, one row per unique file (50 A videos + 31 B videos + 41 B photos = 122 rows). Columns: metadata, scene, people, rugs/objects, description, key timestamps, camera, dialogue, 9:16 fit, tags, rating, redundancy |
| `shot_index_folderA.csv` / `shot_index_folderB.csv` | The same rows, split by folder |
| `notes_A_videos.md`, `notes_B_videos.md`, `notes_B_photos.md` | Longer scene-by-scene visual notes |
| `folderA_transcripts_auto.json`, `folderB_transcripts_auto.json` | Automatic transcripts with timestamps (Whisper medium). Approximate, verify by ear |
| `folderB_duplicates.csv` | md5 duplicate map for Folder B |
| `../_meta/` | Drive inventories, file IDs (original and replacement), ffprobe JSON for every clip, audio track levels |

**People** (described, not named):
- **M1**: main talent. Moustache, curly dark hair, pink overshirt + cream tee, or the cream tee alone.
- **M2**: kiosk clerk. Grey tee, moustache.
- **W1**: a woman with curly hair, white crop top and lilac trousers.
- **M3**: tattooed photographer (BTS photos only).
- **Counter worker** at the pizzeria (Folder B).

Crew can be heard calling M1 "Shir".

---

## 1. Unified footage summary

| | Folder A (Panasonic main camera) | Folder B (iPhone 15 Pro Max) |
|---|---|---|
| Files | 50 video clips (of 63) | 31 videos + 41 photos (68 duplicate uploads removed) |
| Total running time | ~25.8 min | ~3 min video |
| Format | 3840×2160 + 90° rotation flag → **plays vertical 2160×3840 (native 9:16)**. Only **P1060561 is horizontal** | All vertical. Videos are 4K or 1080p, 9:16. Photos are 9:16 JPGs or 3:4 HEICs |
| Codec / fps | 561–577: H.264 50p ~800 Mb/s · 578–610: HEVC 10-bit 25p ~144 Mb/s | HEVC 30 fps |
| Audio | Yes on all clips: 4 × PCM mono; tracks 1–2 are the camera mic, 3–4 silent. Mostly crew direction plus a few M1 lines | Yes on all clips (AAC). Includes the "handmade?" street dialogue |

Both folders were shot on 30 Apr 2025 at the same tufting studio and nearby shops. The 9:16 delivery is easy: everything except P1060561 is already vertical, and the 4K sources leave room to punch in.

**Scenes available:**
1. **Milk carton full of yarn** (kitchenette, cyan wall), A 561–570.
   - M1 finds a milk carton with yarn spilling out of it, investigates it, drops it, shakes it.
   - The carton's handwritten label reads **"השאלות שלך עוד יארגו אותך!"** ("Your questions will end up weaving you!"), a threat-like pun.
2. **Zebra-rug obsession** (studio, teal chalkboard wall), A 571–581 and B photos 3044–3084, IMG_3062/63/74.
   - Face-down worship of the rug, plus whispering "What are you trying to tell me?" to it.
   - A manic hug of the rolled rug.
   - Stares into the lens and an empty-rug frame. A **second person (W1) crawls onto the rug and stares too**.
   - Colour-shifting red/blue light.
3. **Dark red-lit gallery** (rug art + tools), A 582–588 and B 3087–3101.
   - A framed disassembled tufting gun.
   - A tufted guitar rug under pulsing light.
   - The Hebrew-lettering rug, a caricature rug of a grinning man on a toilet, the panda rug.
   - Yarn shelves and piles of tufting guns.
4. **Break-in with a torch** (entrance hall), A 589–593.
   - A door opens from darkness and M1 enters with a torch.
   - Hidden-observer views through hose coils; W1 watching from outside.
   - Line: "I'm not leaving here without answers".
5. **Face-paint under the rugs** (lilac wall), A 594 and B 3105.
   - M1, half his face painted white, grins under the caricature's identical grin, ending in a maniacal laugh.
6. **Tufting gun as a weapon** (dark room), A 595–601 and B 3114–3118.
   - A tufting gun with a light on its nose, aimed like a firearm.
   - It fires yarn, and is pointed straight at the lens until fibres burst toward the camera.
7. **Interrogation stare**, A 602: 90 s tight close-up of M1 in the dark, silent stare that ends in a creepy grin.
8. **Tufting work at night**, A 603–605.
   - Real tufting on the frame.
   - M1 glares at camera while tufting and says "They don't even want to be stepped on".
9. **"Is this handmade?" in shops.**
   - Supermarket: A 607–610 and B 3136–3144.
   - Burger display, pizzeria, cafeteria: B 3149–3160 (only the iPhone covers these).
   - Includes the clerk's uneasy glances, products held overhead and "listened to", the repeated "Is this handmade? Did you make it yourself?", and the "Scusi, this handjob?" pun with the laughing worker.
10. **Street establisher**, A 606 ("EXPRESS MARKET" corner shop). **BTS photos** of the crew and garden break are in B.

---

## 2. Categorized shot index
Full detail is in `shot_index_ALL.csv`. ★ = rating out of 5.

### A. Obsessive investigation: "is this handmade?"
| Clip | ★ | Moment |
|---|---|---|
| A P1060609 | 5 | Holds a bag of nuts to his ear as if listening (6.2–9.1); rapid "Is this handmade?" ×3 (0.7) |
| A P1060608 | 4 | Carton thrust overhead (6.2–12.0); "Is this handmade? Did you make it yourself?" (4.0–12.4, 36.5–40.5, "Yes" 40.5); off-screen arm with a spray bottle (21.1–22.6) |
| A P1060610 | 4 | Knowing grin at camera (6.2); yoghurt held overhead (21.1–24.0); "Is this handmade?" (10.0, 20.4, 21.9) |
| B IMG_3141 | 5 | Low hero angle, bag lifted overhead with a rapt gaze (6.0–11.4); "Is this handmade?" |
| B IMG_3138 / 3139 | 4 / 3 | iPhone angle of the same overhead inspection plus Q&A |
| B IMG_3152–3156 | 3–5 | Pizzeria: "Excuse me, is this handmade?" → "Scusi, this handjob?"; worker laughs (3153 @3.0–5.4) |
| B IMG_3150, 3160 | 3 | Peering through burger glass; cafeteria arms-wide gesture |
| A P1060563–565 | 3–4 | Puzzled at the milk carton: head-scratch (563 @7.8), yarn dangling out (565 @9.3–12.3) |
| A P1060566 | 4 | Extreme low angle explaining the yarn carton to camera (19.8 lean-in grin) |

### B. Rugs: worship, hugging, talking to them
| Clip | ★ | Moment |
|---|---|---|
| A P1060579 | 4 | Face-down on the rug whispering "What are you trying to tell me?" (9–59 s); grimaces 24.0, 32–37, 48 |
| A P1060572 | 5 | Face-down worship: daylight 0–49, red light 56–65, close-up 73.9–89; same line |
| A P1060573 | 5 | Kneeling, clutching the rug like a lover; ecstatic/manic 7.8–28.8 (peak 21.3–24.3) |
| A P1060581 | 5 | Rug hug: deadpan (0–12) → punch-in laughter (14.9–30.2) |
| A P1060578 | 4 | Bows into the rug (4.8–12), sly smile (13.4), collapses onto it (16.8–18.2) |
| A P1060575 | 4 | Face in the rug under shifting red/blue light (15–29), stare into lens (30.3) |
| A P1060580 | 3 | Static rug hug (superseded by 581) |
| B photos 3056–3059, 3079–3081 | 5 | Native 9:16 stills: face mashed into the rug; belly-laugh hug |

### C. Unsettling / surreal / mysterious
| Clip | ★ | Moment |
|---|---|---|
| A P1060571 | 5 | Rises from the rug and stares into the lens (4.8–7.8); **empty rug** (10.8–18.3); legs return (19.8) |
| A P1060576 | 5 | **W1** crawls onto the rug and holds a dead-eyed stare (1.8–9.3) |
| A P1060602 | 5 | 90 s silent stare in the dark; eyes dart (43–47); creepy grin (1:28.3) |
| A P1060594 | 5 | Half-painted face grinning under the caricature (1:16–1:26); maniacal laugh (2:02–2:06); clean plate 0–10 |
| A P1060605 | 5 | Tufting at night, glares at camera (21.6–33.6, 47.0–53.3) |
| A P1060589–593 | 3–4 | Dark hall with light strip, door opens, M1 with a torch; hose-coil observer POV (593); W1 watching (592 @7.7–10.6) |
| A P1060577 | 4 | Low-key pleading/beckoning to the lens from the rug (15.3–28.8) |
| A P1060562 / 570 | 4 | Label insert: "Your questions will end up weaving you!" (570 @16.8–31.8 cleanest) |
| A P1060584 / 585 | 3 / 4 | Torch finds the tufted guitar (16.8–19.7); pulsing red light on the guitar (4.8–19.7) |
| A P1060586 | 4 | Nightmarish red handheld: Hebrew rug, toilet-caricature (6.2–7.7), panda extreme close (21–25) |
| A P1060582 | 3 | Framed tufting-gun "evidence"; hand shadow on the tool wall (49.4) |

### D. Tufting gun as a weapon
| Clip | ★ | Moment |
|---|---|---|
| A P1060601 | 5 | Gun aimed at the lens, fibres explode at camera (12.0–13.4) |
| A P1060600 | 4 | Gun aimed at the lens, star-burst flare |
| A P1060597 | 4 | Gun fires yarn (7.7–10.6, 18.2–22.6); man in sunglasses passes holding it (25.4–26.9) |
| A P1060595 | 4 | Clean side-on aim with fibre spray (12.0–14.9) |
| A P1060596 / 598 / 599 | 2–3 | More passes |
| B IMG_3117 | 4 | iPhone angle, fibre spray (~3.7) |

### E. Craft process / tools / materials
| Clip | Moment |
|---|---|
| A P1060603 | Tufting on the frame: 6.2–12.0, 22.6–24.0 |
| A P1060604 | Tufting 0–13.4; M1 face lit by work light 30.2–34.6 |
| A P1060587 + B IMG_3099 | Yarn shelves |
| A P1060588 + B IMG_3101 | Tufting guns on a ring rug; close-ups 25.4–34.6 |
| B IMG_3087/88, A P1060582 | Framed tufting gun |
| B IMG_3095, A P1060586 | Hebrew-lettering rug |

### F. Reactions from others
| Clip | Moment |
|---|---|
| A P1060607 | Kiosk clerk's uneasy sideways glances: 6.2–13.4, 18.2–24.0 |
| B IMG_3153 | Counter worker laughing |
| A P1060592 | W1 watching from the doorway |
| A P1060576 | W1 copying M1's behaviour |

### G. Location / BTS
- A P1060606: street establisher.
- B IMG_3104: placard on a fence.
- B BTS photos 3044–3048 and garden photos 3131–3134.

---

## 3. Strongest storytelling moments (both folders)
1. **A P1060609 @6.2–9.1**: M1 holds a product to his ear, "listening" whether it's handmade. Pure absurd investigation.
2. **A P1060608 @4.0–12.4**: "זה עבודת יד? עשית את זה בעצמך?" ("Is this handmade? Did you make it yourself?") while the product is thrust overhead.
3. **B IMG_3141 @6.0–11.4**: low-angle rapture, product lifted to the light.
4. **B IMG_3153 @3.0–5.4**: the counter worker laughs at "Scusi, this handjob?".
5. **A P1060607 @6.2–13.4**: the clerk's suspicious sideways glances (a witness).
6. **A P1060565 @9.3–12.3** and **A P1060570 @16.8–31.8**: yarn pours out of the milk carton; the label "Your questions will end up weaving you!".
7. **A P1060579 @9–59**: whispering "What are you trying to tell me?" into the rug.
8. **A P1060573 @21.3–24.3**: manic ecstatic hug of the zebra rug.
9. **A P1060581 @14.9–30.2**: belly-laugh hug after the punch-in.
10. **A P1060571 @4.8–7.8, then 10.8–18.3**: stare into the lens, then he's gone and the rug sits empty.
11. **A P1060576 @1.8–9.3**: W1 on the rug with the same dead stare ("it's spreading").
12. **A P1060590 @4.9 / P1060589 @22.6–37.4**: the door bursts open, torch in hand, "I'm not leaving here without answers".
13. **A P1060602 @0–43 and 1:28.3**: the silent interrogation stare and the final creepy grin.
14. **A P1060605 @21.6–33.6**: glaring while tufting at night: "They don't even want to be stepped on".
15. **A P1060594 @1:16–1:26 and 2:02–2:06**: half-painted face mirroring the caricature's grin, then a maniacal laugh.
16. **A P1060601 @12.0–13.4**: the tufting gun "shoots" yarn straight at the viewer.
17. **A P1060585 @4.8–19.7**: the tufted guitar under pulsing red light (tension/beat bed).
18. **B IMG_3105**: iPhone panda face-paint shot (bright, 1080p): a lighter alternative to 594.

## 4. Dialogue and reactions most useful for dark comedy
Automatic transcripts; check by ear before use.

**On-camera lines by M1:**
| Line | Translation | Where |
|---|---|---|
| "זה עבודת יד? עשית את זה בעצמך?" | "Is this handmade? Did you make it yourself?" | A 608 @4.0, 8.4, 12.4, 36.5 (answer "כן" / "Yes" @40.5); A 610 @10.0, 20.4, 21.9; B 3138, 3139, 3141, 3155, 3156 |
| "זה עבודת יד" ×3 (rapid) | "Is this handmade?" | A 609 @0.7 |
| "מה אתה מנסה לומר לי?" | "What are you trying to tell me?" (to the rug) | A 579 @9–59 (whispered takes ~39–59); A 572 |
| "אני לא יוצא מפה בלי תשובות" | "I'm not leaving here without answers." | A 590 @4.9 |
| "הם בכלל לא רוצים שידריכו עליהם" | "They don't even want to be stepped on." (about rugs) | A 605 @4.0, 25.5, 39.5, 41.5. Avoid the crew swear at 51.2 |
| "Scusi, this handjob?" | (pun on "handmade") | B 3152–3156; worker: "מעולה!" / "Excellent!" (3153), "Nice" (3154) |
| "Chips! What do I put in the pita?" | (cafeteria banter) | B 3160 |

**Non-verbal reactions:**
- M1's maniacal laugh vocals ("ah-ah-ah") in A 594 (~1:44–2:06).
- The clerk's uneasy glances (A 607).
- The worker's laugh (B 3153).
- W1's stare (A 576).

**Label text usable as a caption:** "השאלות שלך עוד יארגו אותך!" ("Your questions will end up weaving you!"), A 562 / 570.

**Crew audio to avoid:**
- Most of Folder A carries director cues ("Go", "Nice", lighting talk).
- A 600 has a crew member shouting "SHOOT" (could be repurposed, but it's crew).
- A 566 contains the direction "start with 'what the fuck', continue to trembling and drop", so M1's performance there may include a "what the fuck".

## 5. Irrelevant or redundant footage
- **Unusable:**
  - A P1060583 (black/red blur).
  - A P1060574 (nearly black; maybe a grade-pushed silhouette).
  - B IMG_3089, IMG_3122, IMG_3123.
  - Most of A P1060582 after 55 s.
- **Redundant takes:**
  - Carton: A 563/564/565, 566/567, 568/569.
  - Torch: A 589/590/591, 592/593.
  - Gun: A 595–599.
  - Rug: A 580 (vs 581), 572 vs 579 (similar face-down), 575.
- **Cross-folder doubles** (the iPhone shot the same moments; Folder A is usually higher quality):
  - B 3138/3139 ≈ A 608; B 3136 ≈ A 607; B 3105 ≈ A 594
  - B 3114–3118 ≈ A 595–599; B 3099 ≈ A 587; B 3101 ≈ A 588; B 3087/3088 ≈ A 582
  - B rug photos ≈ A 572–581
- **Folder B duplicates:** 68 identical uploads, listed in `folderB_duplicates.csv`.

## 6. Limitations
- **13 Folder A clips are missing** from the replacement folder: P1060611–P1060623 (~5.6 GB). The original copies are still quota-blocked.
- **Folder A was sampled, not watched in full:**
  - Frames were taken every ~1.4–3.3 s, from keyframes only.
  - Audio was fully fetched and transcribed, but only automatically. Hebrew ASR mishears some words, and repeated lines can be partly hallucinated (e.g. 579's evenly spaced repeats), so confirm by ear.
- **Lighting:**
  - Several dark clips (574, 582–586, 589–601) are very dim in the samples and will need grading.
  - 594 is dim purple.
- **P1060561** is the only horizontal clip. Cropping it to 9:16 loses part of the yarn tail.
- **People are described, not identified.** The crew calls M1 "Shir", but that isn't confirmed as his name.
