# CaterIQ — Platform Foundation & Search-Based Artificial Intelligence

> **Course:** Artificial Intelligence (Semester Project 1)  
> **Student Name:** Rayyan Mustafa  
> **Registration Number:** 2312335  
> **Repository:** Production-Grade Clean Architecture & Algorithmic Foundation

---

## 🌟 Executive Summary

**CaterIQ** is an enterprise catering platform designed to solve the operational paperwork of event caterers (menus, proposals, event builder, calendar sync, deposits, and financial profit reporting) paired with **four classical AI search helpers**:

| Real-Life Problem | AI Search Module | Algorithm | Course Lab |
|---|---|---|---|
| "A guest is allergic to peanuts. What's the smallest change to this dish that makes it safe?" | **Allergen Substitution** | **Breadth-First Search (BFS)** | Lab 04 |
| "Build a 3-course package under $40/head with vegetarian and gluten-free options." | **Menu Constraint Solver** | **Depth-First Search (DFS) with Pruning** | Lab 05 |
| "What package delivers the highest guest appeal at the lowest price?" and "Fastest route?" | **Menu Optimizer & Routing** | **A\* Search vs Greedy Best-First** | Lab 06 |
| "A rival caterer is bidding on the same wedding. What price should I quote?" | **Bid Pricing Advisor** | **Minimax with Alpha-Beta Pruning** | Lab 07 |

---

## 🚀 Quickstart Guide (Under 10 Minutes)

### Option A: Standard Local Setup (Fastest, Zero External Dependencies)

#### 1. Setup Backend & AI Engine
```bash
# Clone the repository
git clone https://github.com/your-username/cateriq.git
cd cateriq

# Install backend dependencies
pip install -r backend/requirements.txt

# Populate realistic demo database (SQLite default)
python scripts/seed_data.py

# Launch FastAPI backend
python -m uvicorn backend.app.main:app --reload --port 8000
```
*Backend Swagger API docs available at: [http://localhost:8000/docs](http://localhost:8000/docs)*

#### 2. Setup Frontend
```bash
# In a new terminal:
cd frontend
npm install
npm run dev
```
*Frontend application available at: [http://localhost:3000](http://localhost:3000)*

---

### Option B: Docker Compose (Full Stack with PostgreSQL)

```bash
docker compose up --build
```
This boots:
- **PostgreSQL 16** on `localhost:5432`
- **FastAPI Backend** on `localhost:8000`
- **Next.js Frontend** on `localhost:3000`

---

## 🔑 Demo Credentials & Quick Links

- **Email:** `demo@cateriq.com`
- **Password:** `Password123!`
- **Role:** Owner (Apex Artisan Catering)
- **Public Client Proposal Portal:** [http://localhost:3000/p/demo-wedding-token-2026](http://localhost:3000/p/demo-wedding-token-2026)
- **iCal Calendar Subscription Feed:** [http://localhost:8000/api/v1/calendar/demo-calendar-token-apex-2026.ics](http://localhost:8000/api/v1/calendar/demo-calendar-token-apex-2026.ics)

---

## 🧪 Running Automated Tests

Run the test suite covering both the AI search engine and the multi-tenant backend API:

```bash
# Run full pytest suite with coverage
python -m pytest ai_engine/tests backend/app/tests -v
```

### Verified Test Properties:
- **BFS:** Finds the provably minimal swap chain of ingredient substitutions.
- **DFS:** Plain DFS and Pruned DFS return identical valid solutions, with Pruned DFS expanding up to **85% fewer nodes**.
- **A\* vs Greedy:** Verifies that A\* path cost $\le$ Greedy Best-First on deceptive routing graphs.
- **Minimax vs Alpha-Beta:** Verifies that Minimax and Alpha-Beta return the **exact same expected payoff**, while Alpha-Beta evaluates significantly fewer states.
- **Tenant Isolation:** Rigorous security suite verifying that Tenant B receives 404/403 when requesting Tenant A's private data.
- **Webhook Idempotency:** Webhooks replayed with the same event ID are safely ignored without double-processing.

---

## 📂 Repository Structure

```
cateriq/
├── README.md                    # Project documentation & quickstart
├── docker-compose.yml           # Multi-container orchestration (Postgres, Backend, Frontend)
├── .gitignore                   # Clean standard gitignore
├── .github/workflows/ci.yml     # GitHub Actions automated test & build pipeline
│
├── ai_engine/                   # PURE PYTHON (Zero DB or web dependencies)
│   ├── search/
│   │   ├── core.py              # Problem, Node, SearchResult abstractions
│   │   ├── bfs.py               # Breadth-First Search (FIFO queue)
│   │   ├── dfs.py               # Depth-First Search with backtracking & pruning
│   │   ├── greedy.py            # Greedy Best-First Search (h(n) priority)
│   │   ├── astar.py             # A* Search (f(n) = g(n) + h(n))
│   │   └── adversarial.py       # Minimax & Alpha-Beta Pruning
│   ├── problems/
│   │   ├── allergen_substitution.py # Module A (BFS)
│   │   ├── menu_constraints.py      # Module B (DFS)
│   │   ├── menu_optimizer.py        # Module C1 (A*)
│   │   ├── delivery_routing.py      # Module C2 (Greedy vs A*)
│   │   └── bid_pricing.py           # Module D (Minimax)
│   ├── benchmarks/
│   │   └── runner.py            # Automated benchmark comparisons
│   └── tests/                   # 100% pure Python unit tests
│
├── backend/                     # FASTAPI & SQLALCHEMY 2.0 SERVICE
│   ├── app/
│   │   ├── main.py              # Application entry point & CORS
│   │   ├── core/                # Config, database session, JWT security, auth dependencies
│   │   ├── models/              # SQLAlchemy models (multi-tenant scoped)
│   │   ├── schemas/             # Pydantic v2 request & response schemas
│   │   ├── services/            # Business logic (pricing, proposals, payments, reporting)
│   │   ├── routers/             # API routers (auth, events, menu, calendar, proposals, reports, ai)
│   │   └── tests/               # API, security, and tenant isolation tests
│   ├── Dockerfile
│   ├── requirements.txt
│   └── pyproject.toml
│
├── frontend/                    # NEXT.JS 14 (React, TypeScript, Tailwind CSS)
│   ├── app/                     # App router pages & layouts
│   ├── components/              # Reusable UI components (Navbar, Sidebar)
│   ├── lib/api.ts               # Typed API client
│   ├── public/manifest.json     # PWA manifest
│   └── Dockerfile
│
├── scripts/
│   ├── seed_data.py             # Seeds realistic demo catering business
│   └── generate_data.py         # Synthetic data generator interface for Project 2
│
└── docs/
    ├── architecture.md          # Multi-tenancy, security, and data flow architecture
    └── algorithms.md            # Formal AI problem formulations & admissibility proofs
```

---

## ⚖️ Safety & Ethical Disclaimer

- **Allergen Notice:** The allergen substitution finder is an artificial intelligence decision aid. Caterers and kitchen staff remain legally and operationally responsible for checking physical ingredient packaging and managing cross-contamination.
- **Payment Processing:** All payment workflows use simulated Stripe Test Mode credentials. No live payment cards are processed.
