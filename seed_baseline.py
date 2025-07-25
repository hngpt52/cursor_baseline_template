#!/usr/bin/env python3
"""
seed_baseline.py – copy baseline_template into a fresh repo
and deep-copy ONE stack template.

Run from inside your project folder, e.g.
    python ../baseline_template/tools/seed_baseline.py . web-nextjs
If you omit the stack key you’ll be prompted.
"""

import json, pathlib, shutil, sys, filecmp, subprocess, textwrap

BASE   = pathlib.Path(__file__).resolve().parent       # baseline_template/tools
ROOT   = BASE.parent                                  # baseline_template/
TARGET = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
STACK  = sys.argv[2] if len(sys.argv) > 2 else None   # templates/<stack>

# ── helpers ────────────────────────────────────────────────────────────────
def ask_stack() -> str:
    stacks = [p.name for p in (ROOT / "templates").iterdir() if p.is_dir()]
    print("Available stacks:", ", ".join(stacks))
    return input("Stack key (blank = none) › ").strip()

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
            print(f"COPY  {d.relative_to(TARGET)}")

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
    for k,v in mapping.items():
        if k not in s: s[k]=v; changed=True
    if changed:
        pkg.write_text(json.dumps(data, indent=2)+"\n")
        print("📝  npm scripts injected")

def set_git_hooks() -> None:
    if not (TARGET/".git").is_dir(): return
    subprocess.run(["git","config","core.hooksPath",".githooks"],
                   cwd=TARGET, check=False)

def seed_backlog() -> None:
    (TARGET/".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET/".backlog/tasks.json").write_text(
        json.dumps({"1":{"title":"Placeholder","status":"TODO","deps":[],"complexity":1}},indent=2)+"\n")
    (TARGET/".backlog/tasks/1.md").write_text("# Task 1 – Placeholder\nTODO\n")

# ── main ───────────────────────────────────────────────────────────────────
if not STACK:
    STACK = ask_stack() or ""          # empty string means “no tech template”

print(f"🔧  Seeding baseline into {TARGET}  (stack = '{STACK or 'none'}')")

# 1. core folders / tools
for folder in [".cursor",".backlog"]:
    copy_tree(ROOT / folder, TARGET / folder)
copy_tree(ROOT / "tools", TARGET / "tools")

# 2. optional stack template
tpl_dir = ROOT / "templates" / STACK if STACK else None
if tpl_dir and tpl_dir.exists():
    copy_tree(tpl_dir, TARGET)
elif STACK:
    sys.exit(f"❌  Unknown stack: {STACK}")

# 3. top-level shared templates
for f in ["PRD_TEMPLATE.md","THEME_TEMPLATE.json"]:
    shutil.copy2(ROOT/f, TARGET/f); print(f"COPY  {f}")

# 4. init backlog if new
if not (TARGET/".backlog/tasks.json").exists():
    seed_backlog()

ensure_scripts()
set_git_hooks()

print(textwrap.dedent("""
    ✅  Baseline seeded — next:
      git add . && git commit -m 'seed baseline'
      # then: pnpm run gen:backlog   (after writing PRD.md)
"""))