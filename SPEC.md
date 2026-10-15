# SPEC: agent-replay

## 概要
Claude Code のセッションログ(`~/.claude/projects/**/*.jsonl`)を、依存ゼロ・1ファイルの自己完結 HTML(タイムライン再生・検索・トークン/コスト集計)に変換する CLI。

## MVP 範囲
- `agent-replay <session.jsonl> [-o out.html]`: HTML を生成
- `agent-replay --stats <session.jsonl>`: ターミナルにサマリ(ターン数、ツール別回数、トークン、推定コスト)
- `agent-replay --latest`: `~/.claude/projects` 内で最新のセッションを対象にする
- HTML 機能: タイムライン(ユーザー/アシスタント/思考/ツール呼び出し/結果)、ツール呼び出しと結果の対応表示、エラー強調、全文検索、種別フィルタ、▶ 再生(1イベントずつ表示)、トークン/推定コストのサマリ、ダーク/ライト自動
- 非対応(将来): 他エージェント形式、ホスティング、要約

## 受け入れ基準
1. サンプル JSONL から HTML が生成され、外部リソース参照(http(s) の src/href)を含まない
2. 同一 message.id の分割行でトークンが二重計上されない
3. tool_use と tool_result が id で対応付く。is_error が保持される
4. 不正な行・未知の type があってもクラッシュせずスキップする
5. `</script>` を含むログでも HTML が壊れない(エスケープ)
6. `--stats` が集計を出力する
7. `python -m unittest` が全て通る

## 技術スタック
Python 3.9+ 標準ライブラリのみ(MIT)。HTML 内は素の JS/CSS。

## README 構成
キャッチ → デモ GIF/スクショ → インストール(pipx / 直接実行) → 使い方 → 出力の機能 → コスト推定の注意 → ロードマップ → ライセンス

## デモ GIF シナリオ(30秒)
1. `agent-replay --latest -o replay.html` を実行
2. ブラウザで開く → サマリ(トークン/コスト)が見える
3. ▶ を押してタイムラインが流れる
4. 検索ボックスに "error" と入れて絞り込む
