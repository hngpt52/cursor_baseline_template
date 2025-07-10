# 🛠️  Baseline Template · Task-Master-Lite × Cursor

A zero-dependency starter kit that gives you

* Task-Master-style backlog control  
* Locked visual theming  
* Works entirely offline — **no** MCP servers, API keys, or cloud calls.

Clone / copy this template into any fresh repo, run one command, and Cursor will execute tasks **one at a time** under your guard-rails.

---

## ✨ What’s inside

baseline_template/
├─ .cursor/
│  └─ rules/
│     ├─ backlog.mdc          one-task loop rule
│     ├─ chat_visual.mdc      chat style guard
│     └─ ui_theme.mdc         locks component lib + token file
├─ .backlog/
│  ├─ tasks.json              stub ledger with placeholder task
│  └─ tasks/                  empty – generator fills later
├─ tools/
│  ├─ seed_baseline.py        copies baseline into a new repo
│  └─ backlog_gen.py          PRD.md → .backlog generator
├─ PRD_TEMPLATE.md            fill-in-blanks project spec
└─ THEME_TEMPLATE.json        blank design-token template

design.tokens.json is not shipped here.
Each project creates it by copying & filling THEME_TEMPLATE.json
into src/ui/design.tokens.json.


🚀 Quick-start

# 1  Scaffold project (example: Next.js 15 + pnpm)
npx create-next-app@latest my-app --ts --tailwind --package-manager pnpm
cd my-app

# 2  Inject baseline
python path/to/baseline_template/tools/seed_baseline.py .
git add . && git commit -m "seed baseline"

# 3  Draft theme tokens
cp THEME_TEMPLATE.json src/ui/design.tokens.json
#   ⇢ fill colours / radii / shadows, then import in tailwind.config.ts

# 4  Draft PRD
cp PRD_TEMPLATE.md PRD.md
#   ⇢ fill pages / dependencies

# 5  Generate backlog
pnpm run gen:backlog          # runs tools/backlog_gen.py PRD.md
git add .backlog PRD.md
git commit -m "generate backlog from PRD"

# 6  Open Cursor Auto mode → watch tasks execute



🛡️ Rules in play

Rule file	Enforces
.cursor/rules/backlog.mdc	Cursor must take one task at a time from .backlog/tasks.json.
.cursor/rules/chat_visual.mdc	Prevents styling drift in src/components/chat/**.
.cursor/rules/ui_theme.mdc	Cursor must import from the chosen library (e.g. shadcn) and use only tokens in src/ui/design.tokens.json.



🔧 Helper scripts (full code below)
	•	seed_baseline.py — copies the baseline into a fresh repo and patches package.json.
	•	backlog_gen.py — converts numbered ## headings in PRD.md into backlog tasks.


## Seed_baseline.py
```python
#!/usr/bin/env python3
"""Copy baseline_template into a target repo."""

import json, pathlib, shutil, sys, filecmp

HERE      = pathlib.Path(__file__).resolve().parent
TEMPLATE  = HERE.parent
TARGET    = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

def copytree(src: pathlib.Path, dst: pathlib.Path):
    if not src.exists(): return
    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            copytree(item, dst_item)
        else:
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            if dst_item.exists() and not filecmp.cmp(item, dst_item, shallow=False):
                print(f"SKIP (exists) → {dst_item}")
            else:
                shutil.copy2(item, dst_item)
                print(f"COPY → {dst_item}")

def init_backlog():
    ledger = {"1": {"title": "Example placeholder task",
                    "status": "TODO", "deps": [], "complexity": 1}}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")

def ensure_pkg_script():
    pkg = TARGET / "package.json"
    if not pkg.exists(): return
    data = json.loads(pkg.read_text())
    data.setdefault("scripts", {})["gen:backlog"] = "python tools/backlog_gen.py PRD.md"
    pkg.write_text(json.dumps(data, indent=2))
    print("📝  scripts.gen:backlog added")

def main():
    print(f"🔧 Injecting baseline into: {TARGET}")
    for folder in [".cursor", ".backlog", "tools"]:
        copytree(TEMPLATE / folder, TARGET / folder)

    for file in ["PRD_TEMPLATE.md", "THEME_TEMPLATE.json"]:
        copytree(TEMPLATE / file, TARGET / file)

    if not (TARGET / ".backlog/tasks.json").exists():
        init_backlog()
    ensure_pkg_script()
    print("\n✅  Baseline injected. Run: git add . && git commit -m 'seed baseline'")

if __name__ == "__main__":
    main()
```

## Backlog_gen.py
```python
#!/usr/bin/env python3
"""Convert PRD.md headings → .backlog/tasks.json + tasks/*.md"""

import json, pathlib, re, sys
from collections import OrderedDict

if len(sys.argv) != 2:
    sys.exit("Usage: backlog_gen.py PRD.md")

prd  = pathlib.Path(sys.argv[1])
out  = pathlib.Path(".backlog/tasks")
out.mkdir(parents=True, exist_ok=True)

ledger, tid, title, deps, body = OrderedDict(), 0, "", [], []

def flush():
    global tid, title, deps, body
    if not title: return
    tid += 1
    (out / f"{tid}.md").write_text(f"# Task {tid} – {title}\n" +
                                   ("\n".join(body) or "TODO") + "\n")
    ledger[str(tid)] = {"title": title, "status": "TODO",
                        "deps": deps, "complexity": 1}
    title, deps, body[:] = "", [], []

for line in prd.read_text().splitlines():
    m = re.match(r"^##\s+\d+\s+(.+?)(?:\s+$begin:math:text$depends:\\s*([\\d,\\s]+)$end:math:text$)?$", line)
    if m:
        flush()
        title = m.group(1).strip()
        deps  = [int(x) for x in m.group(2).split(",")] if m.group(2) else []
    else:
        body.append(line.rstrip())

flush()
(pathlib.Path(".backlog/tasks.json")
 ).write_text(json.dumps(ledger, indent=2))
print(f"Generated {len(ledger)} tasks → .backlog/")
```


🖌️ Create src/ui/design.tokens.json
	1.	Copy THEME_TEMPLATE.json → src/ui/design.tokens.json.
	2.	Fill colours, radii, shadows, fonts, component overrides.
	3.	Import tokens in tailwind.config.ts.
	4.	ui_theme.mdc now forces Cursor to use only those tokens and the specified component library.


Happy building—fork, star, PRs welcome!