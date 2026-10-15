# 調査メモ (2026-10-15)

## 取得できた情報と制約
- GitHub Trending(weekly) は取得できた。Hacker News / Algolia API は 403 で取得不可。
- Web 検索は一般的な内容ばかりで、最新トレンドの裏付けは薄かった。

## GitHub Trending (weekly) 出典: https://github.com/trending?since=weekly
| リポジトリ | 内容 | 所感 |
|---|---|---|
| mattpocock/skills | エージェント向け skills 集 (12k stars/週) | エージェントの設定・スキル共有に需要 |
| cathrynlavery/diagram-design | AI コーディングツール向け図版デザイン (HTML/SVG) | 見た目が映える成果物は伸びる |
| heygen-com/hyperframes | HTML から動画を生成、エージェント向け | 「エージェントが使える」ことが売り |
| tester-army/e2e | E2E テスト自動化 | テスト自動化への需要 |
| thedotmack/claude-mem | エージェントセッション間の永続メモリ | コンテキスト引き継ぎの不満 |
| earthtojake/text-to-cad | エージェントに CAD 能力 | 領域特化の agent ツール |
| twostraws/SwiftUI-Agent-Skill | SwiftUI 用 agent skill | 言語/FW 別 skill |

## 傾向
1. コーディングエージェント周辺(skills、メモリ、テスト、図/動画生成)が圧倒的に伸びている。
2. 「エージェントが使える形式 (HTML/SVG/CLI)」で出力する小さな単機能ツールが受ける。
3. 見た目で価値が伝わるもの(図、動画)はデモ映えする。

## 開発者の不満(出典: https://codex.danielvaughan.com/2026/03/30/reddit-codex-cli-sentiment-march-2026/ ほか)
- エージェント CLI の使用量メータリングが不透明(トークン/コスト把握が難しい)。
- セッション間でコンテキストが失われる。
- クラウドコンソール等を開かずターミナルだけで完結したい (https://dev.to/zop_8abedcc7e12/an-open-source-cli-that-solves-one-common-pain-point-5a2d)。
