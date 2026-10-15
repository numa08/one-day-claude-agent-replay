import argparse
import glob
import os
import sys

from . import __version__
from .parse import parse_file
from .render import render_html


def latest_session():
    files = glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl"))
    return max(files, key=os.path.getmtime) if files else None


def format_stats(st):
    u = st["usage"]
    lines = [
        f"events:  {st['events']}  (errors: {st['errors']}, skipped lines: {st['skipped']})",
        f"models:  {', '.join(st['models']) or '-'}",
        f"tokens:  in={u['input']:,} out={u['output']:,} cache_read={u['cache_read']:,} cache_write={u['cache_write']:,}",
        f"cost:    ~${st['cost_usd']:.2f}{'' if st['cost_complete'] else '+ (some models unpriced)'}  (estimate)",
        "tools:   " + (", ".join(f"{k}×{v}" for k, v in sorted(st["tools"].items(), key=lambda x: -x[1])) or "-"),
    ]
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="agent-replay", description="Turn a Claude Code session log into a self-contained HTML replay.")
    ap.add_argument("session", nargs="?", help="session .jsonl file")
    ap.add_argument("--latest", action="store_true", help="use the newest session in ~/.claude/projects")
    ap.add_argument("-o", "--output", help="output HTML path (default: <session>.html)")
    ap.add_argument("--stats", action="store_true", help="print a summary instead of writing HTML")
    ap.add_argument("--version", action="version", version=__version__)
    a = ap.parse_args(argv)
    path = a.session or (latest_session() if a.latest else None)
    if not path:
        ap.error("give a session file or --latest")
    if not os.path.isfile(path):
        print(f"error: not found: {path}", file=sys.stderr)
        return 1
    parsed = parse_file(path)
    if a.stats:
        print(format_stats(parsed["stats"]))
        return 0
    out = a.output or os.path.splitext(os.path.basename(path))[0] + ".html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_html(parsed, title=os.path.basename(path)))
    print(f"wrote {out} ({parsed['stats']['events']} events)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
