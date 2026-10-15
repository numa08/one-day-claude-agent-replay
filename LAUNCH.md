# LAUNCH (下書き)

## X / Twitter (日本語)
Claude Code のセッションログを、依存ゼロの1枚HTMLに変換する agent-replay を作りました。
プロンプト・思考・ツール呼び出し・エラーをタイムラインで再生、検索、トークン/推定コストも一目で。
`agent-replay --latest` だけ。MIT。
https://github.com/numa08/one-day-claude

## X / Twitter (English)
agent-replay: turn a Claude Code session log into one self-contained HTML file — replayable timeline, search, tool calls, errors, token & cost totals. Zero dependencies, runs locally.
`agent-replay --latest` · MIT
https://github.com/numa08/one-day-claude

## Hacker News
**Title:** Show HN: agent-replay – Replay Claude Code sessions as a single HTML file

**Body:**
Claude Code writes every session to JSONL under ~/.claude/projects, but it's hard to read back. agent-replay converts one into a self-contained HTML page: timeline of prompts, thinking, tool calls and results, errors highlighted, full-text search, a play button to step through, and token/estimated-cost totals (de-duplicated across streamed chunks).

Python stdlib only, no network, one file output you can attach to a PR. Cost is an estimate from a built-in price table. The log format is undocumented, so unknown lines are skipped. Feedback welcome on other agents' formats and redaction.
