"""DERIVED textures, made only from production recordings (plus CC0 Foley where noted):
- whispers: granular re-synthesis of M1's own whispered take (P1060579, 42.75-44.95), reversed/pitched/filtered and
  blended into carpet-fibre brushing so nothing intelligible survives (checked with Whisper afterwards)
- low texture + sub drop: P1060602 room tone pitched down 2-3 octaves
- tufting-gun pulses + burst: P1060601 gun motor (11.3-14.3), pitched down, reverbed, gated to the score's pulse."""
from lib import *

rng = np.random.default_rng(20260428)        # seeded: every rebuild is identical
MEDIA = os.path.join(ROOT, "assets", "media")
FOLEY = os.path.join(SRC, "foley")
OUT = os.path.join(SRC, "derived"); os.makedirs(OUT, exist_ok=True)


def resample(x, factor):  # factor < 1 -> lower pitch, longer
    n = int(len(x) / factor); return np.interp(np.linspace(0, len(x) - 1, n), np.arange(len(x)), x).astype(np.float32)


def granular(src, dur, density=13, gmin=0.04, gmax=0.11, pitch=(0.62, 0.8), rev=0.6):
    out = np.zeros(int(dur * SR) + SR, np.float32)
    for _ in range(int(dur * density)):
        g = int(rng.uniform(gmin, gmax) * SR); p = rng.integers(0, len(src) - g)
        grain = src[p:p + g] * np.hanning(g)
        if rng.random() < rev: grain = grain[::-1]
        grain = resample(grain, rng.uniform(*pitch)) * rng.uniform(0.4, 1.0)
        t = int(rng.uniform(0, dur) * SR); out[t:t + len(grain)] += grain[: len(out) - t]
    return out[: int(dur * SR)]


def whispers():
    w = load(os.path.join(MEDIA, "s12.mp4"), 1.35, 2.2, mono=True)       # s12 working copy starts at 41.40 -> 42.75-44.95
    w = w / (np.abs(w).max() + 1e-9)
    brush = load(os.path.join(FOLEY, "fibre_brush.wav"), 1.5, 4.2, mono=True); brush /= (np.abs(brush).max() + 1e-9)
    res = {}
    for name, dur, env_in, env_out in [("whisper_a", 0.95, 0.25, 0.4), ("whisper_b", 2.2, 0.6, 0.8), ("whisper_c", 2.1, 0.8, 0.9)]:
        g = granular(w, dur)
        b = brush[: len(g)] * 0.55
        mix = np.stack([g * 0.9 + b * 0.5, g * 0.6 + b * 0.8], 1)           # slight width: the sound sits "in" the fabric
        mix = ffx(mix, "highpass=f=380,lowpass=f=2600,aecho=0.7:0.6:45|90:0.25|0.15")
        mix = fade(mix[: int(dur * SR)], env_in, env_out)
        mix /= (np.abs(mix).max() + 1e-9)
        save(os.path.join(OUT, name + ".wav"), mix); res[name] = mix
    return res


def low_texture():
    rt = load(os.path.join(MEDIA, "roomtone.wav"), 0, 8.0, mono=True)
    yarn = load(os.path.join(FOLEY, "yarn_drape.wav"), 0.2, 3.2, mono=True)[::-1]
    lo = resample(rt, 0.25)[: int(6.3 * SR)]                              # room tone two octaves down
    ys = resample(yarn, 0.3)[: int(6.3 * SR)]                             # reversed yarn, slowed ~3x
    ys = np.pad(ys, (0, max(0, len(lo) - len(ys))))
    tex = ffx(np.stack([lo + ys * 0.35, lo * 0.9 + ys * 0.45], 1), "lowpass=f=420,highpass=f=28")
    tex /= (np.abs(tex).max() + 1e-9); save(os.path.join(OUT, "low_texture.wav"), tex)
    sub = resample(load(os.path.join(MEDIA, "roomtone.wav"), 10, 1.0, mono=True), 0.125)[: int(3.2 * SR)]
    env = np.minimum(1, np.arange(len(sub)) / (0.012 * SR)) * np.exp(-np.arange(len(sub)) / (0.9 * SR))
    sub = ffx(sub * env, "lowpass=f=110,highpass=f=24"); sub /= (np.abs(sub).max() + 1e-9)
    save(os.path.join(OUT, "sub_drop.wav"), sub)
    return tex, sub


def gun():
    motor = load(os.path.join(MEDIA, "s21.mp4"), 1.4, 2.8, mono=True)    # s21 copy starts at 10.10 -> 11.5-14.3 (steady motor)
    onset = load(os.path.join(MEDIA, "s21.mp4"), 1.2, 0.9, mono=True)    # motor start transient
    low = resample(motor, 0.5); low = np.tile(low, 3)
    proc = ffx(low, "highpass=f=60,lowpass=f=1800,aecho=0.6:0.5:70|140:0.3|0.2"); proc /= (np.abs(proc).max() + 1e-9)
    # gate to the score's accelerating pulse (same formula as cue_E)
    t0, t1 = 40.36, 52.80; t = 0.0; beats = []
    while t0 + t < t1 - 0.05:
        beats.append(t); bpm = 60 + 24 * (t / (t1 - t0)) ** 1.3; t += 60 / bpm
    n = int((t1 - t0) * SR); gate = np.zeros(n, np.float32)
    for b in beats:
        i = int(b * SR); k = np.arange(min(n - i, int(0.45 * SR))); gate[i:i + len(k)] = np.maximum(gate[i:i + len(k)], np.exp(-k / (0.13 * SR)))
    ramp = np.linspace(0.35, 1.0, n) ** 1.5
    src = np.resize(proc[:, 0], n)
    pulses = fade(np.stack([src * gate * ramp] * 2, 1), 0.05, 0.004)
    save(os.path.join(OUT, "gun_pulses.wav"), pulses)
    burst = ffx(resample(onset, 0.7), "highpass=f=80,aecho=0.7:0.6:60|130:0.35|0.25"); burst = fade(burst, 0.003, 0.6); burst /= (np.abs(burst).max() + 1e-9)
    save(os.path.join(OUT, "gun_burst.wav"), burst)
    return pulses, burst


if __name__ == "__main__":
    w = whispers(); tex, sub = low_texture(); p, b = gun()
    for k, v in list(w.items()) + [("low_texture", tex), ("sub_drop", sub), ("gun_pulses", p), ("gun_burst", b)]:
        print(k, round(len(v) / SR, 2), "s")
