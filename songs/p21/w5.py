"""Song 21 writing room, pass 5: the writer's notes (19:51), scored as his lines."""
import sys; sys.path[:0] = ["/home/claude/p21", "/home/claude/carol", "/home/claude/pop"]
import engine_p21 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
for name, line, role in (("V2.3w into place", "we wrestled the shade into place with all four hands", "verse"),
                         ("V2.3w down", "we wrestled the shade down with all four hands", "verse"),
                         ("V3.1w floor", "you hand me my shirt from the floor", "verse"),
                         ("C.2 keep", "while the warmth is slow to leave me", "chorus"),
                         ("C.2w A", "while the warmth is slow to leave", "chorus"),
                         ("C.2w B", "warmth still slow to leave me", "chorus")):
    E.run(name, line, role=role, nslots=16, show=1)
E.save("/home/claude/p21/w5.json")
