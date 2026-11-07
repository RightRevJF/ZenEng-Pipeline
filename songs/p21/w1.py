"""Song 21 writing room, pass 1 (v64 port): named moves; the poem 'Cattywumpus' kept, its images in order (Q1 A), present tense, I to
you (Q3 A). 4/4 at q = 72: a line takes two bars (14 syllables, v58). Narrative register; both never-say lists are deaths; Rule V1
on for verse lines, read on the couplet. The hook 'the afternoon will have to make do' (Q2 B); 'cattywumpus' once, in a verse,
CAT-uh-WAM-pus (Q12 B)."""
import sys; sys.path[:0] = ["/home/claude/p21", "/home/claude/carol", "/home/claude/pop"]
import engine_p21 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
def V(mate_line=None, **k):
    d = dict(role="verse", nslots=16, show=4, couplet=mate_line); d.update(k); return d
# ===== VERSE 1 -- the car, the cold air, you =====
E.run("V1.1 the windows, the leather", """
object: the windows blacked out and the leather still warm
plain: the windows blacked out, the leather under me
body: the leather under me still holding our shape
""", **V("the air conditioner hums against the evidence"))
E.run("V1.2 the quiet work", """
object: the air conditioner hums against the evidence
plain: the cold air starts its quiet work against the evidence
time: the air conditioner starts its quiet work
""", **V("the windows blacked out and the leather still warm"))
E.run("V1.3 you, the tremor", """
body: you beside me and a small tremor working its way out
plain: you beside me, and a tremor working its way out
object: a small tremor working its way out of me
""", **V("the air smells of skin and cooling dust"))
E.run("V1.4 skin and dust", """
object: the air smells of skin and cooling dust
plain: and the air smells of skin and cooling dust
""", **V("you beside me and a small tremor working its way out"))
# ===== VERSE 2 -- the clothes, the shade =====
E.run("V2.1 the footwell", """
object: your clothes lie in the footwell where they fell
plain: your clothes are in the footwell where they fell
""", **V("the shade a black eyelid that will not quite close"))
E.run("V2.2 the eyelid", """
object: the shade a black eyelid that will not quite close
plain: and the light gets in where the shade won't close
body: a black eyelid on the glass that will not quite close
""", **V("your clothes lie in the footwell where they fell"))
E.run("V2.3 both hands", """
body: we wrestled it into place with both hands
plain: we fought the shade into place with all four hands
object: we wrestled the shade up with all four hands
""", **V("but one corner's gone cattywumpus, loose in its dark"))
E.run("V2.4 cattywumpus", """
object: but one corner's gone cattywumpus, loose in its dark
plain: but one corner's gone cattywumpus
contradiction: one corner gone cattywumpus, a little loose in its dark
""", **V("we wrestled it into place with both hands"))
# ===== CHORUS =====
E.run("C.1 the light at the corner", """
plain: I watch that corner and the light it lets through
object: I watch the thin light come in at the corner
body: I lie here watching that one bright seam
""", role="chorus", nslots=16, show=3)
E.run("C.2 the warmth leaving", """
plain: while the last of the warmth leaves me
object: and the last warmth leaving me
""", role="chorus", nslots=16, show=3)
E.run("C.3 the day outside", """
plain: let the day go on without us
object: the whole bright day is waiting out there
contradiction: we're not ready to be anywhere
""", role="chorus", nslots=16, show=3)
E.run("C.4 the hook [kernel]", """
plain: the afternoon will have to make do
object: and the afternoon will have to make do
""", kernel="make do", role="hook", nslots=16, show=2)
E.save("/home/claude/p21/w1.json")
print("compounds:", E.COMPOUND_LOG)
