#!/usr/bin/env python3
"""
seed_baseline.py  –  Copy baseline_template contents into a freshly-scaffolded project.

Run from inside your project, e.g.:
    python ../baseline_template/seed_baseline.py .

Baseline layout assumed:
baseline_template/
├─ .cursor/
│   └─ rules/
│       ├─ backlog_auto.mdc      # NEW – auto-split rule
│       └─ … other rules …
├─ .backlog/                     # stub placeholder (may be empty)
├─ backlog_gen.py                # task generator
├─ auto_split_backlog.py         # NEW – splits oversized tasks
├─ prd_sanitizer.py              # optional cleaner
├─ PRD_TEMPLATE.md
├─ THEME_TEMPLATE.json
└─ seed_baseline.py              # this file
"""

import json, pathlib, shutil, sys, filecmp

HERE     = pathlib.Path(__file__).resolve().parent   # …/baseline_template
TEMPLATE = HERE
TARGET   = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# ───────────────────────── helpers ──────────────────────────────────────────

def copy_tree(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Recursively copy src → dst, skipping identical files."""
    if not src.exists():
        return
    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            copy_tree(item, dst_item)
        else:
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            if dst_item.exists() and filecmp.cmp(item, dst_item, shallow=False):
                continue  # identical
            shutil.copy2(item, dst_item)
            print(f"COPY → {dst_item}")

def init_backlog() -> None:
    ledger = {"1": {"title": "Example placeholder task",
                    "status": "TODO", "deps": [], "complexity": 1}}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2) + "\n")
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")
    print("📄  Initial backlog seeded.")

def ensure_pkg_scripts() -> None:
    pkg = TARGET / "package.json"
    if not pkg.exists():
        print("⚠️  package.json not found – skipped script injection")
        return

    data = json.loads(pkg.read_text())
    scripts = data.setdefault("scripts", {})
    changed = False

    if "gen:backlog" not in scripts:
        scripts["gen:backlog"] = "python3 backlog_gen.py PRD.md"
        changed = True
    if "fix:prd" not in scripts and (TARGET / "prd_sanitizer.py").exists():
        scripts["fix:prd"] = "python3 prd_sanitizer.py PRD.md"
        changed = True
    if "refresh:backlog" not in scripts:
        scripts["refresh:backlog"] = "python3 auto_split_backlog.py PRD.md"
        changed = True

    if changed:
        pkg.write_text(json.dumps(data, indent=2) + "\n")
        print("📝  Added npm scripts to package.json")
    else:
        print("✓  npm scripts already present")

# ───────────────────────── main ─────────────────────────────────────────────

def main() -> None:
    print(f"🔧  Injecting baseline into: {TARGET}")

    # Copy core folders (.cursor includes backlog_auto.mdc)
    for folder in [".cursor", ".backlog"]:
        copy_tree(TEMPLATE / folder, TARGET / folder)

    # Copy standalone files (always overwrite to keep fresh)
    for fname in [
        "backlog_gen.py",
        "auto_split_backlog.py",
        "prd_sanitizer.py",
        "PRD_TEMPLATE.md",
        "THEME_TEMPLATE.json",
    ]:
        src = TEMPLATE / fname
        if src.exists():
            dst = TARGET / fname
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"COPY → {dst}")

    if not (TARGET / ".backlog/tasks.json").exists():
        init_backlog()

    ensure_pkg_scripts()
    print("\n✅  Baseline injected.  Next:\n   git add . && git commit -m 'seed baseline'")

if __name__ == "__main__":
    main()