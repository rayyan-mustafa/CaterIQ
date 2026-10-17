# CaterIQ — System Architecture & Multi-Tenancy

> **Project 1:** Platform Foundation & Search-Based Artificial Intelligence  
> **Author:** Rayyan Mustafa (Reg: 2312335)  
> **Course:** Artificial Intelligence (Semester Project)

---

## 1. Architectural Overview

CaterIQ is architected around a strict decoupled design separating the pure algorithmic search engine from web and database concerns:

```
 ┌──────────────────────┐             HTTPS              ┌──────────────────────┐
 │   Browser / Mobile   │ ─────────────────────────────► │   Next.js Frontend   │
 │         PWA          │ ◄───────────────────────────── │   (React + Tailwind) │
 └──────────────────────┘                                └──────────┬───────────┘
                                                                    │ REST / JSON
                                                                    ▼
                                                         ┌──────────────────────┐
    Stripe Checkout / Webhooks ◄───────────────────────► │   FastAPI Backend    │
    Apple/Google Calendar Sync ◄──── RFC 5545 iCal ───── │ (Auth, CRM, Invoices)│
                                                         └───────┬───────┬──────┘
                                                                 │       │
                                                   SQLAlchemy 2.0│       │ Pure Python
                                                                 ▼       ▼
                                                       ┌────────────┐ ┌────────────────┐
                                                       │ PostgreSQL │ │   ai_engine    │
                                                       │ / SQLite   │ │  (Search AI)   │
                                                       └────────────┘ └────────────────┘
```

---

## 2. Decoupled AI Search Engine (`ai_engine/`)

The search algorithms live in their own self-contained package (`ai_engine/`) with **zero dependencies on FastAPI, SQLAlchemy, or HTTP networking**.

### Benefits:
1. **Isolated Unit Testing:** All search algorithms can be tested in sub-second test runs without setting up a database or web server.
2. **Pedagogical Clarity:** Clear, educational implementation mapping directly to course lab concepts:
   - `core.py`: Abstract `Problem`, `Node`, and `SearchResult`.
   - `bfs.py`: FIFO queue (`collections.deque`), explored set.
   - `dfs.py`: LIFO stack with backtracking and early constraint pruning.
   - `greedy.py`: Priority queue ordered strictly by heuristic $h(n)$.
   - `astar.py`: Priority queue ordered by $f(n) = g(n) + h(n)$.
   - `adversarial.py`: 2-Player zero-sum Minimax tree search and Alpha-Beta pruning.
3. **Project 2 Handoff:** Clean abstraction layer ready to be extended with machine learning and expert systems.

---

## 3. Multi-Tenancy & Data Isolation

Multi-tenancy is enforced at the database and application levels:

1. **Foreign Key Scoping:** Every relational entity (`locations`, `clients`, `menu_items`, `events`, `proposals`, `invoices`, `payments`, `ai_runs`) contains an `organization_id` column.
2. **Injected Dependency:** The FastAPI dependency `get_current_context` extracts the authenticated user's `organization_id` directly from the validated cryptographically-signed JWT.
3. **Zero Client Trust:** Routes never accept an `organization_id` in request bodies or query parameters.
4. **Automated Tenant Isolation Tests:** The test suite (`backend/app/tests/test_tenant_isolation.py`) automatically verifies that a user from Tenant B querying Tenant A's IDs receives HTTP 404/403.

---

## 4. Financial & Payment Lifecycle

```
Lead Event ──► Proposed ──► Proposal Generated ──► Client Approves & Pays Deposit ──► Confirmed ──► Balance Invoice
```

1. **Server-Side Totals:** Event prices, food costs, and profit margins are calculated exclusively on the backend (`pricing_service.py`), never trusting values submitted by the client browser.
2. **Public Proposal Token:** Unguessable cryptographically-random tokens (`secrets.token_urlsafe(24)`) allow clients to review proposals without requiring a login account.
3. **Payment Idempotency:** Webhooks and checkout confirmations verify the unique `raw_event_id` before mutating invoices, preventing double-charging on replayed webhooks.
