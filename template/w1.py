"""Song 27 writing room (v64 port, v65 fixes as ports): 'Either Or' -- the lines drafted with the writer (11:47-12:56), scored here for
the record: his poem's stanzas (draft 1-2), the new verses (draft 3), and drafts 4-5 from his notes. Verses 5/4 (3+2) at q = 132, a line
two bars (20 eighths); the refrain 4/4, a line two bars (16 eighths). Rule V1 on the couplets."""
import sys; sys.path[:0] = ["/home/claude/p27", "/home/claude/carol", "/home/claude/pop"]
import engine_p27 as E, phrasestress48 as P; P.install(E); E.install_patches()
def V(mate=None, **k):
    d = dict(role="verse", nslots=20, show=6, couplet=mate); d.update(k); return d
E.METER = "5/4"
E.run("V1.1-2 the line (poem -> drafts 3-5)", """
plain: where is the conflict? it's with either or
plain: birthed by a thinker whose thought line was poor
plain: birthed by Aristotle, whose line of thought was poor
object: Aristotle drew a line in the dust
object: Aristotle drew a line across the dust
plain: said a thing is true or it's a lie
plain: said one thing's true and the other must be lies
""", **V())
E.run("V1.3-4 the blood (poem -> drafts 3-5)", """
body: now there is anguish, everyone's made sore
plain: all 'cause of Ari, should've known he's a boor
body: and we've been bleeding on that line ever since
body: and we've bled across that line ever since
body: calling our own blood the other side
""", **V())
E.run("V2 the tower (poem -> drafts 3-5)", """
plain: theologians are cowards, hiding in words
plain: crowing their nonsense, syllables for the birds
object: they sat in the tower systematizing wind
object: stacking up syllables for the birds
object: weighing the wind by the words that they heard
object: then they sprinkled water on whatever they wrote
object: sprinkled holy water on the laws they wrote
plain: and the herd said amen, word for word
""", **V())
E.run("V3 the stones (poem -> drafts 3-5)", """
plain: the mugwumps are hated by denizens of dread
object: who spin issues into inheritance, bones into bread
plain: telling you one thing, different from what's read
plain: and it's into perdition that you're being led
object: the ones in the middle catch the stones
object: the ones who won't choose catch the stones
plain: from the denizens of dread
object: from the keepers of the dead
plain: who hand them their fathers' wars by name
plain: handing down their fathers' wars by name
object: turning bones into bread
""", **V())
E.METER = "4/4"
E.run("R the wind (draft 1 -> 5)", """
object: and the wind blows where it wants to blow
plain: it doesn't stop to ask you yes or no
plain: you can't nail it down, you can't keep score
plain: you can't fence it in, you can't keep score
plain: the wind was never either or
plain: and you were never either or
""", role="refrain", nslots=16, show=6)
E.save("/home/claude/p27/w1.json")
print("compounds:", E.COMPOUND_LOG)
