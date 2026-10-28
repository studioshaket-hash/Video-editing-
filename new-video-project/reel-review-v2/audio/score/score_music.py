"""MUSIC stem: original score, composed note by note, rendered with FluidSynth + FluidR3_GM (MIT).
D minor. Restraint first: sparse pizzicato bass and woodwinds, one musical accent in Act 1,
music drops out under the pun, hard cuts at the label (20.52 s) and the stare (52.80 s).
All times are V1 timeline seconds; each cue is rendered on its own and gated to its window."""
from lib import *

# GM programs (0-based)
PIANO, CELESTA, MUSICBOX, PIZZ, BASS_AC, CELLO, CONTRA, TREM, STR1, STR_SLOW, TIMP, BASSOON, TROMBONE, TUBA, VIOLIN = \
    0, 8, 10, 45, 32, 42, 43, 44, 48, 49, 47, 70, 57, 58, 40
D1, A1, Bb1, C2, Cs2, D2, Eb2, E2, F2, Fs2, G2, A2, Bb2, D3, Eb3, E3, F3, A3, Bb3, D4, E4, F4, G4, A4, Bb4, D5, E5, F5, A5, Bb5 = \
    26, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 45, 46, 50, 51, 52, 53, 57, 58, 62, 64, 65, 67, 69, 70, 74, 76, 77, 81, 82

BEAT = 60 / 96          # Act 1 tempo
def B_(bar, beat=0.0):  # bar (0-based) + beat -> seconds
    return (bar * 4 + beat) * BEAT


def cue_A():  # 0.00-10.80 documentary investigation
    bass = [(B_(0), .5, D2, 68), (B_(0, 2), .4, A1, 56), (B_(1), .5, D2, 66), (B_(1, 2), .35, F2, 54), (B_(1, 3), .3, E2, 50),
            (B_(2), .5, D2, 64), (B_(2, 2), .4, A1, 54), (B_(3), 1.1, Bb1, 60), (B_(3, 2), .45, A1, 52), (B_(4), .4, D2, 56)]
    piano = []
    for bar, figure in [(0, [(1, D4), (1.5, F4), (2, E4), (3, A3)]), (1, [(1, D4), (1.5, F4), (2, G4), (2.5, F4), (3, E4)]),
                        (2, [(1, D4), (1.5, F4), (2, E4), (3, A3)]), (3, [(1.5, Bb3), (3, A3)])]:
        piano += [(B_(bar, b), .22, p, 44) for b, p in figure]
    pad = [(0, 5.0, D3, 34), (0, 5.0, A3, 30), (5.0, 2.5, Bb2, 34), (5.0, 2.5, F3, 30), (7.5, 3.3, A2, 34), (7.5, 3.3, E3, 28)]
    # the one accent of Act 1: a sly low bassoon question under the clerk's silent glance (7.36-8.76)
    bassoon = [(7.62, .32, A2, 62), (8.0, .22, Bb2, 58), (8.28, .5, A2, 54)]
    perc = []
    for bar in range(5):
        for k in range(8):
            t = B_(bar, k * .5)
            if t < 10.7: perc.append((t, .05, 42, 20 + (6 if k % 2 else 0)))   # closed hat, very soft
        if B_(bar, 3) < 10.7: perc.append((B_(bar, 3), .05, 37, 34))           # side-stick on 4
    parts = [dict(prog=BASS_AC, ch=1, notes=bass, cc=[(0, 7, 100)]), dict(prog=PIANO, ch=2, notes=piano, cc=[(0, 7, 78)]),
             dict(prog=STR_SLOW, ch=3, notes=pad, cc=[(0, 7, 80), (0, 11, 70)]), dict(prog=BASSOON, ch=4, notes=bassoon, cc=[(0, 7, 96)]),
             dict(prog=0, ch=9, notes=perc, cc=[(0, 7, 70)])]
    return render(parts, "cue_A", reverb=0.45)


