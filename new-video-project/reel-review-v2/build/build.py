"""Generates index.html + compositions/captions.html for REVIEW V1 from one shot table.

Edit the SHOTS / CAPTIONS tables, then run:  python3 build/build.py
Source in/out times are seconds in the ORIGINAL camera file. Each working copy
in assets/media/<id>.mp4 starts at (planned_in - 1.5 s), recorded in MEZZ_T0.
"""
import json, os

FPS = 25
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# working-copy start offsets in the original source (from the cut log)
MEZZ_T0 = {"s01": 4.1, "s02": 3.9, "s03": 18.25, "s04": 4.7, "s05": 0.0, "s06": 2.1, "s07": 7.5, "s08": 17.9,
           "s09": 7.8, "s10": 16.5, "s11": 6.9, "s12": 41.4, "s13": 82.7, "s14": 27.1, "s15": 19.8, "s16": 0.5,
           "s17": 4.5, "s18": 25.9, "s19": 18.3, "s20": 75.5, "s21": 10.1, "s22": 121.1, "s23": 72.5}

# id, source file, in, out, audio ("own" | "mute"), volume, punch-in {scale, ox, oy} or push {from,to}, note
SHOTS = [
    # ACT 1: the man who asks too many questions (fast, documentary)
    ("s02", "P1060609", 5.00, 7.85, "own", 1.0, {"scale": 1.12, "ox": 45, "oy": 28}, "bag to the ear"),
    ("s01", "P1060608", 5.80, 7.80, "own", 1.0, {"scale": 1.0}, "carton overhead"),
    ("s03", "P1060610", 20.10, 22.62, "own", 1.0, {"scale": 1.08, "ox": 50, "oy": 30}, "yoghurt overhead"),
    ("s04", "P1060607", 6.20, 7.60, "own", 0.8, {"scale": 1.2, "ox": 45, "oy": 38}, "clerk's glance"),
    ("s05", "IMG_3156", 0.30, 2.00, "own", 1.0, {"scale": 1.0}, "pizzeria question"),
    ("s06", "IMG_3153", 3.60, 5.70, "own", 1.0, {"scale": 1.3, "ox": 22, "oy": 52}, "scusi + worker"),
    # ACT 2: he goes too far (music-free, slower)
    ("s07", "P1060590", 9.00, 12.35, "own", 1.0, {"scale": 1.0}, "door opens, torch"),
    ("s08", "P1060590", 19.40, 21.45, "own", 1.0, {"scale": 1.15, "ox": 50, "oy": 36}, "line in darkness"),
    ("s09", "P1060565", 9.30, 11.90, "own", 0.9, {"scale": 1.12, "ox": 42, "oy": 48}, "yarn from the carton"),
    ("s10", "P1060570", 18.00, 21.60, "mute", 0.0, {"push": [1.0, 1.25], "ox": 50, "oy": 62}, "THE LABEL (genre turn)"),
    # ACT 3: the rugs speak to him
    ("s11", "P1060579", 8.40, 10.40, "own", 1.0, {"scale": 1.12, "ox": 28, "oy": 76}, "what are you trying to tell me"),
    ("s12", "P1060579", 42.65, 45.25, "own", 1.25, {"scale": 1.45, "ox": 24, "oy": 77}, "whispered"),
    ("s13", "P1060572", 85.00, 87.55, "own", 1.1, {"scale": 1.0}, "plural, close-up"),
    ("s14", "P1060575", 28.05, 30.50, "mute", 0.0, {"scale": 1.1, "ox": 50, "oy": 32}, "lifts head, stares (silence)"),
    # ACT 4: pulled into their world
    ("s15", "P1060573", 21.30, 23.60, "own", 0.85, {"scale": 1.2, "ox": 45, "oy": 32}, "manic hug"),
    ("s16", "P1060576", 2.00, 4.60, "mute", 0.0, {"scale": 1.2, "ox": 50, "oy": 30}, "woman's stare"),
    ("s17", "P1060586", 6.00, 7.70, "own", 0.7, {"scale": 1.0}, "red gallery, caricature"),
    ("s18", "P1060605", 26.90, 30.45, "own", 1.0, {"scale": 1.12, "ox": 38, "oy": 30}, "they don't want to be stepped on"),
    # ACT 5: the dark world of rugs
    ("s19", "P1060591", 19.80, 21.60, "mute", 0.0, {"scale": 1.0}, "torch orb"),
    ("s20", "P1060594", 77.00, 80.00, "own", 0.9, {"scale": 1.1, "ox": 55, "oy": 42}, "half-painted grin"),
    ("s21", "P1060601", 11.60, 13.60, "mute", 0.0, {"scale": 1.0}, "gun fires at lens"),
    ("s22", "P1060594", 124.25, 126.35, "own", 1.0, {"scale": 1.18, "ox": 55, "oy": 48}, "maniacal laugh"),
    # ACT 6: ending
    ("s23", "P1060602", 74.00, 81.20, "own", 1.0, {"push": [1.0, 1.3], "ox": 50, "oy": 40}, "silent stare"),
]
BLACK_TAIL = 0.5

