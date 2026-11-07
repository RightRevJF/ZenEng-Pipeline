"""Song 21 writing room, pass 4: the writer's own lines (19:48), scored as his (locked; the filters report, the stress check stands)."""
import sys; sys.path[:0] = ["/home/claude/p21", "/home/claude/carol", "/home/claude/pop"]
import engine_p21 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
for name, line, role in (("C.1w", "I watch a blade of daylight find its way in", "chorus"), ("C.1w alt", "a little daylight slipping through the corner", "chorus"),
                         ("C.2w", "while the warmth is slow to leave me", "chorus"), ("V2.3 test", "we wrestled the shade up with all four hands", "verse"),
                         ("V2.3 fallback", "we wrestled the shade up with both our hands", "verse"), ("V2.4w", "one corner gone cattywumpus in the dark", "verse")):
    E.run(name, line, role=role, nslots=16, show=1)
E.save("/home/claude/p21/w4.json")
import lyricsearch as LS
print([(x[0], x[2]) for x in LS.syllables("we wrestled the shade up with all four hands")])
