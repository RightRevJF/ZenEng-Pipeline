# Card 2: Discogs-VI (what a "clique" is, and what being in one means)

## 1. Citation and copy read
Araz, R. O., Serra, X., & Bogdanov, D. (2024). Discogs-VI: A Musical Version Identification Dataset Based on Public Editorial Metadata. Proc. ISMIR 2024. arXiv:2410.17400v1 (submitted 22 Oct 2024).

Copy read: the arXiv PDF (v1), whole paper including the reference list. It has no appendix or supplement. The arXiv abstract page was also read. These pages were blocked by unanswered permission prompts and were NOT read: the arXiv HTML page, the Zenodo record 13983028, the dataset page (mtg.github.io/discogs-vi-dataset) and the model repo (github.com/raraz15/Discogs-VINet). So nothing here comes from the README or from later dataset releases. If the Zenodo record is a later dump, its counts may differ from the ones below.

## 2. Claim and data (how the dataset is built)
The paper's aim is a large training and test set for audio version identification ("cover song" detection). Clique quality is a means to that end, not a subject of study.

1. **Source.** The July 2024 Discogs monthly dump, which is public domain. Discogs is a crowd-edited database of releases.
2. **Fields per track.** Title, track artists, featured artists, release artists, and writer credits at track and release level ("Written-By"). Writer sets are widened with group members, aliases and name variations. Genre, style, label, format, release date, master release and country are also collected.
3. **Title normalisation.** Removes diacritics, leading articles and anything in parentheses, turns "&" into "and", and strips punctuation.
4. **Clique rule.** Tracks are first grouped by exact normalised title. Each group is then split so that tracks sharing at least one writer go together. No route through master releases or Discogs "versions" pages is described. A track with no writer credit has nothing to join on (the paper does not say this outright). The authors call the shared-writer test sufficient but not necessary, and chose it because writer credits are inconsistent across releases.
5. **Version rule.** Inside a clique, all tracks by the same performer set (track artists, or release artists if those are missing, plus featured artists) count as ONE version. Reissues in other years or countries collapse into it. Live takes, remixes and radio edits are included, but by the same performer they would merge into that performer's one version. A different featured-artist set makes a separate "version".
6. **Minimum size. Cliques with only one version are discarded.** Every clique therefore has at least two distinct performer sets.
7. **Counts.** Discogs-VI has 348,796 cliques and 1,911,611 versions. Clique size: maximum 1,837, mean 6, median 2. There are 239,949 distinct artists. The paper gives no raw track count and no count of tracks lacking writer credits.
8. **Discogs-VI-YT.** Each version was searched on YouTube from Barcelona between March 2023 and July 2024. A hit had to be official, in the Music category, at most 20 minutes long, and an exact title match after stripping remaster and lyric tags. 34% of versions matched and 33% were downloaded. Cliques were then cut to those with at least two downloaded versions. That leaves 98,785 cliques and 493,049 versions (mean 5, median 2), with 13 genres and 512 styles. Duplicate URLs (under 8% of versions) were resolved by hand.
9. **Overlap and splits.** The cliques contain 93% of the Da-TACOS benchmark cliques and 90% of SHS100K-Test cliques. The splits are train 80,017, validation 8,890 and test 9,878 cliques.

## 3. Is the measure from the notes?
No. This is the outcome side. Clique membership records that, in Discogs' credits, a title with a shared writer was released by two or more different performer sets. It measures documented re-recording on catalogued releases. It does not measure popularity, streams or the quality of the notes.

## 4. Effect size / how checked
The paper reports no audit of clique precision or recall and no error rate. "High precision" is asserted for the YouTube matching without a figure. The only checks are recovery rates of 93% for Da-TACOS and 90% for SHS100K-Test cliques. The authors admit three problems:
- splits from title variants (e.g. "Moon Over Naples" vs "Spanish Eyes");
- weak rule-based text matching across languages;
- ambiguous credits that create duplicate versions.

A baseline model reached MAP 0.443 on the Discogs-VI-YT test set, 0.607 on Da-TACOS and 0.660 on SHS100K-Test. These figures say nothing about metadata error.

