# agent-replay

Turn a Claude Code session log into a **single self-contained HTML file**: a searchable, replayable timeline of every prompt, thought, tool call and result — with token and cost totals. No dependencies, nothing leaves your machine.

Try it: open [`examples/sample.html`](examples/sample.html) (generated from `examples/sample.jsonl`).

## Install

Python 3.9+, standard library only.

```sh
pipx install git+https://github.com/numa08/one-day-claude   # or: pip install .
# or run without installing:
python -m agent_replay --latest
```

## Usage

```sh
agent-replay --latest -o replay.html     # newest session in ~/.claude/projects
agent-replay path/to/session.jsonl       # writes session.html
agent-replay --stats session.jsonl       # terminal summary only
```

## What you get

- Timeline of user / assistant / thinking / tool_use / tool_result events, errors highlighted
- Full-text search and per-kind filters
- ▶ Play: watch the session unfold step by step
- Token totals (cache read/write included) and an **estimated** cost
- Dark/light automatically; one file you can attach to an issue or PR

## Demo steps

1. `agent-replay --latest -o replay.html`
2. Open `replay.html`, press ▶, then search for `error`.

## Notes

- Cost is an estimate from a built-in price table (Opus/Sonnet/Haiku families); check your actual billing.
- Session logs may contain secrets. Review the HTML before sharing it.
- Log format is Claude Code's undocumented JSONL; unknown lines are skipped.

## Roadmap

Other agents' formats, redaction rules, diff/merge views, hosted share links.

## Test

```sh
python -m unittest
```

MIT
