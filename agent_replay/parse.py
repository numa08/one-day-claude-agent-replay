"""Parse Claude Code session JSONL into a flat list of events + stats."""
import json

# USD per 1M tokens (input, output). Estimates only; cache read = 0.1x input,
# cache write = 1.25x input.
PRICES = {
    "opus": (15.0, 75.0),
    "sonnet": (3.0, 15.0),
    "haiku": (1.0, 5.0),
}


def price_for(model):
    m = (model or "").lower()
    for key, val in PRICES.items():
        if key in m:
            return val
    return None


def _text_of(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for c in content:
            if isinstance(c, dict):
                if c.get("type") == "text":
                    parts.append(str(c.get("text", "")))
                else:
                    parts.append(json.dumps(c, ensure_ascii=False))
            else:
                parts.append(str(c))
        return "\n".join(parts)
    return json.dumps(content, ensure_ascii=False)


def parse_lines(lines):
    events = []
    seen_msg = set()
    usage = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    cost = 0.0
    cost_known = True
    models = set()
    tools = {}
    errors = 0
    skipped = 0
    first_ts = last_ts = None

    def add(kind, ts, **kw):
        ev = {"i": len(events), "kind": kind, "ts": ts}
        ev.update(kw)
        events.append(ev)
        return ev

    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except ValueError:
            skipped += 1
            continue
        if not isinstance(obj, dict) or obj.get("type") not in ("user", "assistant"):
            continue
        msg = obj.get("message")
        if not isinstance(msg, dict):
            skipped += 1
            continue
        ts = obj.get("timestamp")
        if ts:
            first_ts = first_ts or ts
            last_ts = ts
        role = obj["type"]
        content = msg.get("content")
        if role == "assistant":
            model = msg.get("model")
            mid = msg.get("id")
            u = msg.get("usage")
            if model:
                models.add(model)
            if isinstance(u, dict) and mid not in seen_msg:
                if mid:
                    seen_msg.add(mid)
                i_, o_ = u.get("input_tokens") or 0, u.get("output_tokens") or 0
                cr, cw = u.get("cache_read_input_tokens") or 0, u.get("cache_creation_input_tokens") or 0
                usage["input"] += i_
                usage["output"] += o_
                usage["cache_read"] += cr
                usage["cache_write"] += cw
                p = price_for(model)
                if p:
                    cost += (i_ * p[0] + o_ * p[1] + cr * p[0] * 0.1 + cw * p[0] * 1.25) / 1e6
                elif i_ or o_:
                    cost_known = False
        blocks = content if isinstance(content, list) else [{"type": "text", "text": content}] if isinstance(content, str) else []
        for b in blocks:
            if not isinstance(b, dict):
                continue
            t = b.get("type")
            if t == "text":
                text = str(b.get("text", ""))
                if text.strip():
                    add(role, ts, text=text)
            elif t == "thinking":
                text = str(b.get("thinking", ""))
                if text.strip():
                    add("thinking", ts, text=text)
            elif t == "tool_use":
                name = str(b.get("name", "?"))
                tools[name] = tools.get(name, 0) + 1
                add("tool_use", ts, tool=name, id=b.get("id"),
                    text=json.dumps(b.get("input"), ensure_ascii=False, indent=2))
            elif t == "tool_result":
                err = bool(b.get("is_error"))
                errors += err
                add("tool_result", ts, id=b.get("tool_use_id"), error=err,
                    text=_text_of(b.get("content")))
    return {
        "events": events,
        "stats": {
            "usage": usage,
            "cost_usd": round(cost, 4),
            "cost_complete": cost_known,
            "models": sorted(models),
            "tools": tools,
            "errors": errors,
            "skipped": skipped,
            "start": first_ts,
            "end": last_ts,
            "events": len(events),
        },
    }


def parse_file(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return parse_lines(f)
