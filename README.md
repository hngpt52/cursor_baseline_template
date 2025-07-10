# 🛠️ Baseline Template  •  Task-Master-Lite for Cursor

A zero-dependency starter kit that reproduces the **core power of Task Master**  
(file-based backlog, dependency gating, Cursor rule injection) without:

* MCP servers
* API keys
* Cloud calls

Copy / clone this template into any brand-new project, run one command, and Cursor will march through tasks *one at a time* with your visual guard-rails in place.

---

## ✨  What’s inside

baseline_template/
├─ .cursor/
│  └─ rules/
│     ├─ backlog.mdc          # 1-task loop rule  (alwaysApply)
│     ├─ chat_visual.mdc      # style guard for chat components
│     └─ ui_tokens.mdc        # enforces colour-token file (see below)
├─ .backlog/
│  ├─ tasks.json              # stub ledger with a placeholder task
│  └─ tasks/                  # kept empty – generator fills later
├─ tools/
│  ├─ backlog_gen.py          # PRD → .backlog generator (60 LOC)
│  └─ seed_baseline.py        # copies this template into any repo
├─ design_tokens.pinkgold.json# ← example colour-palette file
└─ PRD_TEMPLATE.md            # fill-in-blanks spec template         # fill-in-the-blanks spec template

---

## 🚀 Quick-start (one-liner)

```bash
# 1  Scaffold a fresh project (example: Next.js 15 with pnpm)
npx create-next-app@latest my-app --ts --tailwind --package-manager pnpm
cd my-app

# 2  Bring in the baseline
python path/to/baseline_template/tools/seed_baseline.py .

# 3  Draft your PRD
cp baseline_template/PRD_TEMPLATE.md PRD.md
#   -> fill placeholders (ChatGPT is great for this)

# 4  Generate backlog files
pnpm run gen:backlog         # runs tools/backlog_gen.py PRD.md
git add .backlog PRD.md
git commit -m "generate backlog from PRD"

# 5  Open Cursor in Auto mode → watch it execute tasks


⸻

🗂️  seed_baseline.py  — copy baseline into project

#!/usr/bin/env python3
"""Copy baseline_template content into a target repo."""
import shutil, pathlib, sys, filecmp, json

HERE      = pathlib.Path(__file__).resolve().parent
TEMPLATE  = HERE.parent              # baseline root
TARGET    = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()

def copytree(src: pathlib.Path, dst: pathlib.Path):
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
    ledger = {"1": {
        "title": "Example placeholder task",
        "status": "TODO", "deps": [], "complexity": 1}}
    (TARGET / ".backlog/tasks").mkdir(parents=True, exist_ok=True)
    (TARGET / ".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
    (TARGET / ".backlog/tasks/1.md").write_text("# Task 1 – Example\nTODO\n")

def main():
    copytree(TEMPLATE / ".cursor",  TARGET / ".cursor")
    copytree(TEMPLATE / ".backlog", TARGET / ".backlog")
    copytree(TEMPLATE / "tools",    TARGET / "tools")
    if not (TARGET / ".backlog/tasks.json").exists():
        init_backlog()
    print("\n✅ Baseline injected. Run  git add . && git commit -m 'seed baseline'")

if __name__ == "__main__":
    main()

The script skips files that already exist and differ, so it’s safe to rerun.

⸻

📄  backlog_gen.py  — PRD ➜ tasks

#!/usr/bin/env python3
"""
Convert PRD.md headings into .backlog/tasks.json + tasks/*.md.
Heading syntax:

## 3 Payment page (depends: 2)
- bullet spec line…
"""
import sys, json, re, pathlib, fileinput
from collections import OrderedDict

if len(sys.argv) != 2:
    sys.exit("Usage: backlog_gen.py PRD.md")

prd_path = pathlib.Path(sys.argv[1])
out_dir  = pathlib.Path(".backlog/tasks")
out_dir.mkdir(parents=True, exist_ok=True)

ledger = OrderedDict()
tid, title, deps, body = 0, "", [], []

def flush():
    global tid, title, deps, body
    if not title: return
    tid += 1
    (out_dir / f"{tid}.md").write_text(f"# Task {tid} – {title}\n" +
        ("\n".join(body) or "TODO") + "\n")
    ledger[str(tid)] = {"title": title, "status": "TODO",
                        "deps": deps, "complexity": 1}
    title, deps, body[:] = "", [], []

for line in prd_path.read_text().splitlines():
    h = re.match(r"^##\s+\d+\s+(.+?)(?:\s+$begin:math:text$depends:\\s*([\\d,\\s]+)$end:math:text$)?$", line)
    if h:
        flush()
        title = h.group(1).strip()
        deps  = [int(x) for x in h.group(2).split(",")] if h.group(2) else []
    else:
        body.append(line.rstrip())

flush()
pathlib.Path(".backlog/tasks.json").write_text(json.dumps(ledger, indent=2))
print(f"Generated {len(ledger)} tasks → .backlog/")

Add a script entry in your project package.json:

"scripts": { "gen:backlog": "python tools/backlog_gen.py PRD.md" }


⸻

📝  PRD_TEMPLATE.md  (fill & rename to PRD.md)

Headings (## ) become tasks.
“Depends” lists produce dependency graphs.

# {{Project Name}} – Product Requirements

## 1 Landing page
Purpose · {{value}}  
Route · `/`  
Specs:  
- Headline “{{tagline}}”  
- CTA buttons  
- Illustration

## 2 Dashboard *(depends: 1)*
Route · `/app`  
Specs:  
- Sidebar nav  
- Greeting card  

## 3 Auth *(depends: 1)*
Tech · **{{Supabase / Firebase / Clerk}}**  
Specs:  
- Redirect `/login` if no session  

## 4 Realtime stream *(depends: 2,3)*
Tech · **{{Upstash Redis / Pusher}}**  
Specs:  
- Edge function `/api/stream`


⸻

🔄  Full workflow diagram

flowchart TD
  A[create-next-app] --> B(seed_baseline.py)
  B --> C[commit baseline]
  C --> D[fill PRD.md]
  D --> E[gen:backlog]
  E --> F[commit backlog]
  F --> G[Cursor Auto loop]
  G --> H[task 1 IN_PROGRESS → DONE]
  H --> G
  G --> Z[All tasks DONE → deploy]


⸻

That’s everything needed for you and anyone on GitHub to clone the template, generate backlogs from a PRD in seconds, and let Cursor execute tasks safely.