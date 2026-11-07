"""Song 21 writing room, pass 2: V1.1 -- the poem's opening image (the blacked-out windows) kept without 'still warm', since the
chorus carries the warmth leaving (the critique the writer heard: the warmth said twice)."""
import sys; sys.path[:0] = ["/home/claude/p21", "/home/claude/carol", "/home/claude/pop"]
import engine_p21 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
E.run("V1.1b the windows, the leather", """
object: the windows blacked out, the leather holding our shape
plain: the windows blacked out and the leather holding our shape
body: windows blacked out, and the leather still holding our shape
""", role="verse", nslots=16, show=4, couplet="the air conditioner hums against the evidence")
E.save("/home/claude/p21/w2.json")