# restrained exposure correction (applied through `hyperframes media-treatment`, never CSS filters)
GRADES = {
    "s20": {"adjust": {"exposure": 0.45, "contrast": 0.06, "shadows": 0.15}},
    "s22": {"adjust": {"exposure": 0.45, "contrast": 0.06, "shadows": 0.15}},
}

# captions: (shot id, source start, source end, text, style)  -- only M1's real dialogue
CAPTIONS = [
    ("s02", 5.15, 6.15, "זה עבודת יד?", "n"),
    ("s02", 7.08, 7.72, "זה עבודת יד?", "n"),
    ("s01", 6.03, 7.62, "זה עבודת יד?\nעשית את זה בעצמך?", "n"),
    ("s03", 20.38, 20.97, "זה עבודת יד?", "n"),
    ("s03", 21.90, 22.58, "עבודת יד?", "n"),
    ("s05", 0.62, 1.64, "סלח לי, זה עבודת יד?", "n"),
    ("s06", 3.78, 4.90, "Scusi, this handjob?", "ltr"),
    ("s08", 19.98, 21.32, "אני לא יוצא מפה בלי תשובות.", "n"),
    ("s11", 8.93, 10.18, "מה אתה מנסה לומר לי?", "n", 960),
    ("s12", 42.73, 44.97, "מה אתה מנסה לומר לי?", "w", 960),
    ("s13", 85.93, 87.42, "מה אתם מנסים לומר לי?", "n"),
    ("s18", 26.98, 30.37, "הם בכלל לא רוצים\nשידרכו עליהם.", "n"),
]


def fr(t):
    return round(t * FPS) / FPS


