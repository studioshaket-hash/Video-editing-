"""MIX + MASTER for REVIEW V2.
Ducking is driven by explicit speech windows (the V1 caption windows + M1's vocal moments), not by guesswork.
Master: sum -> peak-safe gain -> two-pass linear loudnorm to -16 LUFS / -1.5 dBTP; digital silence after 60.00 s."""
import re
from lib import *

# relative stem levels (dB)
LEVEL = dict(dialogue=0.0, music=-3.0, ambience=0.0, foley=0.0)
# ducking depth while someone speaks (dB) per stem; "light" windows are non-verbal vocal moments
DUCK = dict(music=-10.0, ambience=-4.0, foley=-7.0)
DUCK_LIGHT = dict(music=-6.0, ambience=-2.0, foley=-4.0)

def speech_windows():
    caps = open(os.path.join(ROOT, "compositions", "captions.html")).read()
    w = [(float(a), float(a) + float(d)) for a, d in re.findall(r'class="clip capwrap" data-start="([0-9.]+)" data-duration="([0-9.]+)"', caps)]
    full = [(max(0, a - 0.12), b + 0.10) for a, b in w] + [(50.72, 52.80)]          # captions + the laugh
    light = [(33.72, 36.04), (45.72, 48.72)]                                         # ecstatic moans in the hug, chuckles under the grin
    return full, light

def envelope(windows, depth_db, attack=0.08, release=0.30):
    g = np.zeros(N, np.float32)
    for a, b in windows: g[sec(a):sec(b)] = 1.0
    # smooth: separate attack/release one-pole filters, run on a 1 kHz control rate
    ctl = g[::48]; y = np.zeros_like(ctl); aa = np.exp(-1 / (attack * 1000)); rr = np.exp(-1 / (release * 1000))
    for i in range(1, len(ctl)):
        c = aa if ctl[i] > y[i - 1] else rr; y[i] = c * y[i - 1] + (1 - c) * ctl[i]
    y = np.repeat(y, 48)[:N]; y = np.pad(y, (0, N - len(y)))
    return db(depth_db * y)

def main():
    st = {k: load(os.path.join(STEMS, k + ".wav")) for k in ["dialogue", "music", "ambience", "foley"]}
    for k in st: st[k] = np.pad(st[k], ((0, max(0, N - len(st[k]))), (0, 0)))[:N] * db(LEVEL[k])
    full, light = speech_windows()
    for k in ["music", "ambience", "foley"]:
        st[k] = st[k] * (envelope(full, DUCK[k]) * envelope(light, DUCK_LIGHT[k]))[:, None]
        save(os.path.join(STEMS, k + "_ducked.wav"), st[k])
    mix = sum(st.values())
    mix[sec(STORY_END):] = 0.0                                   # black frame: complete digital silence
    save(os.path.join(STEMS, "premaster.wav"), mix)
    print("premaster peak dBFS", round(20 * np.log10(np.abs(mix).max() + 1e-12), 2))

if __name__ == "__main__":
    main()
