# CaterIQ — Project 1: Platform Foundation + Search-Based AI

> **Course:** Artificial Intelligence (semester project)
> **Covers course weeks:** 1 – 7 (Labs 01–07), assessed as **Project 1**
> **Product working name:** CaterIQ (placeholder, rename anytime)
> **Document audience:** developers *and* non-technical readers. Every section starts with a plain-English explanation ("In simple words") followed by technical detail.

---

## Table of Contents

1. [What is this project, in simple words](#1-what-is-this-project-in-simple-words)
2. [Why this product (the market reasoning, honestly stated)](#2-why-this-product)
3. [Glossary](#3-glossary)
4. [Goals, non-goals, and priorities](#4-goals-non-goals-and-priorities)
5. [Users and roles](#5-users-and-roles)
6. [System architecture](#6-system-architecture)
7. [Technology stack and why](#7-technology-stack-and-why)
8. [Repository structure](#8-repository-structure)
9. [Data model](#9-data-model)
10. [Security and multi-tenancy](#10-security-and-multi-tenancy)
11. [Product features (the "normal app" part)](#11-product-features)
12. [AI engine (the "course" part)](#12-ai-engine)
13. [Benchmark page](#13-benchmark-page)
14. [API reference (summary)](#14-api-reference-summary)
15. [Testing strategy](#15-testing-strategy)
16. [CI/CD and deployment](#16-cicd-and-deployment)
17. [Week-by-week plan](#17-week-by-week-plan)
18. [Acceptance criteria and definition of done](#18-acceptance-criteria-and-definition-of-done)
19. [Risks and mitigations](#19-risks-and-mitigations)
20. [Demo script and report outline](#20-demo-script-and-report-outline)
21. [Handoff to Project 2](#21-handoff-to-project-2)

---

## 1. What is this project, in simple words

A **caterer** is a business that prepares food for events: office lunches, weddings, parties. Running that business involves a lot of paperwork: building menus, sending price quotes, collecting deposits, tracking which event is on which day, and working out whether each event actually made money.

**CaterIQ** is a web and phone-friendly app that does all of that in one place. On top of the everyday tools, it adds *AI helpers* that solve real catering problems:

| Real-life problem | AI helper (course topic) |
|---|---|
| "A guest is allergic to peanuts. What's the smallest change to this dish that makes it safe?" | Allergen substitution finder (Breadth-First Search) |
| "Build me a 3-course package for 80 guests under $40 a head that includes vegetarian and gluten-free options." | Menu constraint solver (Depth-First Search) |
| "Which combination of dishes gives the best value for this budget?" and "What's the fastest delivery route?" | Menu optimizer and route planner (Greedy Best-First and A*) |
| "A rival caterer is bidding too. What price should I quote?" | Bid pricing advisor (Minimax with Alpha-Beta pruning) |

**Project 1 delivers:** a working, deployed app with the everyday catering tools **plus** the four search-based AI helpers above, with tests and a page that compares how the algorithms perform.

**Project 2 (separate document)** adds the learning-based helpers: scheduling, customer grouping, forecasting, prediction and neural networks.

---

## 2. Why this product

*In simple words:* we did market research before choosing the idea. The honest result is that **no catering software niche is completely empty**, so we are not claiming a "gap in the market". We are building a product that is **better in specific, documented ways**.

### What the research found (summary)

- Catering software already exists in many forms (Caterease, Better Cater, CaterZen, Flex Catering, Curate, Total Party Planner, Perfect Venue and others).
- The older tool **Caterease** is widely described by reviewers as dated and clunky, with a monthly price plus per-user fees and a setup fee.
- The cheap, well-liked tool **Better Cater** has a very high review score, but its reviewers repeatedly ask for things it lacks.

### The user complaints CaterIQ targets

| Complaint reported by users of existing tools | CaterIQ response |
|---|---|
| No way to accept credit cards inside the tool | Stripe card payments, deposits and balance invoices (feature F7) |
| Weak reporting (no event counts for a date range, no profit view) | Reporting module with profit per event (feature F8) |
| No mobile app and poor calendar sync | Installable PWA + live calendar feed (features F6, F9) |
| Separate logins needed for each location | One account, many locations (feature F2) |
| Menu building is manual and time-consuming | AI helpers (Section 12) |

### Honest limitations

- Delivery routing already exists in several competitors, so in CaterIQ the A* route planner is a **course module**, not our selling point.
- Our selling points are payments, reporting, mobile/calendar and the AI menu tools.
- This is a student project: we will not claim to have validated paying customers.

---

## 3. Glossary

| Term | Plain meaning |
|---|---|
| **Caterer** | A business that prepares food for events. |
| **Tenant / Organization** | One caterer's company account. Their data is invisible to other companies. |
| **Multi-tenant** | One running app serves many companies, each isolated from the others. |
| **Proposal** | A priced offer sent to a client before they book. |
| **Deposit** | Part of the price paid in advance to confirm a booking. |
| **PWA (Progressive Web App)** | A website that can be installed on a phone like an app. |
| **API** | The set of web addresses the front end calls to read and write data. |
| **Migration** | A versioned script that changes the database structure safely. |
| **Webhook** | A message Stripe sends to our server when a payment happens. |
| **iCal feed** | A calendar link that Google/Apple Calendar can subscribe to. |
| **State** (search) | One snapshot of the problem, e.g. "the dish with these ingredients". |
| **Action** | A move from one state to another, e.g. "swap butter for olive oil". |
| **Goal test** | A yes/no check that a state solves the problem. |
| **BFS** | Breadth-First Search: explores all 1-step options, then all 2-step options, etc. Finds the fewest steps. |
| **DFS** | Depth-First Search: follows one path as deep as it goes, backs up when stuck. |
| **Heuristic** | An educated guess of how far a state is from the goal. |
| **Greedy Best-First** | Always expands the state that *looks* closest to the goal. Fast but not always optimal. |
| **A\*** | Expands states using (cost so far + estimated cost remaining). Optimal if the estimate never over-guesses (admissible). |
| **Minimax** | Decision method for two opposing players: you maximize your result assuming the opponent minimizes it. |
| **Alpha-Beta pruning** | A speed-up for minimax that skips branches that cannot change the answer. |
| **Admissible heuristic** | A heuristic that never overestimates the true remaining cost. |

---

## 4. Goals, non-goals, and priorities

### 4.1 Goals

1. A deployed, secure, multi-tenant catering web app usable on desktop and phone.
2. Four search-based AI modules, each implemented as clean, tested Python and exposed through the app.
3. A benchmark page that **measures** (not just claims) how the algorithms compare.
4. A codebase another developer can run in under 10 minutes using Docker.

### 4.2 Non-goals for Project 1

- Machine learning, scheduling and forecasting (Project 2).
- Native iOS/Android apps (the PWA covers mobile).
- Accounting integrations (QuickBooks/Xero), recipe costing, staff payroll.
- Real marketplace delivery-driver integrations.
- Real customers or real payment processing in live mode (we use Stripe **test mode**).

### 4.3 Priority levels (MoSCoW) — use this to cut scope safely

| Priority | Items |
|---|---|
| **Must have** | Auth + roles, multi-tenancy, menu/client/event CRUD, event calendar, all four AI modules, benchmark page, tests, CI, deployment |
| **Should have** | PDF proposals, Stripe test-mode deposits, profit report, iCal feed |
| **Could have** | PWA offline mode, multi-location switcher, audit log UI |
| **Won't have** | Native apps, live-mode payments, accounting sync |

> If time runs short, cut from the bottom of the list upward. The AI modules are what the course grades, so they are protected.

---

## 5. Users and roles

| Role | Who | Can do |
|---|---|---|
| **Owner** | The caterer who owns the account | Everything, including billing, users, reports |
| **Manager** | A senior staff member | Create/edit events, menus, proposals; view reports; cannot manage owners |
| **Staff** | Kitchen/office staff | View events and menus; limited edits |
| **Driver** | Delivery person | View only the deliveries assigned to them |
| **Client (external, view-only)** | The person ordering the event | Opens a proposal link, approves it, pays a deposit. Does **not** need an account. |

**Access rule (in simple words):** you can only ever see data that belongs to *your* company, and within it only what your role allows.

---

## 6. System architecture

### 6.1 Big picture

```
 ┌───────────────┐        HTTPS         ┌──────────────────────┐
 │  Browser /    │ ───────────────────► │   Next.js frontend   │
 │  Phone (PWA)  │ ◄─────────────────── │   (UI, forms, charts)│
 └───────────────┘                      └──────────┬───────────┘
                                                   │ REST/JSON
                                                   ▼
                                        ┌──────────────────────┐
   Stripe  ◄── webhooks / checkout ───► │    FastAPI backend   │
   Calendar apps ◄── iCal feed ───────  │  (auth, business     │
                                        │   logic, validation) │
                                        └───────┬───────┬──────┘
                                                │       │ imports
                                                ▼       ▼
                                      ┌──────────────┐ ┌────────────────┐
                                      │ PostgreSQL   │ │  ai_engine     │
                                      │ (all data)   │ │  (pure Python, │
                                      └──────────────┘ │  no web code)  │
                                                       └────────────────┘
```

### 6.2 Key design decision: the AI engine is separate

*In simple words:* the AI algorithms live in their own folder that knows nothing about web pages or databases. They take plain inputs and return plain outputs. This means:

- they can be **tested alone** (fast, reliable),
- they can be **reused in Project 2**,
- you can **explain them in your report** without drowning in web code,
- they map cleanly to the **course labs**.

### 6.3 Request flow example (allergen finder)

1. Staff clicks "Make this dish nut-free" in the UI.
2. Frontend calls `POST /api/v1/ai/allergen-substitution`.
3. Backend checks login and role, loads the dish's ingredients and the substitution rules from the database.
4. Backend converts them to plain Python objects and calls `ai_engine.search.bfs_substitution(...)`.
5. The engine returns the shortest swap chain plus statistics (nodes explored).
6. Backend returns JSON; the UI shows "Swap almond flour → oat flour (1 change)".

---

## 7. Technology stack and why

| Layer | Choice | Why (beginner-friendly reasoning) |
|---|---|---|
| Language (backend + AI) | **Python 3.12** | The course is in Python. One language for app and AI. |
| Web framework | **FastAPI** | Modern, auto-generates API docs, strong typing with Pydantic. |
| Database | **PostgreSQL** | Industry standard, relational, free on most hosts. |
| ORM + migrations | **SQLAlchemy 2 + Alembic** | Safe schema changes over time; standard in production Python. |
| Frontend | **Next.js (React) + TypeScript + Tailwind** | Popular, installable as PWA, fast to build good-looking UI. |
| Auth | **JWT access + refresh tokens** (or a hosted provider such as Supabase Auth if time-boxed) | Never hand-roll password security. Use well-tested libraries. |
| Payments | **Stripe Checkout (test mode)** | Hosted payment page: we never touch card numbers. |
| PDFs | **WeasyPrint** or **ReportLab** | Generate proposal/invoice PDFs from HTML templates. |
| Testing | **pytest, pytest-cov, Playwright (optional e2e)** | Unit tests for AI, API tests for backend. |
| Code quality | **ruff, mypy, pre-commit** | Catches errors before they reach the repo. |
| Containers | **Docker + Docker Compose** | "Works on my machine" becomes "works on every machine". |
| CI | **GitHub Actions** | Runs tests automatically on every push. |
| Hosting | **Render or Fly.io** (backend + DB), **Vercel** (frontend) | Free/cheap tiers suitable for a student project. |

---

## 8. Repository structure

```
cateriq/
├── README.md                    # how to run, in 10 minutes
├── docker-compose.yml
├── .github/workflows/ci.yml
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── core/                # config, security, dependencies
│   │   ├── models/              # SQLAlchemy tables
│   │   ├── schemas/             # Pydantic request/response shapes
│   │   ├── routers/             # auth, menu, clients, events, payments, reports, ai
│   │   ├── services/            # business logic (pricing, proposals, payments)
│   │   └── tests/
│   ├── alembic/                 # database migrations
│   └── pyproject.toml
├── ai_engine/                   # PURE PYTHON, no FastAPI / DB imports
│   ├── search/
│   │   ├── core.py              # Node, Problem base class, result stats
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── greedy.py
│   │   ├── astar.py
│   │   └── adversarial.py       # minimax + alpha-beta
│   ├── problems/
│   │   ├── allergen_substitution.py
│   │   ├── menu_constraints.py
│   │   ├── menu_optimizer.py
│   │   ├── delivery_routing.py
│   │   └── bid_pricing.py
│   ├── benchmarks/runner.py
│   └── tests/
├── frontend/
│   ├── app/ (pages), components/, lib/api.ts, public/manifest.json
└── docs/
    ├── architecture.md
    └── algorithms.md
```

---

## 9. Data model

*In simple words:* the database is a set of linked tables. Almost every table carries an `organization_id`, which is how we keep each company's data separate.

### 9.1 Core tables

**organizations** — one row per catering company
`id, name, created_at, stripe_customer_id (nullable)`

**locations** — a company's kitchens/branches
`id, organization_id, name, address, latitude, longitude`

**users**
`id, email (unique), password_hash, full_name, is_active, created_at`

**memberships** — links a user to an organization with a role
`id, user_id, organization_id, role (owner|manager|staff|driver), location_id (nullable = all locations)`

**clients** — customers who order events
`id, organization_id, name, email, phone, company_name, notes, created_at`

### 9.2 Menu tables

**ingredients**
`id, organization_id, name, unit, cost_per_unit`

**allergens**
`id, name` (e.g. peanut, gluten, dairy, shellfish) — shared reference list

**ingredient_allergens** — which allergens an ingredient contains
`ingredient_id, allergen_id`

**ingredient_substitutions** — allowed swaps used by the BFS module
`id, organization_id, from_ingredient_id, to_ingredient_id, swap_cost, notes`

**menu_items** — dishes
`id, organization_id, name, category (starter|main|dessert|drink|side), description, price_per_head, cost_per_head, is_vegetarian, is_vegan, is_halal, popularity_score (0–1), is_active`

**menu_item_ingredients**
`menu_item_id, ingredient_id, quantity`

**packages** — saved menu bundles (e.g. "Corporate Lunch Classic")
`id, organization_id, name, price_per_head`

**package_items**
`package_id, menu_item_id`

### 9.3 Event and money tables

**events**
`id, organization_id, location_id, client_id, title, event_date, start_time, end_time, venue_address, venue_latitude, venue_longitude, headcount, status (lead|proposed|confirmed|completed|cancelled), notes`

**event_items** — what is being served at this event
`event_id, menu_item_id, quantity, unit_price, unit_cost`

**proposals**
`id, event_id, version, total_amount, deposit_percent, public_token, status (draft|sent|approved|declined), pdf_path, sent_at, approved_at`

**invoices**
`id, event_id, kind (deposit|balance|full), amount, due_date, status (unpaid|paid|void)`

**payments**
`id, invoice_id, stripe_payment_intent_id, amount, currency, status, paid_at, raw_event_id` *(unique raw_event_id prevents double-processing a webhook)*

### 9.4 Support tables

**calendar_tokens** — secret tokens for private calendar feeds
`id, organization_id, token (unique, random), created_at`

**travel_times** — distances between named places (used by A* routing)
`id, organization_id, from_place, to_place, minutes, latitude/longitude helper columns`

**audit_log** — who changed what
`id, organization_id, user_id, action, entity, entity_id, timestamp, details_json`

**ai_runs** — saved results of AI calls (also feeds the benchmark page)
`id, organization_id, module, params_json, nodes_expanded, runtime_ms, result_json, created_at`

### 9.5 Rules enforced by the database

- Foreign keys everywhere; deletes are soft (`is_active`/`status`) for money-related records.
- Unique constraints: user email, proposal public token, Stripe event id.
- Indexes on `(organization_id, event_date)` for fast calendar queries.

---

## 10. Security and multi-tenancy

*In simple words:* it must be impossible for Caterer A to see Caterer B's data, even by guessing web addresses.

| Concern | Control |
|---|---|
| Tenant isolation | Every query is filtered by the caller's `organization_id`. A shared dependency injects it; routes never accept `organization_id` from the client. |
| Passwords | Hashed with **argon2** or **bcrypt**. Never stored or logged in plain text. |
| Sessions | Short-lived access tokens; refresh tokens stored securely; logout invalidates refresh. |
| Roles | A permission check dependency (`require_role("manager")`) on every protected route. |
| Payments | Card data never reaches our server (Stripe Checkout). Webhooks verify Stripe's **signature** and are **idempotent**. |
| Public proposal links | Random, unguessable tokens; read-only plus approve/pay actions only. |
| Input validation | Pydantic schemas on every request. |
| Secrets | Environment variables only; `.env` is git-ignored; no keys in the repo. |
| Rate limiting | Login and public-link endpoints limited. |
| Dependencies | Dependabot or `pip-audit` in CI. |
| Tests | A dedicated "tenant isolation" test suite: user from Org A requests Org B's IDs and must get 404/403. |

---

## 11. Product features

Each feature lists: what it does in simple words, then the technical requirement.

### F1 — Authentication and accounts
**Simple:** people sign up, log in, and the first person becomes the Owner.
**Technical:** register/login/refresh/logout endpoints; email uniqueness; password rules; membership creation; invitation flow for staff (invite link or owner-created accounts).
**Done when:** login works, protected routes reject anonymous calls, role checks tested.

### F2 — Organizations and locations (multi-location)
**Simple:** a caterer with two kitchens uses one login and switches between them.
**Technical:** `locations` CRUD; a location switcher in the UI; staff memberships can be restricted to one location; reports can filter by location.
**Priority:** Could (the data model supports it from day one).

### F3 — Menu management
**Simple:** build a library of dishes with prices, ingredients, dietary tags, and group them into packages.
**Technical:** CRUD for menu items, ingredients, packages; dietary flags; ingredient-to-allergen links; validation that price and cost are non-negative; CSV import for bulk upload (Should).

### F4 — Clients (a lightweight CRM)
**Simple:** a contact list that remembers every event a client has ordered.
**Technical:** CRUD, search by name/email/company, client detail page listing events and total spend.

### F5 — Events and event builder
**Simple:** create an event (date, place, headcount), attach dishes, see totals update instantly.
**Technical:** event lifecycle `lead → proposed → confirmed → completed` (or cancelled); line items with quantity × unit price; server-side total calculation (never trust the browser's total); double-booking warning if the same location has overlapping events.

### F6 — Calendar and calendar sync
**Simple:** see all events in a month/week view, and subscribe from Google or Apple Calendar so events appear on your phone.
**Technical:** calendar page (month/week/day); iCal (`.ics`) feed at `/calendar/{token}.ics` per organization (and optionally per location); regenerating the token revokes access.
*Limitation stated honestly:* the feed is one-way (CaterIQ → your calendar). Two-way Google sync is out of scope.

### F7 — Proposals, deposits, and payments
**Simple:** send the client a professional PDF/online proposal; the client clicks "Approve & pay deposit"; the money arrives and the event becomes confirmed automatically.
**Technical flow:**

1. Manager clicks **Generate proposal** → server builds a versioned proposal and a PDF.
2. Client opens the public link (token) → sees the proposal → clicks **Approve**.
3. Server creates a **deposit invoice** and a Stripe Checkout Session → redirects client.
4. Stripe calls our **webhook** (`checkout.session.completed`) → server verifies the signature → marks invoice paid → sets event to `confirmed` → records a payment row.
5. Balance invoice is created automatically, due N days before the event.

**Edge cases to handle:** duplicate webhooks (idempotency), failed/abandoned checkout (invoice stays unpaid), proposal edited after sending (new version, old link shows "superseded").
**Mode:** Stripe **test mode only** for the course.

### F8 — Reporting (a direct answer to user complaints)
**Simple:** answer "how many events did we do last quarter?" and "which events made money?" in two clicks.
**Technical reports:**

| Report | Definition |
|---|---|
| Events in period | Count of events by status within a date range, per location |
| Revenue | Sum of paid invoices in range |
| Profit per event | (sum of `unit_price × qty`) − (sum of `unit_cost × qty`) |
| Margin % | profit ÷ revenue |
| Revenue by client | Total paid per client, ranked |
| Outstanding balances | Unpaid invoices with age buckets (0–30, 31–60, 60+ days) |

Each report supports date filters and **CSV export**.

### F9 — Mobile experience (PWA)
**Simple:** open the site on a phone, tap "Add to Home Screen", and it behaves like an app.
**Technical:** web manifest, icons, service worker caching the app shell and today's/this week's events for offline viewing; responsive layouts tested at phone width; Lighthouse PWA check passes.

### F10 — Audit log (Could)
Records who created/edited/deleted key records; viewable by Owners.

---

## 12. AI engine

*In simple words:* each AI helper is a "search problem". We describe the problem as: **where do we start, what moves are allowed, how do we know we're done, and what does each move cost.** Then a general algorithm explores moves until it finds an answer.

### 12.0 Shared framework (`ai_engine/search/core.py`)

```python
class Problem:
    def initial_state(self): ...
    def actions(self, state): ...          # list of possible moves
    def result(self, state, action): ...   # the new state after a move
    def is_goal(self, state) -> bool: ...
    def step_cost(self, state, action, next_state) -> float: ...
    def heuristic(self, state) -> float: ...   # optional, used by greedy/A*

@dataclass
class SearchResult:
    solution_path: list | None   # states or actions leading to the goal
    total_cost: float | None
    nodes_expanded: int
    nodes_generated: int
    max_frontier_size: int
    runtime_ms: float
    found: bool
```

Every algorithm returns a `SearchResult`, so the benchmark page can compare them fairly.

**Course concepts used here:** Python functions, tuples, sets, dictionaries (states are hashable tuples/frozensets; visited sets are Python `set`s; graphs are dicts), loops, queues and stacks (Weeks 1–3).

---

### 12.1 Module A — Allergen Substitution Finder (BFS) — Week 4

**Simple:** a guest is allergic to peanuts, but the dish contains satay sauce. Find the **fewest ingredient swaps** that make the dish safe.

**Problem definition**

| Element | Definition |
|---|---|
| State | The dish's current ingredient set (frozenset of ingredient IDs) |
| Initial state | The original recipe |
| Actions | Replace one ingredient with an allowed substitute from `ingredient_substitutions` |
| Goal test | No ingredient in the set contains any of the guest's allergens |
| Step cost | 1 per swap (BFS minimizes the *number* of swaps) |

**Algorithm (BFS)**

```
frontier = queue([initial])
visited = {initial}
while frontier:
    state = frontier.popleft()
    if is_goal(state): return path to state
    for each action in actions(state):
        child = result(state, action)
        if child not in visited:
            visited.add(child); frontier.append(child)
return "no safe version exists"
```

**Why BFS fits:** it explores 1-swap options, then 2-swap options, so the first solution found has the **fewest swaps**. Complexity: O(b^d) time and memory, where b is options per step and d is the swap depth. Fine here because dishes have few ingredients and swaps are limited (cap depth at 4).

**Edge cases:** no safe version exists (return a clear message); a substitute that introduces *another* allergen (the goal test checks all of the guest's allergens); cycles (visited set).
**UI:** event page → "Dietary check" → pick allergen(s) → see the suggested swaps and a before/after ingredient list.
**Tests:** known tiny graph with a known shortest path; no-solution case; cycle case; two allergens at once.

---

### 12.2 Module B — Menu Constraint Solver (DFS with backtracking) — Week 5

**Simple:** "Build a package for 80 guests, 3 courses, under $40/head, with at least one vegetarian and one gluten-free option." The solver tries combinations and backs up when a choice breaks a rule.

**Problem definition**

| Element | Definition |
|---|---|
| State | A partial package (list of chosen dishes, one slot filled at a time) |
| Initial state | Empty package |
| Actions | Pick a dish for the next unfilled slot (starter, main, dessert, ...) |
| Goal test | All slots filled **and** all constraints satisfied |
| Constraints | Total price per head ≤ budget; ≥ N vegetarian items; gluten-free coverage; no duplicate dish; excluded allergens absent |

**Algorithm (recursive DFS / backtracking)**

```
def solve(partial, slots):
    if not slots: return partial if all_constraints_ok(partial) else None
    for dish in candidates(slots[0]):
        if violates_hard_constraints(partial + [dish]):   # prune early
            continue
        result = solve(partial + [dish], slots[1:])
        if result: return result
    return None
```

**Improvements to implement and measure:** early pruning (reject as soon as the running price exceeds the budget), and candidate ordering (try cheaper or more popular dishes first). The benchmark page compares "plain DFS" against "DFS with pruning".
**Variation:** return the first *k* valid packages so the caterer can choose.
**Complexity:** worst case O(m^s) for m dishes per slot and s slots; pruning cuts it drastically in practice.
**Why DFS fits:** the solution is found at a fixed depth (all slots filled), memory is tiny (one path), and backtracking is natural.
**Tests:** a case with exactly one valid answer; an impossible case (budget too low) returning `None`; pruning gives the same answers as no pruning but with fewer nodes.

---

### 12.3 Module C — Menu Optimizer (A\*) and Route Planner (Greedy vs A\*) — Week 6

#### C1. Menu optimizer (A\*)

**Simple:** among all valid packages, find the **best-value** one: lowest cost with highest guest appeal.

| Element | Definition |
|---|---|
| State | (slot index, chosen dishes so far) |
| Step cost g | For a chosen dish: `price_per_head + λ × (1 − popularity_score)`; λ is an adjustable "appeal weight" |
| Heuristic h | Sum, over the remaining slots, of the **cheapest possible step cost** in that slot |
| Goal | All slots filled, constraints satisfied |

**Admissibility proof (put this in your report):** `h` assumes each remaining slot gets its single cheapest option. The real remaining cost can never be lower than that, so `h` never overestimates → A\* is guaranteed optimal.

#### C2. Delivery route planner (Greedy Best-First vs A\*)

**Simple:** find the quickest way for the van to get from the kitchen to the venue; compare a fast-but-sometimes-wrong method against a guaranteed-best method.

| Element | Definition |
|---|---|
| State | A location (node) in a road graph |
| Actions | Drive to a neighboring location |
| Step cost | Travel minutes from `travel_times` |
| Heuristic | Straight-line (haversine) distance to the destination converted to minutes at the maximum plausible speed |

- **Greedy Best-First:** expands the node with the smallest `h` only. Very fast, may return a longer route.
- **A\*:** expands by `g + h`. Returns the shortest route when `h` is admissible.

**Multi-stop deliveries:** order stops with a nearest-neighbor pass and compute each leg with A\*. State clearly that this is a simplified heuristic, not an optimal tour solver.
**Honest note:** we use stored or calculated travel times, not live traffic. Real routing services are out of scope.
**Tests:** a hand-built graph where greedy returns a longer path than A\*; consistency check that A\*'s cost is never worse than greedy's; heuristic admissibility test (h ≤ true cost on sample nodes).

---

### 12.4 Module D — Bid Pricing Advisor (Minimax + Alpha-Beta) — Week 7

**Simple:** two caterers are competing for the same event. If you price too high you lose the job; too low and you earn little. Minimax picks the price that gives the **best worst-case result**. Alpha-beta pruning makes it faster by skipping options that can't matter.

**Honest scope:** this is a *simplified game model*. It illustrates adversarial search; it does not predict real competitor behavior. Say so in the report.

**Game definition**

| Element | Definition |
|---|---|
| Players | MAX = our caterer; MIN = competitor (assumed to act against us) |
| Moves | Each player, in turn, chooses a price level from a small set (e.g. −10%, −5%, 0, +5%, +10% around the base price) |
| Rounds | Up to 3 rounds (offer, counter, final) |
| Client rule | The client picks the lower price, but a quality bonus (rating) can offset a small price difference |
| Terminal payoff for us | If we win: `(our price − our cost) × headcount`; if we lose: 0 |
| Competitor payoff | Mirror image (zero-sum approximation) |

**Algorithm (with pruning)**

```
def alphabeta(state, depth, alpha, beta, maximizing):
    if depth == 0 or is_terminal(state): return payoff(state)
    if maximizing:
        best = -inf
        for move in moves(state):
            best = max(best, alphabeta(next(state, move), depth-1, alpha, beta, False))
            alpha = max(alpha, best)
            if alpha >= beta: break      # prune
        return best
    else:
        best = +inf
        for move in moves(state):
            best = min(best, alphabeta(next(state, move), depth-1, alpha, beta, True))
            beta = min(beta, best)
            if alpha >= beta: break      # prune
        return best
```

**Outputs:** recommended price, expected margin, a game-tree summary (and "nodes explored: minimax vs alpha-beta").
**Key property to test:** minimax and alpha-beta must return the **same value**; alpha-beta must expand **fewer or equal** nodes.
**UI:** proposal page → "Pricing advisor" → enter our cost, an estimated competitor price range → see the recommendation and a simple tree diagram.

---

## 13. Benchmark page

**Simple:** a page that proves the algorithms behave as theory says, with real numbers.

| Comparison | Metrics shown |
|---|---|
| BFS vs DFS (allergen/menu problems of growing size) | nodes expanded, runtime, solution depth, memory (max frontier) |
| DFS plain vs DFS with pruning | nodes expanded |
| Greedy vs A\* (routes) | path cost, nodes expanded, runtime |
| Minimax vs Alpha-Beta | nodes evaluated, pruned count, same-value check |

**Implementation:** `ai_engine/benchmarks/runner.py` generates problems of increasing size with a fixed random seed, runs each algorithm, and stores results (`ai_runs`). The frontend shows tables and charts. A button re-runs the benchmark.
**Report value:** this page is your evidence section.

---

## 14. API reference (summary)

Base path: `/api/v1`. All routes except auth, health and public proposal links require a valid token.

| Area | Endpoints |
|---|---|
| Auth | `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `GET /auth/me` |
| Org/Locations | `GET/POST /locations`, `PATCH/DELETE /locations/{id}` |
| Menu | `GET/POST /menu-items`, `PATCH/DELETE /menu-items/{id}`, same for `/ingredients`, `/packages` |
| Clients | `GET/POST /clients`, `GET/PATCH /clients/{id}` |
| Events | `GET/POST /events`, `GET/PATCH /events/{id}`, `POST /events/{id}/items`, `POST /events/{id}/status` |
| Calendar | `GET /calendar/events?from=&to=`, `GET /calendar/{token}.ics`, `POST /calendar/token/rotate` |
| Proposals | `POST /events/{id}/proposals`, `GET /proposals/{id}/pdf`, public: `GET /p/{token}`, `POST /p/{token}/approve` |
| Payments | `POST /invoices/{id}/checkout`, `POST /webhooks/stripe` |
| Reports | `GET /reports/events`, `/reports/revenue`, `/reports/profit`, `/reports/outstanding` (+ `?format=csv`) |
| AI | `POST /ai/allergen-substitution`, `/ai/menu-solve`, `/ai/menu-optimize`, `/ai/route-plan`, `/ai/bid-advice`, `GET/POST /ai/benchmarks` |
| System | `GET /health` |

The interactive docs are auto-generated by FastAPI at `/docs`.

---

## 15. Testing strategy

| Level | What | Tool | Target |
|---|---|---|---|
| Unit — AI engine | Each algorithm on tiny hand-checkable inputs, plus property tests (e.g. A\* ≤ greedy cost, alpha-beta = minimax value) | pytest | ≥ 90% line coverage of `ai_engine` |
| Unit — services | Price totals, profit calc, proposal versioning | pytest | ≥ 80% |
| API | Every route: success, validation error, unauthorized, wrong role | pytest + FastAPI TestClient | All routes covered |
| Security | Tenant isolation, webhook signature rejection, token expiry | pytest | Must pass |
| Payments | Webhook replay is idempotent; unpaid invoice stays unpaid | pytest with Stripe test fixtures | Must pass |
| End-to-end (optional) | Login → create event → generate proposal → approve | Playwright | 1–2 happy-path flows |
| Non-functional | Lighthouse PWA score; API p95 latency on sample data | Lighthouse, simple load script | Documented |

**Rule:** no pull request merges unless CI is green.

---

## 16. CI/CD and deployment

**Continuous integration (GitHub Actions) on every push:**

1. Install dependencies (cached)
2. `ruff` lint + `mypy` type check
3. `pytest` with coverage report
4. Frontend lint + type check + build
5. Build Docker images

**Local development:** `docker compose up` starts Postgres, backend and frontend; a seed script loads demo data (menu, ingredients, substitutions, sample events).

**Deployment:**

- Backend + Postgres on Render or Fly.io; frontend on Vercel.
- Environment variables: `DATABASE_URL`, `JWT_SECRET`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `FRONTEND_URL`.
- Migrations run automatically on deploy (`alembic upgrade head`).
- A `/health` endpoint is used for uptime checks.
- Stripe webhook URL points to the deployed backend (test mode).

---

## 17. Week-by-week plan

The course schedule gives about **7 weeks**, and the foundation must be built early. Week 8 (midterm) is a buffer, not extra build time.

| Week | Course lab | Build tasks | Output |
|---|---|---|---|
| **1** | Python intro | Repo, Docker Compose, CI skeleton, FastAPI "hello", Postgres connection, Alembic. Write the `Problem`/`SearchResult` base classes using functions, tuples, sets, dicts. | App boots; CI green |
| **2** | Functions, tuples, sets, dicts | Auth (F1), roles, tenant dependency, user/org/membership tables; menu and ingredient tables and CRUD (F3) | Login + menu API |
| **3** | Data structures, loops | Clients (F4), events and event items (F5), seed data script; implement queue/stack utilities for search | Event builder API |
| **4** | **BFS** | Module A (allergen finder) + tests + UI; frontend shell, login and menu pages | BFS feature live |
| **5** | **DFS** | Module B (constraint solver, plain + pruned) + tests + UI; calendar page (F6) and iCal feed | DFS feature live |
| **6** | **Greedy, A\*** | Module C (menu optimizer + route planner) + tests + UI; proposals and PDF (F7 part 1) | A\*/greedy live |
| **7** | **Minimax, Alpha-Beta** | Module D + tests + UI; benchmark page (Section 13); Stripe deposit flow (F7 part 2); reports (F8) | All four AI modules + benchmark |
| **8** | Midterm | **Buffer:** bug fixes, PWA polish (F9), deployment, documentation, demo rehearsal. Do not start new features. | Project 1 release `v1.0` |

**Weekly rhythm (suggested):** Monday plan → Tue–Thu build → Friday test and write notes for the report.

**If you fall behind:** drop in this order: PWA offline mode → audit log → multi-location UI → Stripe (keep invoices without online payment) → PDF styling. Never drop the AI modules or tests.

---

## 18. Acceptance criteria and definition of done

### 18.1 Feature-level acceptance (examples)

- **Allergen finder:** given a dish with peanut sauce and a peanut-allergic guest, returns a swap chain of minimal length; returns "no safe version" when none exists; response includes `nodes_expanded`.
- **Constraint solver:** for the sample 80-guest scenario, returns a valid package in under 2 seconds; an impossible budget returns a clear "no valid package" message.
- **Optimizer:** returns a package whose cost is ≤ any other valid package (verified against brute force on a small dataset).
- **Route planner:** A\* cost ≤ greedy cost on every test graph.
- **Bid advisor:** minimax and alpha-beta values are equal on 100 random trees; alpha-beta expands fewer nodes on average.
- **Payments:** completing a test-mode checkout marks the deposit invoice paid and confirms the event; replaying the same webhook changes nothing.
- **Reports:** profit per event equals revenue minus food cost on the seeded data (verified by test).
- **Mobile:** the site installs as a PWA and passes the Lighthouse PWA audit.

### 18.2 Project-level definition of done

- [ ] All **Must** and **Should** features working on the deployed URL
- [ ] CI is green; coverage targets met
- [ ] Tenant isolation tests pass
- [ ] `README` lets a stranger run the app in ≤ 10 minutes
- [ ] Seed data and a demo account available
- [ ] `docs/algorithms.md` explains each algorithm with the problem formulation tables above
- [ ] Benchmark page populated with results
- [ ] Release tagged `v1.0-project1`
- [ ] Demo script rehearsed (Section 20)

---

## 19. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Foundation takes longer than planned (beginner learning curve) | High | High | Use FastAPI + Supabase Auth or a template; follow MoSCoW cuts; start AI engine in Week 1 in parallel |
| Stripe webhook bugs | Medium | Medium | Use Stripe CLI to replay events locally; idempotency tests |
| Minimax model feels artificial | Medium | Low | Document assumptions openly; show it as an educational model |
| Scope creep ("one more feature") | High | High | Feature freeze at the start of Week 8 |
| Deployment surprises | Medium | Medium | Deploy a "hello world" in Week 1 and redeploy weekly |
| Team coordination | Medium | Medium | Feature branches, small pull requests, weekly sync |
| Competitor claims in the report are challenged | Low | Medium | Phrase as "reported by reviewers"; avoid absolute statements |

---

## 20. Demo script and report outline

### 20.1 Five-minute demo

1. (30 s) Problem and who it's for.
2. (60 s) Log in, create an event, attach dishes, show live totals.
3. (60 s) Generate a proposal PDF, approve it from the client link, pay a test deposit, show the event becoming confirmed.
4. (90 s) Run the four AI helpers on one realistic event.
5. (45 s) Benchmark page: "here is the proof the algorithms behave as theory predicts".
6. (15 s) Show it installed on a phone.

### 20.2 Report outline

1. Introduction and problem statement
2. Market research (honest, with the limitations)
3. System design (architecture, data model)
4. AI modules: for each, formulate it as a search problem (state/actions/goal/cost/heuristic), give pseudocode, complexity, and results
5. Benchmark results and analysis
6. Testing and quality
7. Limitations and ethics (simulated assumptions, no live payments, allergen advice is a **decision aid, not a medical guarantee**)
8. Conclusion and handoff to Project 2

> **Safety note for allergens:** the allergen finder is a planning aid. The caterer remains responsible for verifying ingredients and labels. Say this in the UI and in the report.

---

## 21. Handoff to Project 2

Project 2 can start only if these are true at the end of Project 1:

- The database already stores **events, clients, event items, payments, headcount and dates** (these become the training data).
- The `ai_engine` package has a stable structure so new modules (`optimization`, `ml`, `expert_system`) can be added beside `search`.
- A **synthetic data generator** hook exists (an empty `scripts/generate_data.py` with the planned interface), because Project 2 needs hundreds of historical events.
- The `ai_runs` table and benchmark framework are reusable for comparing models.
- Release `v1.0-project1` is tagged, so Project 2 work happens on top of a stable base.

*End of Project 1 specification.*