def cue_B():  # 12.52-17.92 the door, the torch: half time, thinner
    t0 = 12.52
    bass = [(0, 1.8, D2, 58), (1.9, 1.2, A1, 50), (3.36, 2.0, D2, 46)]
    timp = [(i / 11, .1, D2, int(16 + 26 * min(1, i / 9) * max(0, 1 - i / 17))) for i in range(17)]   # soft roll swell 0-1.5 s
    pad = [(0, 3.36, D2, 30), (0, 3.36, A2, 26), (3.36, 2.0, D2, 26)]
    parts = [dict(prog=BASS_AC, ch=1, notes=bass, cc=[(0, 7, 96)]), dict(prog=TIMP, ch=5, notes=timp, cc=[(0, 7, 80)]),
             dict(prog=STR_SLOW, ch=3, notes=pad, cc=[(0, 7, 80), (0, 11, 64)])]
    return render(parts, "cue_B", reverb=0.6)


def cue_C():  # 17.92-20.52 the yarn: the motif slows and drifts flat, percussion gone
    piano = [(0.18, .3, D4, 42), (0.66, .3, F4, 40), (1.25, .35, E4, 38), (2.0, .5, A3, 34)]
    pad = [(0, 2.6, D2, 28), (0, 2.6, A2, 22)]
    bend = [(i * 0.1, -45 * (i * 0.1 / 2.6) ** 1.4) for i in range(27)]
    parts = [dict(prog=PIANO, ch=2, notes=piano, cc=[(0, 7, 78)], bend=bend),
             dict(prog=STR_SLOW, ch=3, notes=pad, cc=[(0, 7, 80), (0, 11, 60)], bend=[(t, c * .7) for t, c in bend])]
    return render(parts, "cue_C", reverb=0.6)


def cue_R():  # 20.52 rupture: one hit, then a decaying low cluster under the label push-in
    cl = [(0, 3.4, p, 108) for p in (C2, Cs2, Fs2, G2)]
    decay = [(i * 0.1, 11, int(127 - 100 * (i * 0.1 / 3.4) ** 0.6)) for i in range(35)]
    parts = [dict(prog=TIMP, ch=5, notes=[(0, 2.5, D2, 118)], cc=[(0, 7, 110)]),
             dict(prog=STR1, ch=6, notes=cl, cc=[(0, 7, 100)] + decay),
             dict(prog=CONTRA, ch=7, notes=[(0, 2.8, D1, 112)], cc=[(0, 7, 105)] + decay),
             dict(prog=TREM, ch=8, notes=[(0.08, 3.2, A4, 40), (0.08, 3.2, Bb4, 36)], cc=[(0, 7, 70)] + decay)]
    return render(parts, "cue_R", reverb=0.75)


def cue_D_main():  # 24.12-40.36 minimal: pedal, semitone clash, a celesta memory of the motif
    t0 = 24.12
    cello = [(0, 3.9, D2, 40), (3.88, 4.0, D2, 38), (7.9, 4.0, D2, 40), (11.92, 4.4, D2, 44)]
    contra = [(29.17 - t0, 6.9, Eb2, 30), (36.04 - t0, 4.3, Eb2, 36)]
    violin = [(31.28 - t0, 2.4, A5, 22)]
    celesta = [(31.5 - t0, .9, D5, 38), (32.25 - t0, .9, F5, 34), (33.0 - t0, 1.2, E5, 30)]
    swell = [(14.52 + i * 0.1, 11, int(40 + 60 * (i / 17))) for i in range(18)]
    low = [(14.52, 1.8, p, 52) for p in (D2, Eb2, A2)]          # red gallery: the drone thickens (38.64-40.36)
    parts = [dict(prog=CELLO, ch=1, notes=cello, cc=[(0, 7, 96), (0, 11, 80)]), dict(prog=CONTRA, ch=7, notes=contra, cc=[(0, 7, 90)]),
             dict(prog=VIOLIN, ch=8, notes=violin, cc=[(0, 7, 60)]), dict(prog=CELESTA, ch=2, notes=celesta, cc=[(0, 7, 80)]),
             dict(prog=STR_SLOW, ch=6, notes=low, cc=[(0, 7, 90), (0, 11, 40)] + swell)]
    return render(parts, "cue_D_main", reverb=0.7)


