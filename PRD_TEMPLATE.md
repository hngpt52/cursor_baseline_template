<!--
===============================================================
COPY-AND-PASTE PROMPT  →  Give this block to ChatGPT / Claude
===============================================================
```prompt
You are my **product-spec assistant**.

Goal → Produce a complete **PRD.md** for the web-app “{{PROJECT_NAME}}”.
For every task, decide how many sub-tasks it should break into.
Use the marker `{split:n}` immediately after the heading when n > 1.

Workflow  
• **Phase A** – ask me for each missing detail (one concise question at a time).  
• **Phase B** – when everything is answered, output the filled markdown below.  
  Return **only** the markdown in Phase B — no commentary.

Must-ask checklist (if unknown)  
• TAGLINE  
• PRIMARY_CTA text  
• SECONDARY_CTA text  
• Extra pages? (Docs, Pricing, etc.)  
• Auth provider (default Supabase)  
• Billing provider (default Stripe)

Split-size guidance  
• ≤ 4 bullet lines → omit `{split:n}` (single task)  
• 5 – 7 lines     → `{split:2}`  
• 8 – 11 lines    → `{split:3}`  
• > 11 lines      → ask me how granular it should be

Formatting rules  
1. Use heading pattern `## <number> <title> (depends: …) {split:n?}`.  
2. Replace every `>>PLACEHOLDER<<` or `{{BRACES}}`.  
3. Do **not** invent extra sections unless clearly required.

Skeleton to fill starts now
---------------------------------------------------------------------
# {{PROJECT_NAME}} – Product Requirements

## 1 Landing page MVP
Purpose · convince visitors to start a trial  
Route · `/`  
Specs  
- Hero headline “>>TAGLINE<<”  
- Screenshot / animation of chat interface  
- Primary CTA “>>PRIMARY_CTA<<”  
- Secondary CTA “>>SECONDARY_CTA<<”

## 2 ChatShell layout (depends: 1)
Route · `/app/chat`  
Specs  
- Two-pane flex: left mentor list, right chat window  
- Mentors: Finance, Life, Science, Custom  
- Voice message recorder (<Sheet> modal)

## 3 Authentication (depends: 1)
Tech · Supabase (SSR helpers)  
Specs  
- Edge middleware redirects `/login` if no session  
- Expose `ctx.userId` to API and React hooks

## 4 Streaming responses (depends: 2,3)
Tech · Upstash Redis  
Specs  
- Redis pub/sub channel `mentor-<uid>`  
- API route `/api/mentor/stream` returns SSE

## 5 Billing page (depends: 2)
Tech · Stripe portal  
Specs  
- Show plan & usage  
- Link to portal

## 6 Dark-mode toggle (depends: 1)
Specs  
- Toggle stored in `localStorage`  
- Colours drawn from `design.tokens.json`

---------------------------------------------------------------------
(end skeleton)