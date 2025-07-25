#!/usr/bin/env python3
"""
auto_split_backlog.py
Re-build tasks from PRD.md and auto-split any task whose Specs list
is longer than SPLIT_LIMIT lines.

Split rules:
    Task 7  →  7.1, 7.2, 7.3 …   (same deps as parent)
    Parent task is marked DONE with note "split into 7.x".

Usage:  python3 auto_split_backlog.py PRD.md
"""

import re, json, pathlib, sys, textwrap
from collections import OrderedDict
from itertools import islice
SPLIT_LIMIT = 6               # lines in Specs before we split

# ------------ helpers -------------------------------------------------------

def parse_prd(prd_path: pathlib.Path):
    hdr = re.compile(r"^##\s+(\d+)\s+([^\(]+?)(?:\s+\(depends:\s*([0-9,\s]+)\))?\s*$")
    ledger, blocks, cur = OrderedDict(), [], None
    for line in prd_path.read_text().splitlines():
        m = hdr.match(line)
        if m:
            if cur: blocks.append(cur)
            cur = {"id": m.group(1), "title": m.group(2).strip(),
                   "deps": [d.strip() for d in (m.group(3) or "").split(",") if d.strip()],
                   "body": []}
        elif cur:
            cur["body"].append(line)
    if cur: blocks.append(cur)
    return blocks

def specs_len(body):          # count bullet lines in Specs section
    in_specs, count = False, 0
    for l in body:
        if l.strip().lower().startswith("specs"):
            in_specs = True; continue
        if in_specs and re.match(r"^\s*[-•*]", l):
            count += 1
        elif in_specs and l.strip() == "":
            continue
        elif in_specs:
            break
    return count

# ------------ main ----------------------------------------------------------

if len(sys.argv) != 2:
    sys.exit("Usage: auto_split_backlog.py PRD.md")

PRD = pathlib.Path(sys.argv[1])
BACKLOG_DIR = pathlib.Path(".backlog/tasks")
BACKLOG_DIR.mkdir(parents=True, exist_ok=True)

blocks = parse_prd(PRD)
ledger = OrderedDict()
task_idx = 0

for b in blocks:
    need_split = specs_len(b["body"]) > SPLIT_LIMIT
    if not need_split:
        task_idx += 1
        task_id = str(task_idx)
        ledger[task_id] = {"title": b["title"], "status": "TODO",
                           "deps": b["deps"], "complexity": 1}
        BACKLOG_DIR.joinpath(f"{task_id}.md").write_text(
            f"# Task {task_id} – {b['title']}\n" + "\n".join(b["body"]) + "\n")
    else:
        # split into chunks of SPLIT_LIMIT bullet lines each
        spec_lines = [l for l in b["body"] if re.match(r"^\s*[-•*]", l)]
        chunks = [list(islice(spec_lines, i, i + SPLIT_LIMIT))
                  for i in range(0, len(spec_lines), SPLIT_LIMIT)]
        parent_id = None
        for n, chunk in enumerate(chunks, 1):
            task_idx += 1
            sub_id = f"{b['id']}.{n}" if "." not in b['id'] else f"{task_idx}"
            ledger[sub_id] = {"title": f"{b['title']} (part {n})",
                              "status": "TODO", "deps": b["deps"], "complexity": 1}
            BACKLOG_DIR.joinpath(f"{sub_id}.md").write_text(
                f"# Task {sub_id} – {b['title']} (part {n})\n" +
                "Specs\n" + "\n".join(chunk) + "\n")
            if n == 1:
                parent_id = sub_id
        # mark parent as meta-done
        if parent_id:
            ledger[parent_id]["status"] = "DONE"
            ledger[parent_id]["note"]   = f"split into {', '.join([k for k in ledger if k.startswith(parent_id[:-2])])}"

# write ledger
pathlib.Path(".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
print(f"🗂️  Rebuilt backlog ({len(ledger)} tasks)")