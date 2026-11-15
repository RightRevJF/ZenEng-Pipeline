"""Kept 3/4 tables for song 53 (749.4: the metre as a parameter), from the Essen folk-song collection (music21's corpus), with the same
builder as song 52's 6/8 tables (tables_68.build): bar = 36 twelfths, beats at 0, 12, 24. Writes tables/essen_34.json. Run once."""
import sys, json
sys.path.insert(0, "/home/claude/p62")
import tables_68 as T
if __name__ == "__main__":
    out = T.build("3/4", 36, 12)
    json.dump(out, open("/home/claude/p63/tables/essen_34.json", "w"))
    print(out["tunes"], "tunes"); print({a: [round(x, 3) for x in b] for a, b in out["readings_quartiles"].items()})
    print("top bars", out["bar_rhythms"][:10])
