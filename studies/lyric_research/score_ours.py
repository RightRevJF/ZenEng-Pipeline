"""Score our own lyrics on the frozen measures and place each against the
Billboard hits (percentiles). Hold-outs (songs 59, 50, 63 = p69, p60, p73)
are never read.
"""
import glob, os, re, sys, json, pickle
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import measures as M

SONGS = "/home/claude/zeneng-pipeline/songs"
HOLD = {"p69", "p60", "p73"}
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ours.json")
SHOW = ["image_noun_rate", "conc_noun", "stock_rate", "zipf_content", "emo_rate",
        "poetic_stock_rate", "you_rate", "verb_share"]


def pick(d):
    for pat in ("lyric_locked.md", "lyric_locked.txt"):
        f = os.path.join(d, pat)
        if os.path.exists(f):
            return f
    drafts = sorted(glob.glob(os.path.join(d, "lyric_draft*.md")) + glob.glob(os.path.join(d, "lyric_draft*.txt")),
                    key=lambda p: [int(x) for x in re.findall(r"\d+", os.path.basename(p))] or [0])
    drafts = [p for p in drafts if "unshown" not in p]
    return drafts[-1] if drafts else None


def clean(t):
    keep = []
    for line in t.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", "[", "(", "|", "-", "*", ">", "Words and music")) or s.endswith(":"):
            continue
        if re.match(r"^(verse|chorus|refrain|bridge|pre-?chorus|intro|outro|tag|coda)\b", s, re.I):
            continue
        keep.append(s)
    return "\n".join(keep)


def main():
    base = pd.read_csv("/home/claude/lyr_dl/feat.csv").dropna(subset=SHOW)
    table = pickle.load(open("/home/claude/lyr_dl/stock_table.pkl", "rb"))
    rows = []
    for d in sorted(glob.glob(os.path.join(SONGS, "p*"))):
        name = os.path.basename(d)
        if name in HOLD:
            continue
        f = pick(d)
        if not f:
            continue
        ft = M.features(clean(open(f, encoding="utf-8").read()), table, "zeneng")
        if ft.get("n_words", 0) < 60:
            continue
        r = {"folder": name, "song": int(name[1:]) - 10, "file": os.path.basename(f), "n_words": ft["n_words"]}
        for m in SHOW:
            r[m] = round(ft[m], 4)
            r[m + "_pct"] = round(float((base[m] < ft[m]).mean() * 100), 1)
        rows.append(r)
    acc = base[base.rs == 1]; oth = base[base.rs == 0]
    ref = {m: {"acclaimed_median": float(acc[m].median()), "other_median": float(oth[m].median())} for m in SHOW}
    json.dump({"songs": rows, "reference": ref}, open(OUT, "w"), indent=1)
    df = pd.DataFrame(rows)
    print(df[["song"] + [m + "_pct" for m in SHOW]].to_string(index=False))
    print("median percentile:", {m: float(df[m + "_pct"].median()) for m in SHOW})


if __name__ == "__main__":
    main()
