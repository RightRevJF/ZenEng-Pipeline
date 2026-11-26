# Judging research, run 06: the maintainer's check

26 November 2026. The report and its proposed fix list (R06-1 to R06-5), read whole; the run's files on the judging-research branch at 06af481.

## Sources

| Cited | Checked | Found |
|---|---|---|
| March (2024), Helmholtz-Hodge Decomposition on Graphs, arXiv 2412.09434 | abstract page | Exists; Peter March; 12 Dec 2024; math.DG and math.CO. It does what the report says (a curl on graphs, a Helmholtz-Hodge split). The report said the class was "probably math.CO, not confirmed": it is math.DG first. |
| Homs-Dones, MacKay, Sansom and Zhou (2025), Circular Directional Flow Decomposition of Networks, arXiv 2506.12546 | abstract page | Exists; the four authors as given; 14 June 2025. A split into a circular and a one-way part; the abstract says it is generally not unique, as the report says. |
| Kantarelis et al. (2024), Chordonomicon, arXiv 2410.22046 | abstract and dataset card | Exists; over 666,000 songs; CC BY-NC 4.0; the card names genre, release date, structure and Spotify ids, and no artist or title. As the report says. |

Nothing invented. I did not read the two mathematics papers through; I checked that they are what they are said to be.

## The mathematics

**The "battery theorem" is right, and I can say why without the papers.** A song's chord walk enters every chord as often as it leaves it, except that it leaves the first once more and enters the last once more. So the net flow has no sources or sinks but those two. The gradient part of a Hodge split is fixed by the flow's sources and sinks alone. So it is the same for every walk with the same first and last chord over the same edges: the unit current between them. It reads where the excerpt was cut and nothing of the harmony between. The run was right to stop it before any outcome was joined.

**Chirality** is a fair measure (signed area on the circle of fifths belongs to the loops; a move and its return cancel). Unsettled is the right verdict: one half of the artists carries it, and the unsigned size leans the same way, so "which way" is not shown.

## The fresh songs

The table (`fresh_songs_discogs_run06.json`): 1,946 songs, 312 matched, 294 taken up by another artist, as reported. Against my own clique table (made 22 November, independently of the research's rebuild): all 312 matched cliques agree on artist and title; none of the 1,634 unmatched would match by exact title and artist. The sha256 of `Hooktheory.json.gz` on my machine is the research's. I did not rerun their six tests.

The order holds on the branch: predictions 08b5167 (03:16), results 3f39f56 (03:28).

## The proposed list

- **R06-1: done here.** The table is in the data pack as `hooktheory_fresh_covers_discogs.json`, marked seen; the README has the seen ledger (three lines), the raw files' addresses and the checksum, and the note that the old covers file already holds 222 fresh videos.
- **R06-2: agreed, and it is what the engine's side had come to.** 749.185 (the loop gate with a chance) is to be judged on the kept songs' rate alone. The two cover margins lean opposite ways and neither is settled; the fresh songs cannot settle them (a standard error of 1.04 against an effect of about 1). Noted in `lib/luthier/README.md`.
- **R06-3: recorded.** Nothing for the engine.
- **R06-4: not possible from here either.** The dataset's file redirects to a storage host my machine is also refused (us.aws.cdn.hf.co). And it names songs by Spotify id only; turning those into artist and title needs Spotify's own service, which I have no key for and whose terms I would want read before any of it was stored. Two blocks, both the writer's to lift if he wants it: allow the host, and decide about Spotify.
- **R06-5: I would say yes.** Five tests with power of 0.014 to 0.047 cost the one test that could have seen something most of its power, and their "kills" fire half the time on nothing. A floor of 0.2, with power reckoned from fake outcomes before the real ones are joined (as the run does), is sound. The under-powered ones are still worth freezing and reporting as estimates. The same floor is right for my own readings with several marks. The writer rules.
- **R02-3 (carried): mended here.** `studies/covers/study_covers_discogs.py` set `original = 1.0` for every song. It now reads the clique's earliest versions: of the 2,769 songs in that study, the Hooktheory artist is among the first performers in 2,066 and is **not** in 703. A quarter of the "originals" the covers studies measured are themselves covers. No published figure used the flag (it was only a filter nobody had passed), but it bears on R04-2.
- **R04-2 (carried): open.** Cover counts by other artists only, and 749.157 read again. With R02-3 mended it can be done properly: among first performers only. Not done today.

## What it gives the engine's work

Nothing to build. One thing to keep: the report's own first principle, that the measures have outrun the outcomes. The engine's side has the opposite luck. Its outcomes are the kept songs themselves, 160 of them read note by note, and this week's findings (the octave bin, the tie to the chord, the draw sitting on its centre) each came from setting the engine's notes beside theirs, with no popularity figure at all.
