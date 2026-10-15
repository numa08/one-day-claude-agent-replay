#!/usr/bin/env bash
# Mac 側で動かす自律運転ループ（Docker Sandboxes 版）
# 使い方: caffeinate -i ./run-host.sh
#   試運転は HOURS=0.5 caffeinate -i ./run-host.sh
set -u
cd "$(dirname "$0")"
mkdir -p logs

SB="${SB:-day1}"            # サンドボックス名
HOURS="${HOURS:-10}"        # 最長運転時間
MAX_RUNS="${MAX_RUNS:-60}"  # 最大実行回数
MAX_TURNS="${MAX_TURNS:-80}"

END=$(( $(date +%s) + $(awk "BEGIN{print int($HOURS*3600)}") ))
PROMPT="$(cat PROMPT.md)"

# サンドボックス内のクローンで day1 ブランチに切り替える
sbx exec "$SB" -- bash -c 'git switch day1 2>/dev/null || git switch -c day1'

i=0
while [ "$(date +%s)" -lt "$END" ] && [ "$i" -lt "$MAX_RUNS" ]; do
  if sbx exec "$SB" -- test -f DONE; then
    echo "[$(date '+%F %T')] DONE after $i runs" | tee -a logs/runner.log
    break
  fi

  i=$((i+1))
  echo "[$(date '+%F %T')] run $i start" | tee -a logs/runner.log

  if ! sbx exec "$SB" -- claude --dangerously-skip-permissions \
      -p "$PROMPT" \
      --max-turns "$MAX_TURNS" \
      --output-format stream-json --verbose \
      > "logs/run-$i.jsonl" 2>&1; then
    # 利用上限・一時エラー時は待ってから再試行
    echo "[$(date '+%F %T')] run $i failed, sleeping 10min" | tee -a logs/runner.log
    sleep 600
  fi

  sbx exec "$SB" -- git push -u origin day1 >/dev/null 2>&1
  sleep 30
done

echo "[$(date '+%F %T')] loop finished ($i runs)" | tee -a logs/runner.log
