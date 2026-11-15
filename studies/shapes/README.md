# Shapes of songs

The first study of whether songs have Vonnegut-style shapes (see reports/Shapes of music like story arcs.md and shapes_study_report.md).

- shape_lib.py: the method (resample, cosine smoothing, SVD, shared-shape and types tests against null models, synthetic self-test)
- study_hymn_incipits.py: 4,986 Hymnary.org opening lines against printings
- billboard_parse.py, study_billboard.py: CoCoPops Billboard (listener ratings, 214 melodies, 739 structures) against chart peak and weeks
- study_pdmx.py: 11,266 PDMX scores against views, favourites and ratings (seed 20261115; robustness sample seed 777)

Data are not included. Sources and licences: Hymnary.org tune export (derived counts only); CoCoPops (github.com/Computational-Cognitive-Musicology-Lab/CoCoPops, CC BY-NC 4.0); PDMX (Zenodo 10.5281/zenodo.15571083, CC0 / public domain subset without licence conflict).
