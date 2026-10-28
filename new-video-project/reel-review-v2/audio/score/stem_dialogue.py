"""DIALOGUE / PRODUCTION stem: every shot's own camera audio exactly as V1 placed it
(same in/out, volume, 20 ms / 30 ms edge fades, same muted shots)."""
from lib import *

def build():
    out = empty()
    for sid, s in TL.items():
        if s["audio"] != "own":
            continue
        clip = load(os.path.join(ROOT, "assets", "media", f"{sid}.mp4"), s["ms"], s["dur"])
        clip = fade(clip, 0.02, 0.03) * s["vol"]
        place(out, clip, s["start"])
    return out

if __name__ == "__main__":
    d = build(); save(os.path.join(STEMS, "dialogue.wav"), d)
    print("dialogue stem", round(len(d) / SR, 3), "s")
