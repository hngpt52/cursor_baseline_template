#!/usr/bin/env python3
"""
seed_baseline.py  –  copy baseline_template into a fresh repo.

Usage (run **inside** the blank project folder):
    python ../baseline_template/tools/seed_baseline.py .
"""

import json, pathlib, shutil, sys, filecmp, os

BASE   = pathlib.Path(__file__).resolve().parent          # …/baseline_template/tools
ROOT   = BASE.parent                                      # …/baseline_template
TARGET = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# ── helpers ───────────────────────────────────────────────────────────
def copy_tree(src: pathlib.Path, dst: pathlib.Path) -> None:
    if not src.exists():
        return
    for item in src.iterdir():
        d = dst / item.name
        if item.is_dir():
            copy_tree(item, d)
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            if d.exists() and filecmp.cmp(item, d, shallow=False):
                continue
            shutil.copy2(item, d)
            print(f"COPY → {d.relative_to(TARGET)}")

def init_backlog() -> None:
    ledger = {"1": {"title": "Example placeholder task",
                    "status": "TODO", "deps": [], "complexity": 1}}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")
    print("📄  Initial backlog seeded.")

def ensure_scripts() -> None:
    pkg = TARGET / "package.json"
    if not pkg.exists():
        print("ℹ️  package.json not found – skip npm-script injection")
        return
    data = json.loads(pkg.read_text()); scripts = data.setdefault("scripts", {}); changed = False
    mapping = {
        "gen:backlog":     "python3 tools/backlog_gen.py PRD.md",
        "refresh:backlog": "python3 tools/auto_split_backlog.py PRD.md",
        "fix:prd":         "python3 tools/prd_sanitizer.py PRD.md",
        "sync:tokens":     "python3 tools/gen_tailwind_from_tokens.py"
    }
    for k, v in mapping.items():
        if k not in scripts:
            scripts[k] = v; changed = True
    if changed:
        pkg.write_text(json.dumps(data, indent=2) + os.linesep)
        print("📝  npm scripts injected")
    else:
        print("✓  npm scripts already present")

# ── main ──────────────────────────────────────────────────────────────
print(f"🔧  Seeding baseline into {TARGET}")

for folder in [".cursor", ".backlog"]:
    copy_tree(ROOT / folder, TARGET / folder)

copy_tree(ROOT / "tools", TARGET / "tools")                # entire tools dir

for f in ["PRD_TEMPLATE.md", "THEME_TEMPLATE.json"]:
    shutil.copy2(ROOT / f, TARGET / f); print(f"COPY → {f}")

if not (TARGET / ".backlog/tasks.json").exists():
    init_backlog()

ensure_scripts()
print("\n✅  Baseline ready.   git add . && git commit -m 'seed baseline'")