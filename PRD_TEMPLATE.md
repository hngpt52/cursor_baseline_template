<!--
 HOW TO USE THIS TEMPLATE
 • Replace every {{…}} placeholder.
 • KEEP the “## <number> …” headings – the backlog generator converts each
   heading into a task.
 • Put any dependency list in the heading like “(depends: 2,4)”.
 • Add or delete sections as needed; the script simply numbers them in order.
 • If your project uses different back-end services (e.g. Firebase instead of
   Supabase) just describe that in the Specs bullets.
 • The agent should ADD extra sections if it sees missing pages or flows.
-->

# {{Project Name}} – Product Requirements (PRD)

**One-sentence value prop**  
{{e.g. “Helps users build personalised study plans with AI feedback.”}}

---

## 1 Landing page MVP
Purpose · {{why this page exists}}  
Route · `/` or `/marketing`  
Specs ·  
- Hero headline “{{tagline}}”  
- CTA buttons (“{{primary CTA}}”, “{{secondary CTA}}”)  
- Animation / hero illustration (Framer-Motion)  

## 2 Core dashboard *(depends: 1)*
Route · `/app`  
Specs ·  
- Sidebar (Home / Settings / Billing)  
- Greeting with user’s name  
- KPI cards bound to live data  

## 3 Auth & session management *(depends: 1)*
Route · `middleware.ts` or `firebase.ts`  
Tech · **{{Supabase / Firebase / Clerk / …}}**  
Specs ·  
- Redirect `/login` if no session  
- Expose `userId` in server context  

## 4 Chat interface *(depends: 2,3)*
Route · `/app/chat`  
Specs ·  
- Two-pane flex layout  
- Left: mentor list (Finance / Life / Custom)  
- Right: chat message thread  
- Voice message recorder (<Sheet> from shadcn/ui)  

## 5 Streaming responses *(depends: 3,4)*
Tech · **{{Upstash Redis / Firebase Realtime DB / Pusher}}**  
Specs ·  
- Real-time answer stream to client  
- Edge/function endpoint `/api/stream`  

## 6 Billing page *(depends: 2)*
Route · `/app/billing`  
Tech · **{{Stripe / Paddle / LemonSqueezy}}**  
Specs ·  
- Subscribe / cancel plan  
- Show current quota