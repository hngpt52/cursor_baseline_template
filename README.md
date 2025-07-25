Below is a clean, up-to-date README.md that matches the lean-baseline you just finalised (no stack templates, mind-map support, tools/ directory, etc.).
Copy-paste it over your old one.

⸻

🛠️  Baseline Template · Task-Master-Lite × Cursor

A zero-dependency starter kit that gives you

•	Structured Task-Master-style backlog (.backlog/)
•	Universal Cursor guard-rails (no vendor/build drift, one-task loop, optional design-tokens lock-in)
•	Optional mind-map validator to keep architecture & backlog in sync
•	Works 100 % offline — no MCP servers, API keys, or cloud calls

Seed the baseline into any blank repo → draft PRD.md → run pnpm run gen:backlog → open Cursor Auto-mode.
The agent will execute tasks one at a time under your guard-rails.

⸻

📁 What’s inside

baseline_template/
├─ .cursor/
│  └─ rules/
│     ├─ backlog.mdc            one-task loop
│     ├─ no-vendor.mdc          ignore build/Pods/dist
│     ├─ src_boundary.mdc       keep code inside src/ or Sources/
│     └─ design_tokens_optional.mdc
├─ .backlog/                    stub placeholder
│  ├─ tasks.json
│  └─ tasks/
├─ tools/                       language-agnostic helpers
│  ├─ seed_baseline.py
│  ├─ backlog_gen.py
│  ├─ auto_split_backlog.py
│  ├─ gen_tailwind_from_tokens.py
│  ├─ mm_check.py
│  └─ mindmap.mm
├─ PRD_TEMPLATE.md              copy → PRD.md, fill, generate tasks
└─ THEME_TEMPLATE.json          optional design-token starter

Nothing here is tech-specific — you’ll scaffold the actual app shell (Next, FastAPI, SwiftUI…) after seeding.

⸻

🚀 Quick-start

# 1  Create an empty folder & enter it
mkdir my-app && cd my-app

# 2  Seed the baseline (path relative to your repo)
python ../baseline_template/tools/seed_baseline.py .

git add . && git commit -m "seed baseline"

# 3  Draft PRD
cp PRD_TEMPLATE.md PRD.md          # fill pages & deps

# 4  Generate backlog
pnpm init -y                       # (or cargo init / go mod init …)
pnpm add -D python                 # if you need a local runtime
pnpm run gen:backlog               # = python3 tools/backlog_gen.py PRD.md
git add .backlog PRD.md && git commit -m "generate backlog"

# 5  (optional) add design tokens
cp THEME_TEMPLATE.json src/ui/design.tokens.json
# → fill colours/radii/shadows, then `pnpm run sync:tokens`

# 6  Open Cursor Auto-mode → tasks flow, rules enforced


⸻

🛡️ Rules in play (always copied)

Rule file	Enforces
.cursor/rules/backlog.mdc	Cursor must work on exactly one task at the top of .backlog/tasks.json.
.cursor/rules/no-vendor.mdc	Keeps hands off vendor/, Pods/, build/, dist/…
.cursor/rules/src_boundary.mdc	Source code must live under src/ (or Sources/ for Swift).
.cursor/rules/design_tokens_optional.mdc	If src/ui/design.tokens.json exists, all colours/fonts/radii must come from it; otherwise the rule is silent.

Add extra stack-specific rules in your repo as you wish — the baseline stays language-agnostic.

⸻

🔧 Helper scripts

Script	Purpose
seed_baseline.py	Copies .cursor/, .backlog/, tools/, PRD & token templates into the target repo and injects npm scripts if a package.json is present.
backlog_gen.py	Turns numbered ##  headings in PRD.md into .backlog/tasks.json + individual task .md files.
auto_split_backlog.py	(Optional) splits oversized tasks into smaller ones.
gen_tailwind_from_tokens.py	Converts design.tokens.json into a Tailwind 4 config (only if you use Tailwind).
mm_check.py	Pre-commit validator — ensures every new file has a matching node in mindmap.mm, and no task is marked DONE without representation in the map.

All helper scripts live in tools/ and are copied verbatim.

⸻

seed_baseline.py (full)

#!/usr/bin/env python3
"""
Copy baseline_template into a blank repo (runs offline).
Usage:  python ../baseline_template/tools/seed_baseline.py .
"""

import json, pathlib, shutil, sys, filecmp, os

BASE   = pathlib.Path(__file__).resolve().parent
ROOT   = BASE.parent            # baseline_template/
TARGET = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

def copy_tree(src: pathlib.Path, dst: pathlib.Path) -> None:
    if not src.exists(): return
    for item in src.iterdir():
        d = dst / item.name
        if item.is_dir():
            copy_tree(item, d)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            if d.exists() and filecmp.cmp(item, d, shallow=False):
                continue
            shutil.copy2(item, d)
            print("COPY →", d.relative_to(TARGET))

def init_backlog() -> None:
    ledger = {"1": {"title": "Example placeholder task",
                    "status": "TODO", "deps": [], "complexity": 1}}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")

def ensure_scripts() -> None:
    pkg = TARGET / "package.json"
    if not pkg.exists(): return
    data = json.loads(pkg.read_text()); s = data.setdefault("scripts", {}); changed = False
    mapping = {
        "gen:backlog":     "python3 tools/backlog_gen.py PRD.md",
        "refresh:backlog": "python3 tools/auto_split_backlog.py PRD.md",
        "fix:prd":         "python3 tools/prd_sanitizer.py PRD.md",
        "sync:tokens":     "python3 tools/gen_tailwind_from_tokens.py"
    }
    for k, v in mapping.items():
        if k not in s: s[k] = v; changed = True
    if changed:
        pkg.write_text(json.dumps(data, indent=2) + os.linesep)
        print("📝 npm scripts injected")

print(f"🔧 Seeding baseline into {TARGET}")
for folder in [".cursor", ".backlog"]: copy_tree(ROOT / folder, TARGET / folder)
copy_tree(ROOT / "tools", TARGET / "tools")
for f in ["PRD_TEMPLATE.md", "THEME_TEMPLATE.json"]:
    shutil.copy2(ROOT / f, TARGET / f); print("COPY →", f)
if not (TARGET / ".backlog/tasks.json").exists(): init_backlog()
ensure_scripts()
print("✅ Baseline ready – git add . && git commit -m 'seed baseline'")


⸻

Mind-map workflow (optional but recommended)
	1.	Keep a lightweight tools/mindmap.mm updated as you add folders / features.
	2.	Install the pre-commit hook:

ln -s ../../tools/mm_check.py .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

	3.	Any commit touching files without matching nodes will fail until you update the map or amend the task spec — forcing Cursor (or you) to stay honest.

⸻

Happy shipping — PRs & feedback welcome!