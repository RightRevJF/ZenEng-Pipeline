# Run 12: data used and data waiting (chair, 28 Nov 2026)

## Used this pass (notes side; the builders are deterministic and read no outcome)

| What | File | Builder | Notes |
|---|---|---|---|
| Lakh measures, 5,865 songs (6,036 kept files; 81 near-duplicate files dropped in 77 songs) | `/home/claude/dl/run12/lakh_measures12.json` (sha256 ef993e6d20b4b584…) | `run12/experiments/build_lakh12.py` (Pool(2), 65 s) | Rebuilt once into scratch: the `songs` block was identical. Only `meta.seconds` differs between builds. |
| Hooktheory clip measures (G_E5, G_REST, PIC, …), 9,588 songs | `/home/claude/dl/run12/hook_measures12.json` (f73e6a746d0260a8…) | `run12/experiments/build_hook12.py` (52 s) | m_geometer and m_listener, as committed by the imaginers |
| Run 11's frozen cache (REP = pc_entropy, the 13 baselines) | `/home/claude/dl/run11/measures_run11.json` (d6d445329221ccf9…) | run 11's `build_cache11.py` | not rebuilt |
| Lakh notes-side list | `/home/claude/dl/run12/lakh_notes_side.json` (4be5629045b4df93…) | orchestrator | outcome keys removed |
| Outcome-side variance shares (no notes) | `/home/claude/dl/run12/outcome_side_shares.json` (22853347fbdfa50a…) | orchestrator | used only for the fake outcomes |
| Fitness model aggregates (r, A, g, h) | `run12/experiments/fitness/fit.json` | frozen `fitness.py` | no per-song value read |

The outcomes are read only by the guarded loaders in `common12.py`, at run time: `C5.load_outcomes`, `/home/claude/dl/run12/fitness.json` and `data/lakh_songs_discogs_run07.json`.

## Waiting: WINDOWS pooled with Lakh (next pass)
Discogs-VI `main.zip` finished downloading at 10:55 ET (`/home/claude/dl/discogs/dl.log` says DONE; 1.41 GB). It holds `Discogs-VI-20240701.jsonl` (7.9 GB uncompressed) and its YouTube-matched variants. I did **not** reduce it this pass, for three reasons:
1. **The link is an outcome.** The link from a Lakh song to its Discogs-VI clique lives only in the outcome file `data/lakh_songs_discogs_run07.json` (`clique`, an outcome key). A chair-side reduction "for Lakh cliques" would open that link.
2. **Pooling needs rules of its own.** It needs rules frozen beforehand: one measure across two sources (REP on clips against REP_L on the skyline), songs present in both sets, and t0 for Lakh cliques taken from the versions.
3. **Power is borderline even pooled.** Even pooled, the power of Δ would be about 0.1 to 0.2.

**Plan for the next pass, in order:**
1. **Reduce the versions without opening the link.** The orchestrator, or a guarded script, streams `main.zip` → `Discogs-VI-20240701.jsonl` and writes `/home/claude/dl/discogs/versions_all.json.gz` (per clique: the version list of performer sets with their years). This step reads versions only and links nothing to any song.
2. **Write and freeze the pooled design.** A chair writes `windows_pooled/` with:
   - the Lakh cover rule (own sets matched on the normalised Lakh artist, otherwise fitness.py's rule);
   - t0 = the clique's first version year;
   - the frozen g and h;
   - a dataset fixed effect;
   - z-scores within dataset;
   - songs in both sets counted once, taking the Hooktheory row.
3. **Compute power and decide.** Power comes from model-based fake counts on both row sets, before the join, with the same machinery as `harness12.power_windows`.

## Missing data (unchanged)
The performer's field (P11-3) needs recordings aligned to notes, and none are on this machine.

## Addendum (orchestrator, after the results)
- The Lakh windows test was run this pass after seeing results (`experiments/windows_lakh_after`, rule 2d64143 committed before the join): it streamed the full `Discogs-VI-20240701.jsonl` member for the 2,162 Lakh cliques, inside the guarded test. The pooled design above stays for a later pass, now with Lakh cover timing seen.
- **Data request (R12-3):** recordings aligned to notes for the performer's field (physics vector 3). Not on this machine; no allowed source found.
- **Still missing (R11-3):** new named melodies by artists with two or more songs, never joined to an outcome.
