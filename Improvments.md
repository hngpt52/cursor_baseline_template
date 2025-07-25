1 Backlog & Task-Flow
	•	☐ Generate a “UI-polish” task for each page automatically
Rule of thumb: if a task touches JSX, create a follow-up task named Apply theme presets to <page>.
	•	☐ Fail the auto-splitter when a task is closed without touching the page folder
Prevents Cursor from marking a page “DONE” after dropping only copy.
	•	☐ Add npm run reopen:<id> helper that flips a task back to TODO and resets status in .backlog/tasks.json.

⸻

2 Cursor Rule Set
	•	☐ Uniqueness & priority audit
One file → one purpose. Remove overlapping bullets; set priorities in clear tiers (90 blockers → 70 style → 50 lint).
	•	☐ marketing_theme.mdc (priority 70)
Block merges unless every shadcn primitive in /app/(marketing) uses a preset class.
	•	☐ Global colour guard
Disallow raw Tailwind colour classes project-wide (bg-blue-500, hex codes).

⸻

3 Design-Token Pipeline
	•	☐ Keep tokens as JSON-with-comments (commentjson) → convert to strict JSON in sync:tokens.
	•	☐ Auto-generate Tailwind safelist from variant keys (cta, ghost, etc.) to avoid purging preset classes.
	•	☐ Add a unit test (pytest) that fails if any utility class in src/** isn’t derived from a token.

⸻

4 Scripts & Tooling
	•	☐ Move all helper scripts into /tools and make seed_baseline.py copy the entire folder.
	•	☐ sync:tokens
	1.	Parse design.tokens.json
	2.	Write tailwind.config.ts
	3.	Print diff summary
	•	☐ lint:tokens — CI-only script to verify every preset referenced in rules exists in the token file.
	•	☐ VS Code snippet pack → auto-complete preset classes while coding manually.

⸻

5 Developer Prompts & Docs
	•	☐ PRD template: add an explicit “UI polish” section so ChatGPT never omits the styling task.
	•	☐ Readme quick-start: call out the two-step UI flow →
npm run gen:backlog → npm run refresh:backlog (splits & reopens styling tasks).
	•	☐ Add a “Common prompts” doc with copy–paste examples for typewriter headers, SpotlightCard, DotGrid, etc.

⸻

6 Quality Gates (CI)
	•	☐ Pre-commit hook: run lint:tokens + ESLint before allowing a commit.
	•	☐ GitHub Action: block PR if any rule violation appears in the diff (use simple regex scan).

⸻

Outcome

With these points baked into the baseline you will:
	•	Prevent Cursor from prematurely closing style-heavy tasks.
	•	Guarantee that any colour, radius, or shadow used in JSX is traceable to a token.
	•	Eliminate manual rule tweaking when new scripts are added.
	•	Provide future collaborators with fool-proof docs & prompts.