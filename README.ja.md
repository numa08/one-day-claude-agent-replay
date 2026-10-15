# agent-replay

[English](README.md) | 日本語

Claude Code のセッションログを、**依存ファイルなしの単一 HTML** に変換するツールです。プロンプト、思考、ツール呼び出し、結果をすべて含む、検索・再生可能なタイムラインとして閲覧でき、トークン数とコストの合計も確認できます。外部ライブラリは不要で、データがマシンの外に出ることもありません。

試す: [`examples/sample.html`](examples/sample.html) を開いてください(`examples/sample.jsonl` から生成したサンプルです)。

## インストール

Python 3.9 以上、標準ライブラリのみで動作します。

```sh
pipx install git+https://github.com/numa08/one-day-claude-agent-replay   # または: pip install .
# インストールせずに実行する場合:
python -m agent_replay --latest
```

## 使い方

```sh
agent-replay --latest -o replay.html     # ~/.claude/projects 内の最新セッションを変換
agent-replay path/to/session.jsonl       # session.html を出力
agent-replay --stats session.jsonl       # ターミナルに要約だけを表示
```

## できること

- user / assistant / thinking / tool_use / tool_result のイベントをタイムライン表示し、エラーを強調
- 全文検索と種類別フィルタ
- ▶ 再生: セッションの進行をステップごとに再現
- トークン合計(キャッシュの読み書きを含む)と**推定**コスト
- ダーク/ライトを自動で切り替え。1 ファイルなので Issue や PR にそのまま添付できる

## デモの手順

1. `agent-replay --latest -o replay.html`
2. `replay.html` を開いて ▶ を押し、`error` で検索してみる

## 注意事項

- コストは内蔵の価格表(Opus / Sonnet / Haiku 系)からの推定値です。実際の請求額はご自身で確認してください。
- セッションログには秘密情報が含まれる場合があります。共有する前に HTML の内容を確認してください。
- ログ形式は Claude Code の非公開 JSONL です。解釈できない行はスキップされます。

## ロードマップ

他のエージェントのログ形式への対応、マスキングルール、差分・マージ表示、共有リンクのホスティング。

## テスト

```sh
python -m unittest
```

## このリポジトリについて

このリポジトリは、Claude Code を 1 日放置して「何を作るか」を自分で判断させた結果出来上がった成果物です。企画・実装・ドキュメントはすべて Claude Code が行いました。経緯は [`DECISION.md`](DECISION.md)、[`PROGRESS.md`](PROGRESS.md)、[`IDEAS.md`](IDEAS.md) にあります。

## ライセンス

MIT
