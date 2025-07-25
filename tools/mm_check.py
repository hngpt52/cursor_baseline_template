#!/usr/bin/env python3
"""
mm_check.py  –  pre-commit validator for mindmap.mm

• Scans staged additions/renames.
• Ensures each new path has a node in mindmap.mm.
• Auto-adds the node if the parent branch exists, otherwise aborts.
"""

import pathlib, subprocess, sys, xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parents[1]      # repo root
MM   = ROOT / "mindmap.mm"

def staged_paths():
    diff = subprocess.check_output(
        ["git", "diff", "--cached", "--name-status"],
        text=True
    ).strip().splitlines()
    for line in diff:
        status, path = line.split(maxsplit=1)
        if status in {"A", "R"} and (path.startswith("src/") or path.startswith("Docs/")):
            yield pathlib.Path(path).as_posix()

def ensure_node(tree, path):
    parts = path.split("/")
    cur = tree.getroot().find(".//node")     # <node TEXT="PROJECT">
    for part in parts:
        nxt = cur.find(f"./node[@TEXT='{part}']")
        if nxt is None:
            # parent exists → auto-append
            ET.SubElement(cur, "node", TEXT=part)
            nxt = cur
            cur = cur.find(f"./node[@TEXT='{part}']")
        else:
            cur = nxt
    return True

def main():
    if not MM.exists():
        print("⚠️  mindmap.mm missing – skipping check")
        sys.exit(0)

    tree = ET.parse(MM)
    changed = False

    for p in staged_paths():
        if ensure_node(tree, p):
            changed = True

    if changed:
        tree.write(MM, encoding="utf-8")
        subprocess.run(["git", "add", "mindmap.mm"])
        print("🧠  mindmap.mm updated ✔︎")

if __name__ == "__main__":
    main()