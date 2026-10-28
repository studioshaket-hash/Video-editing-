"""Shared helpers for the REVIEW V2 soundtrack: audio I/O through ffmpeg, the V1 shot timeline,
a small MIDI writer (times in seconds) and FluidSynth rendering with the FluidR3_GM soundfont (MIT)."""
import importlib.util, json, os, struct, subprocess
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))            # reel-review-v2/
STEMS = os.path.join(ROOT, "audio", "stems")
SRC = os.path.join(ROOT, "audio", "src")
SF2 = "/usr/share/sounds/sf2/FluidR3_GM.sf2"
os.makedirs(STEMS, exist_ok=True); os.makedirs(SRC, exist_ok=True)


# ---------------------------------------------------------------- timeline (identical to V1)
def _build():
    spec = importlib.util.spec_from_file_location("v1build", os.path.join(ROOT, "build", "build.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

B = _build()

def timeline():
    """{sid: dict(start, dur, src_in, src_out, audio, vol, media_start)} on the 25 fps grid, plus totals."""
    t = 0.0; out = {}
    for sid, src, a, b, aud, vol, cam, note in B.SHOTS:
        d = B.fr(b - a); out[sid] = dict(start=B.fr(t), dur=d, src=src, a=a, b=b, audio=aud, vol=vol, ms=round(a - B.MEZZ_T0[sid], 3), note=note)
        t = B.fr(t + d)
    return out, B.fr(t), B.fr(t + B.BLACK_TAIL)

TL, STORY_END, TOTAL = timeline()
N = int(round(TOTAL * SR))


# ---------------------------------------------------------------- audio I/O
def load(path, start=0.0, dur=None, mono=False):
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", f"{start:.4f}"]
    if dur is not None: cmd += ["-t", f"{dur:.4f}"]
    cmd += ["-i", path, "-vn", "-f", "f32le", "-ac", "1" if mono else "2", "-ar", str(SR), "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).copy()
    return a if mono else a.reshape(-1, 2)

def save(path, a):
    a = np.asarray(a, np.float32)
    if a.ndim == 1: a = np.stack([a, a], 1)
    subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-c:a", "pcm_s24le", "-y", path],
                   input=a.tobytes(), check=True)

def ffx(a, af):
    """Run a stereo buffer through an ffmpeg audio filter chain."""
    a = np.asarray(a, np.float32)
    if a.ndim == 1: a = np.stack([a, a], 1)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-nostdin", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", "-af", af,
                          "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], input=a.tobytes(), capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()

def place(buf, clip, t, gain=1.0):
    """Mix clip into buf starting at t seconds (clip stereo)."""
    if clip.ndim == 1: clip = np.stack([clip, clip], 1)
    i = int(round(t * SR)); j = min(len(buf), i + len(clip))
    if i < 0: clip = clip[-i:]; i = 0
    if j > i: buf[i:j] += clip[: j - i] * gain
    return buf

def fade(a, fin=0.0, fout=0.0):
    a = a.copy(); n = len(a)
    if fin > 0:
        k = min(n, int(fin * SR)); a[:k] *= np.linspace(0, 1, k)[:, None]
    if fout > 0:
        k = min(n, int(fout * SR)); a[n - k:] *= np.linspace(1, 0, k)[:, None]
    return a

def db(x): return 10 ** (x / 20)

def empty(): return np.zeros((N, 2), np.float32)

def sec(t): return int(round(t * SR))


# ---------------------------------------------------------------- MIDI (times in seconds: tempo 60 bpm, 960 ticks/s)
TPQ = 960
def _vlq(n):
    b = [n & 0x7F]; n >>= 7
    while n: b.append((n & 0x7F) | 0x80); n >>= 7
    return bytes(reversed(b))

def write_midi(path, parts):
    """parts: list of dict(prog, ch, notes=[(t, dur, pitch, vel)], cc=[(t, ctrl, val)], bend=[(t, cents)])"""
    chunks = []
    tempo = b"\x00\xff\x51\x03" + (1_000_000).to_bytes(3, "big") + b"\x00\xff\x2f\x00"
    chunks.append(b"MTrk" + struct.pack(">I", len(tempo)) + tempo)
    for p in parts:
        ch = p["ch"]; ev = [(0, 0, bytes([0xB0 | ch, 101, 0])), (0, 0, bytes([0xB0 | ch, 100, 0])), (0, 0, bytes([0xB0 | ch, 6, 2])),  # bend range ±2 semitones
                            (0, 1, bytes([0xC0 | ch, p["prog"]]))]
        for t, ctrl, val in p.get("cc", []): ev.append((int(t * TPQ), 2, bytes([0xB0 | ch, ctrl, int(max(0, min(127, val)))])))
        for t, cents in p.get("bend", []):
            v = int(8192 + max(-8191, min(8191, cents / 200 * 8191))); ev.append((int(t * TPQ), 2, bytes([0xE0 | ch, v & 0x7F, v >> 7])))
        for t, d, pitch, vel in p["notes"]:
            ev.append((int(t * TPQ), 4, bytes([0x90 | ch, pitch, int(max(1, min(127, vel)))])))
            ev.append((int((t + d) * TPQ), 3, bytes([0x80 | ch, pitch, 0])))
        ev.sort(key=lambda e: (e[0], e[1]))
        data = b""; last = 0
        for t, _, e in ev: data += _vlq(t - last) + e; last = t
        data += b"\x00\xff\x2f\x00"
        chunks.append(b"MTrk" + struct.pack(">I", len(data)) + data)
    open(path, "wb").write(b"MThd" + struct.pack(">IHHH", 6, 1, len(chunks), TPQ) + b"".join(chunks))

def render(parts, name, reverb=0.35, gain=0.6):
    """Render MIDI parts with FluidSynth; returns stereo float32 at SR (t=0 is the cue start)."""
    mid = os.path.join(HERE, name + ".mid"); wav = os.path.join(HERE, name + ".wav")
    write_midi(mid, parts)
    subprocess.run(["fluidsynth", "-ni", "-g", str(gain), "-r", str(SR), "-o", "synth.reverb.active=1", "-o", f"synth.reverb.room-size={reverb}",
                    "-o", "synth.reverb.width=0.8", "-o", "synth.reverb.level=0.5", "-o", "synth.chorus.active=0", "-F", wav, SF2, mid],
                   check=True, capture_output=True)
    return load(wav)