def main():
    # lay out shots back to back on the frame grid
    t = 0.0; laid = {}
    for sid, src, a, b, aud, vol, cam, note in SHOTS:
        d = fr(b - a); laid[sid] = (fr(t), d, a, b); t = fr(t + d)
    total = fr(t + BLACK_TAIL); story_end = t

    shot_html, cam_js = [], []
    for z, (sid, src, a, b, aud, vol, cam, note) in enumerate(SHOTS, start=1):
        st, d, _, _ = laid[sid]; ms = round(a - MEZZ_T0[sid], 3)
        audio_attr = f'data-has-audio="true" data-volume="{vol}" data-fade-in="0.02" data-fade-out="0.03"' if aud == "own" else "muted"
        shot_html.append(f'''      <!-- {sid} · {src} {a:.2f}→{b:.2f} · {note} -->
      <div id="{sid}-cam" class="cam" style="z-index:{z}">
        <video id="{sid}" class="clip" src="assets/media/{sid}.mp4" data-start="{st:.2f}" data-duration="{d:.2f}" data-media-start="{ms}" data-track-index="1" {audio_attr} playsinline></video>
      </div>''')
        ox, oy = cam.get("ox", 50), cam.get("oy", 50)
        if "push" in cam:
            s0, s1 = cam["push"]
            cam_js.append(f'tl.set("#{sid}-cam", {{ scale: {s0}, transformOrigin: "{ox}% {oy}%" }}, 0);\n'
                          f'      tl.fromTo("#{sid}-cam", {{ scale: {s0} }}, {{ scale: {s1}, duration: {d - 0.04:.2f}, ease: "sine.inOut" }}, {st:.2f});')
        else:
            cam_js.append(f'tl.set("#{sid}-cam", {{ scale: {cam.get("scale", 1.0)}, transformOrigin: "{ox}% {oy}%" }}, 0);')

    # sound beds: room tone under Acts 2-5 (muted shots + continuity), low bed from the label to the laugh
    act2 = laid["s07"][0]; label = laid["s10"][0]; laugh_end = laid["s22"][0] + laid["s22"][1]; stare = laid["s23"][0]
    room_dur = fr(laugh_end - act2); low_dur = fr(laugh_end - label)
    def pts(lst):
        return json.dumps({"version": 1, "lanes": [{"target": "volume", "points": [{"t": round(x, 2), "v": v} for x, v in lst]}]}).replace('"', "&quot;")
    # room tone: low continuous bed; louder over muted shots
    room_pts = [(0, 0.55)]
    for sid in ["s10", "s14", "s16", "s19", "s21"]:
        s, d = laid[sid][0] - act2, laid[sid][1]
        room_pts += [(max(0, s - 0.05), 0.55), (s, 1.0), (s + d - 0.04, 1.0), (s + d, 0.55)]
    room_pts += [(room_dur - 0.02, 0.55)]
    room_pts = sorted(room_pts)
    # low bed: enters under the label, sits low through Act 3, rises through Acts 4-5, hard stop at the laugh's end
    lb = lambda sid: laid[sid][0] - label
    low_pts = [(0, 0.0), (1.2, 0.55), (lb("s11"), 0.45), (lb("s15"), 0.6), (lb("s19"), 0.8), (lb("s22"), 1.0), (low_dur - 0.02, 1.0)]

    index = f'''<!doctype html>
<html lang="he" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <title>REVIEW V1</title>
    <script src="assets/vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; background: #000; overflow: hidden; }}
      .cam {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; overflow: hidden; }}
      .cam video {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920" data-fps="{FPS}">
{chr(10).join(shot_html)}

      <!-- sound design: production room tone (P1060602 silence) and a low bed derived from it -->
      <audio id="roomtone" class="clip" src="assets/media/roomtone.wav" data-start="{act2:.2f}" data-duration="{room_dur:.2f}" data-track-index="5" data-volume="0.35" data-fade-in="0.4" data-automation="{pts(room_pts)}"></audio>
      <audio id="lowbed" class="clip" src="assets/media/lowbed.wav" data-start="{label:.2f}" data-duration="{low_dur:.2f}" data-track-index="6" data-volume="0.5" data-automation="{pts(low_pts)}"></audio>

      <!-- captions: Hebrew dialogue only, RTL -->
      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{story_end:.2f}" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920" style="z-index:100"></div>
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      {(chr(10) + "      ").join(cam_js)}
      tl.set({{}}, {{}}, {total:.2f});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
    open(os.path.join(ROOT, "index.html"), "w").write(index)

    # captions scene
    groups, gjs, spans = [], [], []
    for k, (sid, a, b, text, style, *top) in enumerate(CAPTIONS):
        st, d, ins, _ = laid[sid]
        g0 = fr(st + (a - ins) - 0.06); g1 = fr(st + (b - ins) + 0.12)
        g0 = max(g0, st, 0.12); g1 = min(g1, st + d)
        if g1 - g0 < 0.8:
            g1 = min(st + d, g0 + 0.8)
        spans.append([g0, g1])
    for k in range(len(spans) - 1):  # one caption at a time
        spans[k][1] = min(spans[k][1], spans[k + 1][0])
    for k, (sid, a, b, text, style, *top) in enumerate(CAPTIONS):
        g0, g1 = spans[k]
        topstyle = f' style="top:{top[0]}px"' if top else ""
        text = text.replace("\n", "<br />")
        gid = f"cap{k + 1:02d}"
        dirn = "ltr" if style == "ltr" else "rtl"; lang = "en" if style == "ltr" else "he"
        cls = "cap whisper" if style == "w" else "cap"
        groups.append(f'    <div id="{gid}" class="clip capwrap" data-start="{g0:.2f}" data-duration="{g1 - g0:.2f}"{topstyle}><p class="{cls}" dir="{dirn}" lang="{lang}"><span id="{gid}-t">{text}</span></p></div>')
        gjs.append(f'tl.fromTo("#{gid}-t", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.08, ease: "power2.out" }}, {g0:.2f});\n'
                   f'    tl.to("#{gid}-t", {{ opacity: 0, duration: 0.08, ease: "power2.in" }}, {g1 - 0.08:.2f});')
    caps = f'''<template>
  <style>
    @font-face {{ font-family: "Heebo"; font-weight: 500; src: url("assets/fonts/heebo-hebrew-500.woff2") format("woff2"); unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F; }}
    @font-face {{ font-family: "Heebo"; font-weight: 500; src: url("assets/fonts/heebo-latin-500.woff2") format("woff2"); unicode-range: U+0000-00FF; }}
    @font-face {{ font-family: "Heebo"; font-weight: 700; src: url("assets/fonts/heebo-hebrew-700.woff2") format("woff2"); unicode-range: U+0590-05FF, U+200C-2010, U+20AA, U+25CC, U+FB1D-FB4F; }}
    @font-face {{ font-family: "Heebo"; font-weight: 700; src: url("assets/fonts/heebo-latin-700.woff2") format("woff2"); unicode-range: U+0000-00FF; }}
    #root {{ position: absolute; inset: 0; }}
    .capwrap {{ position: absolute; left: 0; top: 1176px; width: 1080px; height: 140px; display: flex; align-items: center; justify-content: center; }}
    .cap {{ max-width: 820px; text-align: center; font-family: "Heebo", sans-serif; font-weight: 700; font-size: 56px; line-height: 1.22; color: #fff; unicode-bidi: plaintext; }}
    .cap span {{ display: inline; padding: 4px 18px; background: rgba(0, 0, 0, 0.38); border-radius: 10px; box-decoration-break: clone; -webkit-box-decoration-break: clone; text-shadow: 0 2px 6px rgba(0, 0, 0, 0.45); }}
    .cap.whisper {{ font-weight: 500; font-size: 50px; color: rgba(255, 255, 255, 0.86); }}
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
{chr(10).join(groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {(chr(10) + "    ").join(gjs)}
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(caps)

    # human-readable timeline for the report
    with open(os.path.join(ROOT, "TIMELINE.md"), "w") as f:
        f.write("# REVIEW V1 timeline (generated)\n\n| # | id | timeline | source | in → out | dur | audio | note |\n|---|---|---|---|---|---|---|---|\n")
        for n, (sid, src, a, b, aud, vol, cam, note) in enumerate(SHOTS, 1):
            st, d, _, _ = laid[sid]
            f.write(f"| {n} | {sid} | {st:.2f}–{st + d:.2f} | {src} | {a:.2f} → {b:.2f} | {d:.2f} | {aud} | {note} |\n")
        f.write(f"| – | black | {story_end:.2f}–{total:.2f} | – | – | {BLACK_TAIL:.2f} | silence | hard cut to black |\n\n**Total: {total:.2f} s**\n")
    import subprocess
    for sid, g in GRADES.items():
        r = subprocess.run(["npx", "--yes", "hyperframes@0.8.202", "media-treatment", "--project", ROOT, "--file", "index.html",
                            "--selector", f"#{sid}", "--grading", json.dumps(g), "--apply", "--json"], cwd=ROOT, capture_output=True, text=True)
        print("grade", sid, "ok" if '"ok": true' in r.stdout else r.stdout[-400:] + r.stderr[-400:])
    print("total", total, "story", story_end)


if __name__ == "__main__":
    main()