## 5. Lasting love and covers
**Ways a real, often-covered song can FAIL to be in a clique (or fail our match):**
- The cover's title differs: a translation, a retitle, a medley, or a subtitle outside parentheses.
- Missing or inconsistent writer credits, common on older, budget, digital-only or non-Western releases.
- The writer is spelled as a different Discogs entity that alias linking misses.
- Covers that exist only live, on YouTube, on TikTok or in film are absent; Discogs is release-centric.
- Our own matching: the Hooktheory title or artist normalises differently from Discogs, or the Hooktheory "artist" is not among the clique's performers (a soundtrack credit, game composer, or band vs solo name).
- Recent songs have had less time to be covered. Dump cut-off is July 2024.
- Thin Discogs coverage for some regions or genres; anime, game and K-pop material is plausibly under-credited (my inference, not tested in the paper).

**Ways a never-covered song can still be IN a clique:**
- A featured-artist variant, or a solo-vs-group credit, counts as a second performer set.
- The same performer under an alias or name variant may count as a different "artist".
- Compilations and DJ mixes credit someone else as the release artist.
- Remixes credited to the remixer.
- A different song with the same title and a shared prolific writer (generic titles like "Home" are risky).
- Credit noise that creates duplicates, which the paper acknowledges.

**Judgement:** Being in a clique is a reasonable but noisy, high-threshold proxy for "versioned by someone on a catalogued release". By construction it requires at least two performer sets, which fits the 98% figure. The roughly 2% without a cover are probably variants of the same performer. Non-matches mix "never covered" with "not credited or matched", so they are not true negatives. A within-artist test must hold fixed or model:
- release year, i.e. time at risk;
- genre and source type (anime, game, pop, rock);
- region or language;
- writer-credit availability (e.g. whether the original has any Written-By entry on Discogs);
- title genericness and normalisation success;
- number of Hooktheory clips or sections, as a fame proxy;
- whether the artist is a writer-performer or performs other people's songs.

## 6. Methods and measures for tonight
- **Two outcomes.** Use matched (0/1) and, among matched songs, the count of distinct performer sets minus the original's own. Collapse aliases and group members before counting, and report a version with "feat." variants removed.
- **Covers by period.** Where the files carry release dates, count versions released 5, 10 or 20 years after the first release. Use the earliest release year as the song's date and as the time-at-risk control.
- **Report three non-match cases separately.** Distinguish (a) the artist is found in Discogs-VI under a different title, (b) the artist is absent from Discogs-VI entirely, and (c) the artist is present but the title is not. Only (c) is close to a true "not covered". Restrict the within-artist test to artists with at least one matched song.
- **Robustness check.** Rerun on the YT subset (cliques with at least two downloaded versions) and with generic titles excluded (e.g. titles of one word, or titles found in more than k cliques).
- **Manual audit.** Hand-check about 50 matched and 50 unmatched songs against SecondHandSongs to estimate the false-negative and false-positive rates, since the paper gives none.
- **Write down which dump was used.** The paper used July 2024; the Zenodo record may be later.

## 7. Leads
1. Yesiler, Tralie, Correya et al. (2019), "Da-TACOS: A Dataset for Cover Song Identification and Understanding". It is built from SecondHandSongs, which makes it an independent cover ground truth for validation.
2. Bogdanov & Serra (2017), "Quantifying Music Trends and Facts Using Editorial Metadata from the Discogs Database". Discogs coverage biases by genre, era and country, which we need to quantify the confounds.
3. Xu, Chen & Yang (2018), "Key-Invariant CNN Toward Efficient Cover Song Identification". The source of SHS-100K, a second SHS-based clique list for cross-checking matches.
4. Serrà, Zanin, Laurier & Sordo (2009), "Unsupervised Detection of Cover Song Sets: Accuracy Improvement and Original Identification". Covers identifying the original version, which helps define which artist is the "original".
5. Lanzendörfer, Grötschla, Funke & Wattenhofer (2024), "DISCO-10M: A Large-Scale Music Dataset". Another Discogs-linked corpus, a possible source of release-year and genre fields.
