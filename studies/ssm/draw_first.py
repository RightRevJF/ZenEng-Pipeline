"""The first pictures: nine songs as squares of themselves (bars against bars). Row 1 songs that lasted, row 2 songs that charted low,
row 3 Luthier's own. python3 draw_first.py -> ssm_first.png"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import ssm_lib as L
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
C = "/home/claude/data/cocopops/CoCoPops"; P = "/home/claude/zeneng-pipeline/songs"
rows = [("Songs that lasted", [("RollingStone/Data/BenEKing_StandByMe_1961.hum", "Rolling Stone 500, no. 121"), ("RollingStone/Data/ArethaFranklin_Respect_1967.hum", "Rolling Stone 500, no. 5"), ("Billboard/Data/OtisRedding_TheDockOfTheBay_1968.varms.hum", "Billboard no. 1")]),
        ("Songs that charted low", [("Billboard/Data/JohnDenver_SeasonsOfTheHeart_1982.varms.hum", "Billboard peak 78"), ("Billboard/Data/TheRembrandts_Someone_1991.varms.hum", "Billboard peak 78"), ("Billboard/Data/TheKendalls_HeavensJustASinAway_1977.varms.hum", "Billboard peak 69")]),
        ("Luthier's songs", [(P + "/p68/lyric58.song.json", "song 58"), (P + "/p65/lyric55.song.json", "song 55"), (P + "/p64/lyric54.song.json", "song 54")])]
fig, ax = plt.subplots(3, 3, figsize=(11, 11.6), facecolor="white")
for r, (label, songs) in enumerate(rows):
    for c, (f, note) in enumerate(songs):
        s = L.read_record(f) if f.endswith(".json") else L.read_hum(os.path.join(C, f)); M = L.ssm(s); a = ax[r][c]
        a.imshow(M, cmap="Blues", vmin=0, vmax=1, interpolation="nearest", origin="upper")
        a.set_title(f"{s['title'][:34]}\n{note}, {len(M)} bars", fontsize=9.5, color="#222", pad=5); a.set_xticks([]); a.set_yticks([])
        for sp in a.spines.values(): sp.set_color("#bbb")
    fig.text(0.015, 0.83 - r * 0.315, label, rotation=90, fontsize=12, color="#333", va="center")
fig.suptitle("Each song as a picture of itself: every bar against every other bar (dark = alike in tune and chords)", fontsize=12, color="#222", y=0.985)
plt.tight_layout(rect=(0.03, 0, 1, 0.965)); plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ssm_first.png"), dpi=110)
