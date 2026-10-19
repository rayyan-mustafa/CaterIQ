# AGENTS.md - CaterIQ Repository & Workflow Guidelines

Welcome to CaterIQ. This document outlines the engineering standards, architecture boundaries, and commit workflows required for all AI agents and human contributors working in this repository.

---

## 1. Project Overview & Curriculum Boundaries

CaterIQ is an intelligent catering management and search engine platform. 
Currently, the active codebase is strictly scoped to **Weeks 1–5 (Labs 01–05)** of the AI Lab syllabus:
- **Week 1–2**: Python fundamentals, object-oriented domain models, SQLite/SQLAlchemy schemas, and FastAPI REST endpoints.
- **Week 3–4**: Uninformed Search — Breadth-First Search (BFS) for allergen safe-path graph substitutions.
- **Week 5**: Uninformed Search — Depth-First Search (DFS) for event menu constraint satisfaction.

> **Note**: Advanced modules (A* Search, Greedy Best-First Search, Minimax Adversarial Pricing, Benchmarks, Stripe, FastAPI, and Next.js) have been decoupled and documented in `ARCHIVED_MODULES_REFERENCE.md`. Do not reintroduce them into the active production build without explicit instructions.

---

## 2. Global Git Commit & Push Workflow Standards

Whenever you commit, push, or save progress in this repository, you **MUST** strictly adhere to the following rules:

### A. Conventional Commits Specification
All commit messages must follow this structure:

```text
<type>(<scope>): <concise description in imperative mood>

- <Bullet point explaining WHY and WHAT changed>
- <Additional context or details if applicable>
```

#### Approved Types:
- `feat`: New feature, endpoint, or algorithmic capability
- `fix`: Bug fix, error resolution, edge-case patch
- `refactor`: Code reorganization without behavioral alterations
- `perf`: Performance optimization or algorithmic speedup
- `test`: Adding, updating, or expanding unit and integration test suites
- `docs`: Documentation, README, guides, or report assets
- `chore`: Tooling, dependency management, or environment configuration
- `ci`: CI/CD pipeline modifications (`.github/workflows/`)

#### Dynamic Scope Mapping for CaterIQ:
Always infer the appropriate scope from the modified files:
- `ai`: Algorithmic engine, search routines (`ai_engine/search/`, `ai_engine/problems/`)
- `ui`: Streamlit frontend pages, components, or styles (`streamlit_app.py`, `.streamlit/`)
- `data`: In-memory datasets, knowledge graphs (`data.py`)
- `docs`: Documentation, reference blueprints, and visual diagrams
- `repo`: Repository-wide configs, root guidelines, or scripts

### B. Commit Execution Rules
1. **Present-Tense Imperative Mood**:
   - Correct: `feat(ai): implement bfs allergen pathfinder`
   - Incorrect: `feat(ai): implemented bfs allergen pathfinder` or `feat: adding bfs`
2. **Atomic Commits**:
   - Avoid lumping unrelated components together. Group modifications into cohesive commits matching their scope.
3. **Always Clean Working Tree**:
   - Verify `git status` before committing to ensure no unwanted scratch files or temporary build caches are tracked.
4. **Pre-Push Validation**:
   - Verify Streamlit runs without errors:
     ```bash
     python -m streamlit run streamlit_app.py --server.headless true
     ```
5. **Seamless Push**:
   - Ensure the branch is tracked with `origin` and push cleanly using `git push -u origin <branch>`.

---

## 3. Directory Layout

```text
CaterIQ/
├── .streamlit/                  # Next.js-inspired dark theme configuration
├── AGENTS.md                    # AI Pair-programming guidelines and standards
├── ARCHIVED_MODULES_REFERENCE.md # Complete technical blueprint of decoupled features
├── README.md                    # Project overview & quickstart
├── ai_engine/                   # Weeks 1-5 Search & AI Engine
│   ├── search/                  # BFS and DFS algorithms (core.py, bfs.py, dfs.py)
│   └── problems/                # AllergenSubstitution & MenuConstraintSatisfaction
├── streamlit_app.py             # Modern Next.js-aesthetic Streamlit UI
├── data.py                      # Pure Python in-memory datasets (Weeks 2-3)
└── requirements.txt             # Minimal dependencies (streamlit)
```

---

## 4. Academic Attribution
- **Student**: Rayyan Mustafa
- **Registration Number**: 2312335
- **Course**: Artificial Intelligence Lab — Semester Project
