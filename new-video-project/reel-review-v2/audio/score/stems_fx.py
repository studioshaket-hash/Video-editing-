"""AMBIENCE and FOLEY stems. Restraint: a handful of placements only, each with a cause on screen.
Levels are relative (dBFS before mastering); the master stage sets the final loudness."""
from lib import *

MEDIA = os.path.join(ROOT, "assets", "media"); FOLEY = os.path.join(SRC, "foley"); DER = os.path.join(SRC, "derived")
def f(name, a=0.0, d=None): return load(os.path.join(FOLEY, name + ".wav"), a, d)
def g(name): return load(os.path.join(DER, name + ".wav"))
CUT = 52.80          # music, ambience and Foley stop dead on the first frame of the stare


def ambience():
    out = empty()
    # production room tone (P1060602 silence) from the door opening to the stare, very low
    rt = load(os.path.join(MEDIA, "roomtone.wav"), 0, CUT - 12.52)
    place(out, fade(rt, 0.6, 0.004) * db(-14), 12.52)
    # unnatural low texture under the yarn and the label (derived)
    place(out, fade(g("low_texture")[: sec(24.12 - 18.10)], 1.4, 0.8) * db(-26), 18.10)
    # one sub drop on the label cut (derived), no library stinger
    place(out, g("sub_drop") * db(-18), 20.52)
    # red gallery: fluorescent hum (CC0), flickers once with the handheld move
    hum = f("red_hum", 1.2, 40.36 - 38.64)
    flick = np.ones(len(hum), np.float32); i = sec(0.55); flick[i:i + sec(0.12)] = 0.35
    place(out, fade(hum * flick[:, None], 0.08, 0.15) * db(-22), 38.64)
    out[sec(CUT):] = 0
    return out


def foley():
    out = empty()
    # the yarn emerging from the carton (CC0 rope/drape handling, slowed and softened)
    yarn = ffx(f("yarn_drape", 0.2, 2.6), "asetrate=48000*0.82,aresample=48000,highpass=f=250,lowpass=f=5500")
    place(out, fade(yarn, 0.15, 0.5) * db(-16), 18.45)
    place(out, fade(ffx(f("fibre_brush", 2.2, 1.6), "highpass=f=500,lowpass=f=7000"), 0.3, 0.6) * db(-24), 19.10)
    # rugs awaken: fingers in the pile (24.3), the pile under his face (29.2), one squeeze in the hug (33.8)
    rub = ffx(f("rug_friction", 1.2, 1.5), "volume=26dB,highpass=f=200,lowpass=f=6000")
    place(out, fade(rub, 0.2, 0.5) * db(-10), 24.30)
    place(out, fade(ffx(f("fibre_brush", 10.2, 0.8), "highpass=f=400,lowpass=f=6000"), 0.15, 0.35) * db(-22), 29.20)
    place(out, fade(ffx(f("fibre_brush", 11.0, 1.2), "highpass=f=300,lowpass=f=5000"), 0.1, 0.5) * db(-20), 33.80)
    # whisper-like textures from the fabric (derived, unintelligible), only between spoken lines
    place(out, g("whisper_a") * db(-31), 28.62)
    place(out, g("whisper_b") * db(-29), 31.42)
    place(out, g("whisper_c") * db(-36), 36.30)
    # losing control: processed tufting-gun pulses (derived) and one burst on the fibres hitting the lens
    place(out, g("gun_pulses") * db(-20), 40.36)
    place(out, g("gun_burst") * db(-14), 49.12)
    out[sec(CUT):] = 0
    # the stare: one nearly imperceptible fibre creak (CC0)
    creak = ffx(f("tension_creak", 3.40, 0.55), "highpass=f=300,lowpass=f=4000")
    place(out, fade(creak, 0.08, 0.25) * db(-46), 57.50)
    out[sec(STORY_END):] = 0
    return out


if __name__ == "__main__":
    a = ambience(); save(os.path.join(STEMS, "ambience.wav"), a)
    fo = foley(); save(os.path.join(STEMS, "foley.wav"), fo)
    print("ambience/foley stems written")
