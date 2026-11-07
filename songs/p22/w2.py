"""Song 22 writing room, pass 2: V4.1 -- the novel's 'I kept it for her before I knew there was a her' died on the span (13 > 12); shortened."""
import sys; sys.path[:0] = ["/home/claude/p22", "/home/claude/carol", "/home/claude/pop"]
import engine_p22 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
E.run("V4.1b kept for you", """
contradiction: I kept it for you before there was a you
object: I kept this for you before I knew your face
plain: I wrote it all for you before I knew
""", role="verse", nslots=16, show=4, couplet="wider now, a hand's width east")
E.save("/home/claude/p22/w2.json")