def cue_D_box():  # 33.72-36.04 manic hug: the opening motif on a detuned music box, cut mid-phrase at 36.04
    b = 0.34
    fig = [(0, D5), (b, F5), (2 * b, E5), (4 * b, A4), (5 * b, D5), (6 * b, F5), (7 * b, G4 + 12)]
    notes = [(0.1 + t, .3, p, 64) for t, p in fig]
    return render([dict(prog=MUSICBOX, ch=2, notes=notes, cc=[(0, 7, 90)], bend=[(0, -38)])], "cue_D_box", reverb=0.5)


def cue_E():  # 40.36-52.80 losing control: accelerating pulse, tremolo cluster, low brass tritone
    t0, t1 = 40.36, 52.80; t = 0.0; beats = []
    while t0 + t < t1 - 0.05:
        beats.append(t); bpm = 60 + 24 * (t / (t1 - t0)) ** 1.3; t += 60 / bpm
    def ramp(x): return x / (t1 - t0)
    timp = [(b, .5, D2, int(46 + 50 * ramp(b))) for b in beats]
    contra = [(b, .35, D1 if i % 2 == 0 else D2, int(52 + 46 * ramp(b))) for i, b in enumerate(beats)]
    tom = [(b, .1, 41, int(30 + 60 * ramp(b))) for b in beats if b > 2.0]
    trem = [(43.92 - t0, t1 - 43.92, p, 70) for p in (D3, Eb3, A3)]
    trem_cc = [(43.92 - t0 + i * 0.2, 11, int(26 + 90 * (i * 0.2 / (t1 - 43.92)) ** 1.2)) for i in range(int((t1 - 43.92) / 0.2))]
    brass = [(45.72 - t0, t1 - 45.72, Bb1, 66), (45.72 - t0, t1 - 45.72, E2, 62)]
    brass_cc = [(45.72 - t0 + i * 0.2, 11, int(30 + 85 * (i * 0.2 / (t1 - 45.72)))) for i in range(int((t1 - 45.72) / 0.2))]
    high = [(48.72 - t0, t1 - 48.72, A5, 46), (48.72 - t0, t1 - 48.72, Bb5, 42)]
    parts = [dict(prog=TIMP, ch=5, notes=timp, cc=[(0, 7, 100)]), dict(prog=CONTRA, ch=7, notes=contra, cc=[(0, 7, 96)]),
             dict(prog=0, ch=9, notes=tom, cc=[(0, 7, 80)]), dict(prog=TREM, ch=8, notes=trem, cc=[(0, 7, 96)] + trem_cc),
             dict(prog=TUBA, ch=6, notes=brass, cc=[(0, 7, 84)] + brass_cc), dict(prog=TREM, ch=3, notes=high, cc=[(0, 7, 56), (0, 11, 80)])]
    return render(parts, "cue_E", reverb=0.6)


# cue windows: (render fn, timeline start, hard-cut end, gain dB, fade-out s at the cut)
CUES = [(cue_A, 0.00, 10.80, 6.0, 0.12), (cue_B, 12.52, 17.92, 5.0, 0.25), (cue_C, 17.92, 20.52, 9.0, 0.004),
        (cue_R, 20.52, 24.12, -1.0, 0.4), (cue_D_main, 24.12, 40.36, 8.0, 0.3), (cue_D_box, 33.72, 36.04, 0.0, 0.004),
        (cue_E, 40.36, 52.80, 4.0, 0.004)]

def build():
    out = empty(); report = []
    for fn, t0, t1, g, fo in CUES:
        a = fn()[: sec(t1 - t0)]
        a = fade(a, 0.004, fo) * db(g)
        place(out, a, t0); report.append((fn.__name__, t0, t1, round(20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9), 1)))
    return out, report

if __name__ == "__main__":
    m, rep = build(); save(os.path.join(STEMS, "music.wav"), m)
    for r in rep: print(*r)
