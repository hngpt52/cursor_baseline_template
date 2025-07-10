#!/usr/bin/env python3
"""
Copy baseline_template contents into a freshly-scaffolded project.

Usage:
    python tools/seed_baseline.py [target_path]

•  If no path is given, the current directory is used.
•  Files that already exist AND differ are left untouched (printed as SKIP).
•  Adds the "gen:backlog" script to package.json if missing.
"""

import json
import pathlib
import shutil
import sys
import filecmp

HERE     = pathlib.Path(__file__).resolve().parent          # …/tools
TEMPLATE = HERE.parent                                      # baseline_template root
TARGET   = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

# ---------- helpers ----------------------------------------------------------


def copy_tree(src: pathlib.Path, dst: pathlib.Path) -> None:
    """Recursively copy src → dst without overwriting changed files."""
    if not src.exists():
        return
    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            copy_tree(item, dst_item)
        else:
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            if dst_item.exists():
                if filecmp.cmp(item, dst_item, shallow=False):
                    continue  # identical, no need to copy
                print(f"SKIP (exists) → {dst_item}")
            else:
                shutil.copy2(item, dst_item)
                print(f"COPY → {dst_item}")


def init_backlog() -> None:
    """Seed .backlog with a placeholder task if none exists."""
    ledger = {
        "1": {
            "title": "Example placeholder task",
            "status": "TODO",
            "deps": [],
            "complexity": 1,
        }
    }
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2) + "\n")
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")
    print("📄  Initial backlog seeded.")


def ensure_package_script() -> None:
    """Add scripts.gen:backlog to package.json if missing."""
    pkg_path = TARGET / "package.json"
    if not pkg_path.exists():
        print("⚠️  package.json not found – skip script injection")
        return

    data = json.loads(pkg_path.read_text())
    scripts = data.setdefault("scripts", {})
    if "gen:backlog" not in scripts:
        scripts["gen:backlog"] = "python tools/backlog_gen.py PRD.md"
        pkg_path.write_text(json.dumps(data, indent=2) + "\n")
        print("📝  Added scripts.gen:backlog to package.json")
    else:
        print("✓  scripts.gen:backlog already present")


# ---------- main flow --------------------------------------------------------


def main() -> None:
    print(f"🔧  Injecting baseline into: {TARGET}")
    copy_tree(TEMPLATE / ".cursor", TARGET / ".cursor")
    copy_tree(TEMPLATE / ".backlog", TARGET / ".backlog")
    copy_tree(TEMPLATE / "tools", TARGET / "tools")

    # Design-token files or any other top-level extras
    for extra in ["design.tokens.json", "PRD_TEMPLATE.md"]:
        copy_tree(TEMPLATE / extra, TARGET / extra)

    if not (TARGET / ".backlog/tasks.json").exists():
        init_backlog()

    ensure_package_script()
    print("\n✅  Baseline injected.  Next step:\n   git add . && git commit -m 'seed baseline'")


if __name__ == "__main__":
    main()