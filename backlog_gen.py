#!/usr/bin/env python3
"""
Convert PRD.md headings into .backlog/tasks.json + tasks/*.md.
Heading syntax:

## 3 Payment page (depends: 2)
- bullet spec line…
"""
import sys, json, re, pathlib, fileinput
from collections import OrderedDict

if len(sys.argv) != 2:
    sys.exit("Usage: backlog_gen.py PRD.md")

prd_path = pathlib.Path(sys.argv[1])
out_dir  = pathlib.Path(".backlog/tasks")
out_dir.mkdir(parents=True, exist_ok=True)

ledger = OrderedDict()
tid, title, deps, body = 0, "", [], []

def flush():
    global tid, title, deps, body
    if not title: return
    tid += 1
    (out_dir / f"{tid}.md").write_text(f"# Task {tid} – {title}\n" +
        ("\n".join(body) or "TODO") + "\n")
    ledger[str(tid)] = {"title": title, "status": "TODO",
                        "deps": deps, "complexity": 1}
    title, deps, body[:] = "", [], []

for line in prd_path.read_text().splitlines():
    h = re.match(r"^##\s+\d+\s+(.+?)(?:\s+$begin:math:text$depends:\\s*([\\d,\\s]+)$end:math:text$)?$", line)
    if h:
        flush()
        title = h.group(1).strip()
        deps  = [int(x) for x in h.group(2).split(",")] if h.group(2) else []
    else:
        body.append(line.rstrip())

flush()
pathlib.Path(".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
print(f"Generated {len(ledger)} tasks → .backlog/")