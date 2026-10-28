"""Point the V2 HyperFrames project at the soundtrack stems: shot videos become muted (their audio lives in the
dialogue stem, placed sample-identically), V1's two beds are replaced by four stem tracks.
Run after build/build.py whenever the picture project is regenerated. The delivered MP4 is the mastered mux
(build_all.sh); this composition is the editable/auditionable version of the same mix (same stems, +5.8 dB master gain,
no limiter)."""
import os, re, shutil
from lib import ROOT, STEMS, TOTAL, STORY_END

idx = os.path.join(ROOT, "index.html"); html = open(idx).read()
html = re.sub(r'data-has-audio="true" data-volume="[0-9.]+" data-fade-in="[0-9.]+" data-fade-out="[0-9.]+"', "muted", html)
html = re.sub(r'\n[ \t]*<!-- sound design:[^\n]*-->', '', html)
html = re.sub(r'\n[ \t]*<audio\b[^>]*\bid="(roomtone|lowbed)"[^>]*>\s*</audio>', '', html)   # any attribute order
dst = os.path.join(ROOT, "assets", "stems"); os.makedirs(dst, exist_ok=True)
tracks = []
for i, (k, f) in enumerate([("dialogue", "dialogue.wav"), ("ambience", "ambience_ducked.wav"), ("foley", "foley_ducked.wav"), ("music", "music_ducked.wav")]):
    shutil.copyfile(os.path.join(STEMS, f), os.path.join(dst, f"{k}.wav"))
    tracks.append(f'      <audio id="stem-{k}" class="clip" src="assets/stems/{k}.wav" data-start="0" data-duration="{STORY_END:.2f}" data-track-index="{5 + i}" data-volume="1.95"></audio>')
block = "\n      <!-- REVIEW V2 soundtrack stems (audio/score/*.py): dialogue = production audio, ambience, foley, music (ducked) -->\n" + "\n".join(tracks) + "\n"
html = html.replace("\n      <!-- captions:", block + "\n      <!-- captions:", 1)
open(idx, "w").write(html)
print("index.html now uses", len(tracks), "stem tracks;", html.count(" muted "), "muted shot videos")
