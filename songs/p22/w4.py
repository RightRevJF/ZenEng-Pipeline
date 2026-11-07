"""Song 22 writing room, pass 4 (the run's own review, 06:49): the last chorus's turn after the instrumental; her glass vs his window."""
import sys; sys.path[:0] = ["/home/claude/p22", "/home/claude/carol", "/home/claude/pop"]
import engine_p22 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
E.run("CF.4 the last chorus's turn [kernel]", """
plain: the seam won't close, and we don't ask it to
object: the seam stays open, and we let it stay
contradiction: the seam won't close, and neither will we
""", kernel="seam", role="hook", nslots=16, show=3)
E.run("V1.4b her glass", """
object: your window lit behind my glass
plain: your window, lit, beyond my glass
""", role="verse", nslots=16, show=2, couplet="my hands on the worn place in the wood")
E.save("/home/claude/p22/w4.json")
