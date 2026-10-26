#!/usr/bin/env python3
"""Generate the HyperFrames HTML for the Kinusaiga story from edit.json.

edit.json is the single source of truth for cut points, captions, name
emphasis, punch-ins and gain. Run from the project dir: python3 tools/build.py
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
E = json.loads((ROOT / "edit.json").read_text())
FPS = E["fps"]
W, H = 1080, 1920

# Face-centred transform origins (percent of frame) for segments that are scaled.
ORIGIN = {
    "s01": "36% 40%",
    "s09": "45% 40%",
    "s11": "34% 42%",
    "s14a": "22% 36%",
    "s18": "42% 40%",
}

# ---- lay the segments end to end on a frame grid -------------------------
frame = 0
for s in E["segments"]:
    n = round((s["out"] - s["in"]) * FPS)
    s["start"] = round(frame / FPS, 6)
    s["dur"] = round((frame + n) / FPS, 6) - s["start"]  # exact frame edges, no overlap
    frame += n
TOTAL = round(frame / FPS, 6)


def to_edit(seg, src_t):
    """Map a source time inside a segment to edit time (clamped to the segment)."""
    v = seg["start"] + (src_t - seg["in"])
    return round(min(max(v, seg["start"]), seg["start"] + seg["dur"]), 3)


f3 = lambda x: f"{x:.6f}".rstrip("0").rstrip(".")

# ---- index.html ------------------------------------------------------------
frames, sets = [], []
for i, s in enumerate(E["segments"]):
    src = E["sources"][s["src"]]["src"]
    frames.append(
        f'      <div id="w-{s["id"]}" class="frame" style="z-index:{i + 1}">\n'
        f'        <video id="v-{s["id"]}" class="clip" src="{src}" playsinline data-has-audio="true"\n'
        f'          data-start="{f3(s["start"])}" data-duration="{f3(s["dur"])}" data-media-start="{f3(s["in"])}"\n'
        f'          data-volume="{s["gain"]}" data-fade-in="0.01" data-fade-out="0.01" data-track-index="0"></video>\n'
        f"      </div>"
    )
    origin = ORIGIN.get(s["id"], "50% 45%")
    sets.append(f'      tl.set("#w-{s["id"]}", {{ scale: {s["scale"]}, transformOrigin: "{origin}" }}, 0);')
    if "punchInAt" in s:  # hard punch-in mid-segment
        sets.append(
            f'      tl.set("#w-{s["id"]}", {{ scale: {s["punchScale"]} }}, {to_edit(s, s["punchInAt"])});'
        )

index = f"""<!doctype html>
<html lang="he" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #000; }}
      .frame {{ position: absolute; inset: 0; }}
      .frame video {{ position: absolute; left: 0; top: 0; width: {W}px; height: {H}px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{f3(TOTAL)}"
      data-width="{W}" data-height="{H}">
{chr(10).join(frames)}
      <div id="names" data-composition-id="names" data-composition-src="compositions/names.html"
        data-start="0" data-duration="{f3(TOTAL)}" data-track-index="2" data-track-kind="graphics"
        data-width="{W}" data-height="{H}" style="z-index:110"></div>
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{f3(TOTAL)}" data-track-index="1" data-track-kind="captions"
        data-width="{W}" data-height="{H}" style="z-index:100"></div>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      // Per-segment framing and hard punch-ins (scale on the untimed wrapper, never on the video).
{chr(10).join(sets)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
(ROOT / "index.html").write_text(index)

# ---- captions --------------------------------------------------------------
FONT_FACE = """    @font-face { font-family: "Rubik"; font-weight: 300 900; font-display: block;
      src: url("assets/fonts/rubik-hebrew.woff2") format("woff2");
      unicode-range: U+0307-0308, U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F; }
    @font-face { font-family: "Rubik"; font-weight: 300 900; font-display: block;
      src: url("assets/fonts/rubik-latin.woff2") format("woff2");
      unicode-range: U+0000-00FF, U+2013-2014, U+2018-201E, U+2026; }"""


def cap_html(text, hl):
    t = html.escape(text)
    if hl:
        word = text if hl is True else hl
        t = t.replace(html.escape(word), f'<span class="hl">{html.escape(word)}</span>', 1)
    return t


caps, cap_tl = [], []
k = 0
for s in E["segments"]:
    for c in s["captions"]:
        k += 1
        cid = f"c{k:02d}"
        st, en = to_edit(s, c["s"]), to_edit(s, c["e"])
        size = 94 if len(c["text"]) <= 16 else 84
        caps.append(
            f'    <div id="{cid}" class="cap {c["who"]}" dir="rtl" style="font-size:{size}px">'
            f'<span class="txt">{cap_html(c["text"], c.get("hl"))}</span></div>'
        )
        cap_tl.append(f'    show("#{cid}", {st}, {en});')

captions = f"""<template>
  <style>
{FONT_FACE}
    #root {{ position: absolute; inset: 0; }}
    /* Bottom-anchored on the chest: clear of the face and of the Story reply bar. */
    .cap {{
      position: absolute; left: 0; right: 0; bottom: 400px; padding: 0 90px;
      text-align: center; direction: rtl; unicode-bidi: isolate;
      font-family: "Rubik", sans-serif; font-weight: 800; line-height: 1.12;
      color: #fff; opacity: 0; visibility: hidden; overflow: visible; text-wrap: balance;
    }}
    .cap .txt {{
      -webkit-text-stroke: 14px #000; paint-order: stroke fill;
      text-shadow: 0 4px 18px rgba(0, 0, 0, 0.45);
    }}
    .cap.ai {{ color: #a8e9ff; }}
    .cap .hl {{ color: #ffd60a; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}">
{chr(10).join(caps)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // Plain subtitles: hard on, hard off, no animation.
    function show(sel, start, end) {{
      tl.set(sel, {{ opacity: 1, visibility: "visible" }}, start);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, end);
    }}
{chr(10).join(cap_tl)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "captions.html").write_text(captions)

# ---- name emphasis ---------------------------------------------------------
names, name_tl = [], []
for s in E["segments"]:
    m = s.get("emph")
    if not m:
        continue
    nid = f"n-{s['id']}"
    st = round(s["start"] + (m["s"] - s["in"]), 3)
    en = round(s["start"] + (m["e"] - s["in"]), 3)  # may run into a contiguous next segment
    names.append(
        f'    <div id="{nid}" class="nm" dir="rtl"><span class="word">{html.escape(m["text"])}</span></div>'
    )
    name_tl.append(f'    pop("#{nid}", {st}, {en});')

names_html = f"""<template>
  <style>
{FONT_FACE}
    #root {{ position: absolute; inset: 0; }}
    /* Sits in the open ceiling above the head, below the Story progress bar. */
    .nm {{
      position: absolute; left: 0; right: 0; top: 300px; padding: 0 70px;
      text-align: center; direction: rtl; unicode-bidi: isolate;
      opacity: 0; visibility: hidden; overflow: visible;
    }}
    .nm .word {{
      display: inline-block; font-family: "Rubik", sans-serif; font-weight: 900;
      font-size: 168px; line-height: 1; color: #ffd60a;
      -webkit-text-stroke: 18px #000; paint-order: stroke fill;
      text-shadow: 0 8px 26px rgba(0, 0, 0, 0.4);
    }}
  </style>
  <div id="root" data-composition-id="names" data-width="{W}" data-height="{H}">
{chr(10).join(names)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    // One quick pop on the spoken name, then dead still, then a hard cut out.
    function pop(sel, start, end) {{
      tl.set(sel, {{ opacity: 1, visibility: "visible" }}, start);
      tl.fromTo(sel + " .word", {{ scale: 1.35 }}, {{ scale: 1, duration: 0.16, ease: "expo.out" }}, start);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, end);
    }}
{chr(10).join(name_tl)}
    window.__timelines["names"] = tl;
  </script>
</template>
"""
(ROOT / "compositions" / "names.html").write_text(names_html)

print(f"total {TOTAL:.3f}s, {len(E['segments'])} segments, {k} captions, {len(names)} names")
for s in E["segments"]:
    print(f'{s["id"]:5} {s["start"]:7.3f}-{s["start"] + s["dur"]:7.3f} {s["src"]} {s["in"]}')
