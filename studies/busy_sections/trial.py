"""749.138, first step: 40 quick tunes a song, as lyric_room draws them, under LUTHIER_VERSE_CLOSER unset / kept / all. See PREDICTION.md.
   LUTHIER_VERSE_CLOSER=kept python3 studies/busy_sections/trial.py -> trial_<form>.json"""
import sys, os, json, random, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas"), os.path.join(ROOT, "studies", "soundness")]
import song_from_lyric as SL, metre_engine as M, lyric_room as LR, word_weight as WW
form = os.environ.get("LUTHIER_VERSE_CLOSER") or "as built"; out = {}
class Got(Exception): pass
for tag, f in (("55", "songs/p65/lyric55.json"), ("54", "songs/p64/lyric54.json"), ("58", "songs/p68/lyric58.json"), ("59", "songs/p69/lyric59.json")):
    cap = {}
    def capture(self, N, seed):
        rng = random.Random(f"room {seed}"); rows = []; fits = []; rat = []; tries = 0
        while len(rows) < 40 and tries < 480:
            c, err = self.build(rng); tries += 1
            if err or self.gates(c): continue
            sung = self.as_sung(c["notes"])
            def dens_(part):
                b_ = {}
                for n in sung:
                    if self.KIND.get(n["sec"]) == part: b_[n["on"] // self.BAR] = b_.get(n["on"] // self.BAR, 0) + 1
                return sum(b_.values()) / max(1, len(b_))
            rat.append(dens_("Verse") / dens_("Chorus")); rows.append(LR.read([n["on"] for n in sung], self.BAR)); fits.append(WW.fit([x for x in sung if x.get("melisma") != "second"], self.BAR, self.BEAT, parts=True)["all"])
        cap.update(rat=rat, rows=rows, fits=fits, tries=tries, form=self.S["form"], slots=self.S["slots"]); raise Got()
    old = M.Engine.run; M.Engine.run = capture
    try: SL.write(json.load(open(os.path.join(ROOT, f))), 1000, 12)
    except Got: pass
    finally: M.Engine.run = old
    L = json.load(open(os.path.join(ROOT, f))); bars = sum(len(b) for _, b in cap["form"]); md = lambda c: round(float(np.nanmedian([r[c] for r in cap["rows"]])), 3)
    out[tag] = dict(tunes=len(cap["rows"]), tries=cap["tries"], live_share=round(len(cap["rows"]) / cap["tries"], 3), bars=bars, seconds=round(bars * 4 * 60.0 / L["bpm"]), form=[n for n, _ in cap["form"]], verse_slots=next(v for k, v in cap["slots"].items() if k.lower().startswith("verse")),
                    verse_over_chorus=round(float(np.median(cap['rat'])), 2) if cap['rat'] else None, room=md("room"), contrast=md("contrast"), rhythm_scaling=md("rhythm_scaling"), words_fit=round(float(np.median(cap["fits"])), 3) if cap["fits"] else None)
    print(form, tag, out[tag], flush=True)
json.dump(out, open(os.path.join(HERE, "trial_" + form.replace(" ", "_") + ".json"), "w"), indent=1)
