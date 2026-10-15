## 概要
Claude Code のセッションログ(JSONL)を依存ゼロの1ファイルHTML(再生・検索・トークン/コスト)に変換する CLI「agent-replay」の MVP。調査〜仕様は research/, IDEAS.md, DECISION.md, SPEC.md 参照。

## 公開前に人間が確認すること
- デモ GIF が未収録(SPEC のシナリオ参照)。README に追記
- コスト単価表(parse.py PRICES)が最新か
- ログ形式は非公式。実セッションで `--latest` を試す
- LAUNCH.md の文面とリポジトリ URL
