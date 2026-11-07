"""Song 23 writing room (v64 port): 'What Holds' -- the lines drafted with the writer over three rounds (12:32-12:37), each slot's
versions scored here for the record: draft 1 (the run's), draft 2 (the writer's notes: trust the picture, a line that sticks, tighter
percussive phrases), draft 3 (the writer's notes: the chorus's middle lines, the final line's landing). 4/4 at q = 104: a line takes two
bars (10 syllables, v58). Both never-say lists are deaths; Rule V1 on the verse couplets."""
import sys; sys.path[:0] = ["/home/claude/p23", "/home/claude/carol", "/home/claude/pop"]
import engine_p23 as E, phrasestress48 as P; P.install(E); E.install_patches()
E.METER = "4/4"
def V(mate=None, **k):
    d = dict(role="verse", nslots=16, show=4, couplet=mate); d.update(k); return d
E.run("V1.1 the arch", """
object: every stone in the arch is falling
object: granite curve across the river
""", **V("every block bent toward the ground"))
E.run("V1.2 the stones lean", """
plain: each one leaning on the next
body: every block bent toward the ground
""", **V("granite curve across the river"))
E.run("V1.3 the top stone", """
plain: there's nothing beneath the middle stone
object: top stone hung on empty air
""", **V("trucks roll over all day long"))
E.run("V1.4 it holds", """
contradiction: the falling is what keeps it standing
object: trucks roll over all day long
""", **V("top stone hung on empty air"))
E.run("C.1 what holds [title]", """
plain: what holds is a hand that pushes back
body: what holds is the hand against me
""", kernel="what holds", role="hook", nslots=16, show=2)
E.run("C.2 the push", """
body: two palms flat and leaning in
body: palm to palm and pushing in
object: locked like rafters at the ridge
""", role="chorus", nslots=16, show=3)
E.run("C.3 without it", """
plain: take one away and the other falls
plain: let it go and down I come
object: take your weight away, I'm rubble
""", role="chorus", nslots=16, show=3)
E.run("C.4 the hook", """
plain: what holds is the push from both sides
contradiction: push me, and I stand
""", role="hook", nslots=16, show=2)
E.run("V2.1 the wire", """
object: a man on a wire with a pole in his hands
object: wire strung between two towers
""", **V("one man out there, pole held wide"))
E.run("V2.2 the man", """
plain: weight on the left and weight on the right
object: one man out there, pole held wide
""", **V("wire strung between two towers"))
E.run("V2.3 the pull", """
contradiction: the harder it pulls him both ways at once
object: wind on the left, wind on the right
""", **V("he walks it like a kitchen floor"))
E.run("V2.4 the walk", """
contradiction: the stiller he walks in the open air
object: he walks it like a kitchen floor
""", **V("wind on the left, wind on the right"))
E.run("B.1 the bones", """
body: every bone I've got is pulled two ways
body: every bone pulled two ways
""", role="bridge", nslots=16, show=2)
E.run("B.2 the muscles", """
body: one muscle bends what the other straightens
body: one muscle bends, one straightens
""", role="bridge", nslots=16, show=2)
E.run("B.3 the strain", """
plain: I'm not standing in spite of the strain
plain: not in spite of the strain
""", role="bridge", nslots=16, show=2)
E.run("B.4 because", """
plain: I'm standing because of it
plain: I stand because of it
""", role="bridge", nslots=16, show=2)
E.run("CF.4 the turn", """
plain: what holds is what I'm made of
plain: push me, that's what holds
contradiction: push me, and I stand: that's what holds
""", role="hook", nslots=16, show=3)
E.save("/home/claude/p23/w1.json")
print("compounds:", E.COMPOUND_LOG)
