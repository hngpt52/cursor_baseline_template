#!/usr/bin/env python3
"""
Clean a rough PRD into backlog-friendly markdown.

Usage:
    python3 tools/prd_sanitizer.py PRD.md
"""
import pathlib, re, sys, textwrap

if len(sys.argv) != 2:
    sys.exit("Usage: prd_sanitizer.py PRD.md")

path = pathlib.Path(sys.argv[1])
raw  = path.read_text().splitlines()
out  = []

for line in raw:
    # 1. Make headings start with '##'
    m = re.match(r"^\s*(\d+)\s+(.+)", line)
    if m and not line.lstrip().startswith("##"):
        line = f"## {m.group(1)} {m.group(2)}"

    # 2. Normalise bullet marks
    bullet = re.match(r"^\s*[•*]\s+", line)
    if bullet:
        line = re.sub(r"^\s*[•*]\s+", "- ", line)

    out.append(line.rstrip())

clean = "\n".join(out) + "\n"
path.write_text(clean)
print(f"✅  Sanitised → {path}")