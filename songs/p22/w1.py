"""Song 22 writing room, pass 1 (v64 port): 'The Seam' -- a duet; her verses from the lab side (E minor), his from the window (F minor),
both in the chorus (C major). The novel's images carry the meaning; no plot told; no names (Q11 A). 4/4 at q = 80: a line takes two
bars (12 syllables, v58). Narrative register, leaning abstract; both never-say lists are deaths; Rule V1 on the verse couplets."""
import sys; sys.path[:0] = ["/home/claude/p22", "/home/claude/carol", "/home/claude/pop"]
import engine_p22 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
def V(mate_line=None, **k):
    d = dict(role="verse", nslots=16, show=4, couplet=mate_line); d.update(k); return d
# ===== VERSE 1 -- her: the grey, the warm room, the crack, the hands, the glass =====
E.run("V1.1 the crack", """
object: a hairline crack runs through the grey
plain: there's a crack in the grey floor
time: six inches of crack in a grey that never breaks
""", **V("one warm room at the bottom of the stairs"))
E.run("V1.2 the warm room", """
object: one warm room at the bottom of the stairs
plain: and one warm room below it all
body: I go down to the one warm room
""", **V("a hairline crack runs through the grey"))
E.run("V1.3 the hands", """
body: my hands on the worn place in the wood
object: I keep my hands where the wood is worn
plain: I rest my hands on the keys and wait
""", **V("I watch your window through the glass"))
E.run("V1.4 the glass", """
plain: I watch your window through the glass
object: your window lit behind the glass
you: and you at your window, behind the glass
""", **V("my hands on the worn place in the wood"))
# ===== VERSE 2 -- him: the coffee, the light, the sky wrong by a degree =====
E.run("V2.1 the coffee", """
plain: the coffee's right, the light is right
object: the coffee's warm, the light's the color it should be
""", **V("the sky is wrong by a degree"))
E.run("V2.2 the degree", """
plain: the sky is wrong by a degree
object: but the sky is off by a degree
contradiction: and the sky is wrong, by a hair, above the towers
""", **V("the coffee's right, the light is right"))
E.run("V2.3 two blues", """
object: one blue stops where another starts
plain: where one blue ends another begins
""", **V("I write it down and nobody looks up"))
E.run("V2.4 the notebook", """
plain: I write it down and nobody looks up
object: it's in my notebook, every morning, same hour
understatement: I write it down; it seems the thing to do
""", **V("one blue stops where another starts"))
# ===== CHORUS -- both: the seam =====
E.run("C.1 the seam [kernel]", """
plain: there's a seam
object: a seam across the sky
body: it runs through you and me, the seam
""", kernel="seam", role="hook", nslots=16, show=3)
E.run("C.2 two blues, both real", """
plain: two blues that will not meet
object: two blues, and both of them are real
contradiction: two blues, and neither one is wrong
""", role="chorus", nslots=16, show=3)
E.run("C.3 the line that holds", """
plain: you on your side and me on mine
object: a line we both can see and neither cross
body: my hand against it, and yours
""", role="chorus", nslots=16, show=3)
E.run("C.4 the seam won't close [kernel]", """
plain: and the seam won't close
object: the seam won't close, the seam won't heal
contradiction: and the seam holds open, and the seam holds
""", kernel="seam", role="hook", nslots=16, show=3)
# ===== VERSE 3 -- her: the door, the light in his window, trust the third layer =====
E.run("V3.1 the door", """
object: I built a door I cannot keep
plain: I made a door; it only opens one way
body: I came through a door I built with my own hands
""", **V("the light in your window never goes out"))
E.run("V3.2 his light", """
plain: the light in your window never goes out
object: your lamp stays on when the city dims
""", **V("I built a door I cannot keep"))
E.run("V3.3 the third layer", """
plain: trust the third layer, the note says
object: there's a note on the keys: trust the third layer
contradiction: I trust the third layer, and the third layer holds
""", **V("and the edges thinning while I stay"))
E.run("V3.4 the edges", """
object: and the edges thinning while I stay
plain: and every day the edges thin
time: every day I stay, the edges thin
""", **V("there's a note on the keys: trust the third layer"))
# ===== VERSE 4 -- him: the record kept for her; the seam wider; anyone can see it =====
E.run("V4.1 kept for you", """
contradiction: I kept it for you before I knew there was a you
plain: I kept the record for someone
object: I kept this notebook for a stranger
""", **V("the seam is wider every morning"))
E.run("V4.2 wider", """
plain: the seam is wider every morning
object: wider now, a hand's width east
""", **V("I kept it for you before I knew there was a you"))
E.run("V4.3 anyone can see it", """
plain: now anyone looking east can see it
object: now you don't have to know where to look
""", **V("the bakery's open on the corner"))
E.run("V4.4 the bakery", """
object: the bakery's open on the corner
plain: and the morning goes on like it always does
body: and the bread smell rising from the street
""", **V("now anyone looking east can see it"))
# ===== THE ENDING -- him alone =====
E.run("END.1 the notebook on the sill", """
object: I leave the notebook on the sill
plain: I put the notebook where it can be found
""", role="bridge", nslots=16, show=2)
E.run("END.2 fear requires surprise", """
plain: fear requires surprise
""", role="bridge", nslots=16, show=1)
E.run("END.3 not afraid", """
plain: and I am not afraid
""", role="bridge", nslots=16, show=1)
E.save("/home/claude/p22/w1.json")
print("compounds:", E.COMPOUND_LOG)
