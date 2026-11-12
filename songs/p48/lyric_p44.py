"""Keeping Time -- the locked lyric (11 Nov, Q15 A). From the writer's essay 'The Problem of the Other Mind', used and not copied: the
verses are failed answers (a face, then speech), the pre-choruses name the assumption, the chorus re-asks, the bridge goes one level up,
the last chorus says it plainly. Nothing obvious named (Q1 C note); one faint echo ('hear', Q2 B)."""
TITLE = "Keeping Time"
V1 = [("verse", "Strobe light cuts you into stills"), ("verse", "A different face in every flare"),
      ("verse", "You sing along with your eyes closed"), ("verse", "To someone who isn't there")]
PRE1 = [("pre", "We all walked in on our own"), ("pre", "Till the kick came up through the bone")]
CH = [("chorus", "I can't get behind your eyes"), ("chorus", "But your count keeps falling into mine"),
      ("chorus", "Two clocks on the same wall"), ("hook", "Can't help keeping time, keeping time")]
POST = [("tag", "Fall on the one, fall on the one"), ("tag", "Nobody's counting anymore")]
V2 = [("verse", "You cup your hand against my ear"), ("verse", "The bass eats every vowel whole"),
      ("verse", "You type it out and turn your phone"), ("verse", "The screen times out, I'll never know")]
PRE2 = [("pre", "Two strangers shouting through a wall"), ("pre", "And both of us lean on it after all")]
BRIDGE = [("bridge", "Who set the beat before we came"), ("bridge", "Who made us quick to fall in step"),
          ("bridge", "The one who started it came down"), ("bridge", "And played it close enough to hear")]
LAST = CH[:2] + [("chorus", "It was always the same wall"), CH[3]]
POST3 = [("tag", "Fall on the one, fall on the one"), ("tag", "Nobody's leaving anymore")]
SECTIONS = [("Verse 1", V1), ("Pre 1", PRE1), ("Chorus 1", CH), ("Post 1", POST), ("Verse 2", V2), ("Pre 2", PRE2), ("Chorus 2", CH),
            ("Post 2", POST), ("Bridge", BRIDGE), ("Last Chorus", LAST), ("Post 3", POST3)]
SUNG = [l for _, ls in SECTIONS for _, l in ls]
import re, importlib.util as _u
_s = _u.spec_from_file_location("intake44", "/home/claude/p48/intake.py"); _I = _u.module_from_spec(_s); _s.loader.exec_module(_I)
_t = " ".join(SUNG).lower()
assert not (set(re.findall(r"[a-z']+", _t)) & set(_I.NEVER_SAY))
assert not any(p in _t for p in _I.NEVER_PHRASES)
_lock = open("/home/claude/p48/lyric_locked.md").read()
assert all(l in _lock for l in SUNG), [l for l in SUNG if l not in _lock]               # every sung line is the locked lyric's
