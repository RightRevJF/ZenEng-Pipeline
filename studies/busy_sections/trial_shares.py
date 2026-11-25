"""The trial of 749.153: every living build of a song under one form of the verse sung closer. See PREDICTION_shares.md.
    LUTHIER_VERSE_CLOSER=off|apart|shares python3 studies/busy_sections/trial_shares.py songs/pNN/lyricNN.json out.json
Per song: builds that live of 1,000; the builds' middle rhythm scaling, words' fit and range; the verse over the chorus in notes a sung bar; and each line's mean words' fit over the builds (749.154)."""
import sys, os, json, random, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", "..")); sys.path[:0] = [os.path.join(ROOT, "lib", "luthier"), os.path.join(ROOT, "tables", "metre_atlas")]
import song_from_lyric as SL, metre_engine as M, lyric_room as LR, word_weight as WW
class Got(Exception): pass
cap = {}
def capture(self, N, seed):
    rng = random.Random(seed); rs = []; fit = []; rg = []; rat = []; room = []; lines = collections.defaultdict(list); made = 0
    for k in range(N):
        c, err = self.build(rng); made += 1
        if err or self.gates(c): continue
        sung = self.as_sung(c["notes"]); syl = [x for x in sung if x.get("melisma") != "second"]; rd = LR.read([n["on"] for n in sung], self.BAR)
        rs.append(rd["rhythm_scaling"]); room.append(rd["room"]); fit.append(WW.fit(syl, self.BAR, self.BEAT, parts=True)["all"]); rg.append(self.readings(c["notes"])["range"])
        def dens(part):
            b = {}
            for n in sung:
                if self.KIND.get(n["sec"]) == part: b[n["on"] // self.BAR] = b.get(n["on"] // self.BAR, 0) + 1
            return sum(b.values()) / max(1, len(b))
        rat.append(dens("Verse") / dens("Chorus")); G = collections.OrderedDict()
        for n in syl: G.setdefault(f"{n['sec']}:{n['line'] + 1}", []).append(n)
        for key, g in G.items(): lines[key].append(WW.fit(g))
    cap.update(made=made, live=len(rs), rhythm_scaling=round(float(np.nanmedian(rs)), 3), bars_unsung=round(float(np.median(room)), 3), words_fit=round(float(np.median(fit)), 3), range=float(np.median(rg)), verse_over_chorus=round(float(np.median(rat)), 2),
               line_fit={k: round(float(np.nanmean(v)), 4) for k, v in lines.items()}, kinds=dict(self.KIND), closer=(self.S.get("verse_closer") or {}).get("lines_given_one_bar"),
               floor=((self.S.get("target") or {}).get("choose_range") or {}).get("floor"), bars=sum(len(b) for _, b in self.S["form"]))
    raise Got()
M.Engine.run = capture
L = json.load(open(sys.argv[1]))
try: SL.write(L, 1000, 12)
except Got: pass
cap.update(form=os.environ.get("LUTHIER_VERSE_CLOSER", "off"), song=os.path.basename(sys.argv[1]), seconds=round(cap["bars"] * 240 / L["bpm"]))
json.dump(cap, open(sys.argv[2], "w"), indent=1); print({k: v for k, v in cap.items() if k not in ("line_fit", "kinds")})
