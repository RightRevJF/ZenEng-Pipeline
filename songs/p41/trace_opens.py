"""309: list every file a run reads (an audit hook on open and import), for the repo."""
import sys, os, runpy
seen = set()
def hook(ev, args):
    if ev == "open" and args and isinstance(args[0], (str, bytes, os.PathLike)):
        p = os.path.realpath(os.fsdecode(args[0]))
        if p.startswith("/home/claude") and os.path.isfile(p): seen.add(p)
    elif ev == "import":
        pass
sys.addaudithook(hook)
script = sys.argv[1]; sys.argv = sys.argv[1:]
try: runpy.run_path(script, run_name="__main__")
finally:
    mods = {os.path.realpath(m.__file__) for m in list(sys.modules.values()) if getattr(m, "__file__", None) and m.__file__.startswith("/home/claude")}
    out = sorted((seen | mods) - {os.path.realpath(__file__)})
    open(os.environ.get("TRACE_OUT", "reads.txt"), "w").write("\n".join(out) + "\n")
    print(len(out), "files read")
