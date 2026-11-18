"""Luthier v9, fix 763: a line's slot from its syllables and the tempo, in seconds (Part 21; studies/metre/metre_results.json,
9,313 lines of 198 Billboard songs). The form is no longer typed bar by bar before the words are known: the engine proposes each
line's slot, and a line given less than three-quarters of the kept slot is flagged.

    from slots import propose
    propose([8, 9, 10, 6], bpm=120)            # -> a dict per line: kept seconds, bars at this tempo, whole bars proposed
    python3 lib/luthier/slots.py 120 8 9 10 6 [given bars ...]

Kept median slots (first onset of a line to the next line's first), seconds, by the bar's length and the line's syllables."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
_M = json.load(open(os.path.join(HERE, "..", "..", "studies", "metre", "metre_results.json")))["by_tempo"]
_BANDS = [(k, v) for k, v in _M.items()]
def _tempo_band(bar_s): return next(v for k, v in _BANDS if k.startswith("fast")) if bar_s < 1.8 else next(v for k, v in _BANDS if k.startswith("slow")) if bar_s >= 2.6 else next(v for k, v in _BANDS if k.startswith("middle"))
def _syl_band(n): return "3-5 syl" if n <= 5 else "6-8 syl" if n <= 8 else "9+ syl"
def propose(syllables, bpm, beats_per_bar=4, given=None):
    bar_s = 60.0 / bpm * beats_per_bar; T = _tempo_band(bar_s); out = []
    for k, n in enumerate(syllables):
        b = T[_syl_band(n)]; sec = b["median_slot_seconds"]; bars = sec / bar_s; whole = max(1, int(bars + 0.5))
        row = {"syllables": n, "kept median slot, seconds": sec, "bars at this tempo": round(bars, 2), "whole bars proposed": whole, "kept share in one bar or less": b["one_bar_or_less"]}
        if given is not None:
            row["bars given"] = given[k]; row["flag"] = "under three-quarters of the kept slot" if given[k] < 0.75 * bars else ""
        out.append(row)
    return out
if __name__ == "__main__":
    bpm = float(sys.argv[1]); nums = [int(x) for x in sys.argv[2:]]
    for r in propose(nums, bpm): print(r)
