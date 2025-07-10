#!/usr/bin/env python3
"""
Copy baseline_template contents into a new project folder.

Usage:  python tools/seed_baseline.py /path/to/target
If no path given, uses current directory.
"""
import shutil, pathlib, sys, filecmp, json

HERE      = pathlib.Path(__file__).resolve().parent
TEMPLATE  = HERE.parent      # baseline_template root
TARGET    = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

def copy_tree(src, dst):
    for item in src.iterdir():
        dst_item = dst / item.name
        if item.is_dir():
            copy_tree(item, dst_item)
        else:
            dst_item.parent.mkdir(parents=True, exist_ok=True)
            if dst_item.exists():
                # Skip identical files to avoid overwriting user edits
                if filecmp.cmp(item, dst_item, shallow=False):
                    continue
                print(f"SKIP (exists): {dst_item}")
            else:
                shutil.copy2(item, dst_item)
                print(f"COPY → {dst_item}")

def init_backlog():
    ledger = {"1": {
        "title": "Example placeholder task",
        "status": "TODO",
        "deps": [],
        "complexity": 1
    }}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2) + "\n")
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")

def main():
    copy_tree(TEMPLATE / ".cursor",   TARGET / ".cursor")
    copy_tree(TEMPLATE / ".backlog",  TARGET / ".backlog")
    copy_tree(TEMPLATE / "tools",     TARGET / "tools")
    if not (TARGET / ".backlog/tasks.json").exists():
        init_backlog()
    print("\n✅  Baseline injected.  Next step: git add . && git commit -m 'seed baseline'")

if __name__ == "__main__":
    main()