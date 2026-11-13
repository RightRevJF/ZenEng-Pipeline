"""Dry Ground -- the locked lyric (13 Nov, 'Lock it!'). From the writer's sonnet 'Ark', used and not copied (src/, not committed):
its images and story kept, the lines new (Q2 B); his voice alone (Q3 A); Noah named once, in the bridge (Q9 C)."""
TITLE = "Dry Ground"
V1 = [("verse", "Cold little hum of a parked car"), ("verse", "Foil on the glass to hide the day"),
      ("verse", "The quarter pane fought my thumb and gave"), ("verse", "And the grey came up and we drifted away")]
PRE1 = [("pre", "The heater blowing round our feet"), ("pre", "The windows running thick with breath"),
        ("pre", "The red brick swimming in the glass"), ("pre", "Till the last dry thing went under")]
CH = [("hook", "Now I'm living on dry ground"), ("chorus", "Every window painted shut"),
      ("chorus", "The sprinkler hangs a rainbow on the lawn"), ("chorus", "It's never gonna flood again"),
      ("chorus", "And I miss the water"), ("tag", "God I miss the flood")]
V2 = [("verse", "Your back the slow tide of your hips"), ("verse", "Pulled me under and up again"),
      ("verse", "Light like honey where your backbone dips"), ("verse", "Your skin a garden after rain")]
PRE2 = [("pre", "The little coo you couldn't keep"), ("pre", "A dove sent out to look for land"),
        ("pre", "She came back with nothing in her mouth"), ("pre", "So we went down again")]
BRIDGE = [("bridge", "Every day I pass the library"), ("bridge", "High on the hill like it ran aground"),
          ("bridge", "The bird came home with a leaf in her mouth"), ("bridge", "And Noah stood there missing the rain")]
LAST = CH[:3] + [("chorus", "I stand out in it till I'm soaked")] + CH[4:]
OUTRO = [("outro", "Some days I park where we used to park"), ("outro", "Same cold hum and an empty seat"),
         ("outro", "Roll the little window down"), ("outro", "And let the grey come in")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH),
            ("Bridge", BRIDGE), ("Last Chorus", LAST), ("Outro", OUTRO)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
import re, importlib.util as _u
_s = _u.spec_from_file_location("intake46", "/home/claude/p56/intake.py"); _I = _u.module_from_spec(_s); _s.loader.exec_module(_I)
_t = " ".join(SUNG).lower()
assert not (set(re.findall(r"[a-z']+", _t)) & set(_I.NEVER_SAY))
_lock = open("/home/claude/p56/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]
assert _t.count("noah") == 1                                                           # Q9 C: Noah once
