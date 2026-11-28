# Cantometrics call-and-response count (pass 5)

The scripts the pass 5 reader used to count leader-chorus alternation and overlap in the Global Jukebox Cantometrics code tables (Zenodo record 4898406, a 3.3 MB zip, kept outside the repository). The data is not here.

- The brief asked for a reading pass only, so this count was a deviation. Its figures in `5_regional_dialects.md` are our own count of Lomax-era codes, not a published result. Redo it rule first before any use.
- Licence conflict: Zenodo says CC BY-NC 4.0; the zip's own LICENSE.txt says CC BY 4.0. The stricter, non-commercial reading is taken.
- On any redo, leave out ceremonial, initiation and healing songs.
- Run with `python3 -I <script> <path to the unzipped release>`. Codes are stored as bit sums: code k is counted when the value contains 2^k.
