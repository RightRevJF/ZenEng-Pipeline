"""Tables from edges_billboard.json, by period. Writes edges_tables.json and prints them."""
import json, collections, statistics as st
d = json.load(open("edges_billboard.json"))
def per(y): return "1958-64" if y < 1965 else "1965-69" if y < 1970 else "1970-74" if y < 1975 else "1975-79" if y < 1980 else "1980-84" if y < 1985 else "1985-91"
G = collections.defaultdict(list)
for x in d: G[per(x["year"])].append(x); G["all"].append(x)
def q(v):
    v = sorted(v); n = len(v)
    if not n: return None
    return [round(v[int(.25 * (n - 1))], 1), round(st.median(v), 1), round(v[int(.75 * (n - 1))], 1)]
def sh(xs, f): return round(100 * sum(1 for x in xs if f(x)) / max(len(xs), 1))
T = {}
for g in ["1958-64", "1965-69", "1970-74", "1975-79", "1980-84", "1985-91", "all"]:
    xs = G[g]; fa = [x for x in xs if x["fade"]]; nf = [x for x in xs if not x["fade"]]
    it = [x for x in xs if x["intro"]]
    last = collections.Counter((tuple(x["last2"]) if len(x["last2"]) == 2 else ()) for x in nf)
    T[g] = dict(songs=len(xs), length=q([x["length"] for x in xs]),
        intro_share=sh(xs, lambda x: x["intro"]), intro_s=q([x["intro_s"] for x in it]), intro_bars=q([x["intro_bars"] for x in it if x["intro_bars"]]),
        voice_s=q([x["voice_s"] for x in xs if x["voice_s"] is not None]), voice_in_intro=sh(it, lambda x: x["voice_in_intro"]),
        intro_material={k: sh(it, lambda x, k=k: x["intro_material"] == k) for k in ("its own", "verse", "chorus", "outro or other")},
        intro_lead={k: v for k, v in collections.Counter(x["intro_lead"] or "none marked" for x in it).most_common(5)},
        fade=sh(xs, lambda x: x["fade"]), outro_s_fade=q([x["outro_s"] for x in fa if x["outro_s"]]), outro_s_cold=q([x["outro_s"] for x in nf if x["outro_s"]]),
        cold_last_section={k: sh(nf, lambda x, k=k: x["last_section"] == k) for k in ("outro", "coda", "chorus", "verse", "interlude", "intro")},
        cold_has_outro=sh(nf, lambda x: x["outro_s"] > 0), fade_outro_bars=q([x["outro_bars"] for x in fa if x["outro_bars"]]), cold_outro_bars=q([x["outro_bars"] for x in nf if x["outro_bars"]]),
        cold_last_I=sh(nf, lambda x: x["last2"] and x["last2"][-1] in ("I", "i")),
        cold_V_I=sh(nf, lambda x: tuple(x["last2"]) in (("V", "I"), ("V", "i"))), cold_IV_I=sh(nf, lambda x: tuple(x["last2"]) in (("IV", "I"), ("iv", "I"), ("iv", "i"), ("IV", "i"))),
        cold_bVII_I=sh(nf, lambda x: tuple(x["last2"]) in (("bVII", "I"), ("bVII", "i"))), cold_bVI_I=sh(nf, lambda x: tuple(x["last2"])[:1] in (("bVI",),) and x["last2"][-1] in ("I", "i")),
        bookend=sh(it, lambda x: x["bookend"]))
json.dump(T, open("edges_tables.json", "w"), indent=1)
for g, t in T.items(): print(g, json.dumps(t))
