# CaterIQ — Project 2: Optimization, Reasoning and Machine Learning

> **Course:** Artificial Intelligence (semester project)
> **Covers course weeks:** 9 – 15 (Labs 09–15), assessed as **Lab Work 2** (weeks 9–11) and **Project 2** (weeks 12–15)
> **Builds on:** Project 1 (`v1.0-project1`) — read `PROJECT_1_CaterIQ_Foundation_and_Search_AI.md` first
> **Document audience:** developers *and* non-technical readers. Each section begins with "In simple words".

---

## Table of Contents

1. [What Project 2 adds, in simple words](#1-what-project-2-adds-in-simple-words)
2. [Prerequisites from Project 1](#2-prerequisites-from-project-1)
3. [Glossary (new terms)](#3-glossary-new-terms)
4. [Goals, non-goals, priorities](#4-goals-non-goals-priorities)
5. [The data problem and the synthetic data plan](#5-the-data-problem-and-the-synthetic-data-plan)
6. [Architecture changes](#6-architecture-changes)
7. [Data model additions](#7-data-model-additions)
8. [Machine-learning ground rules](#8-machine-learning-ground-rules)
9. [Module E — Shift Scheduler (Genetic Algorithm)](#9-module-e--shift-scheduler-genetic-algorithm)
10. [Module F — Client Segmentation (K-Means)](#10-module-f--client-segmentation-k-means)
11. [Module G — Rules Engine (Forward/Backward Chaining)](#11-module-g--rules-engine-forwardbackward-chaining)
12. [Module H — Demand Forecasting (Linear Regression)](#12-module-h--demand-forecasting-linear-regression)
13. [Module I — Booking Prediction (Decision Tree)](#13-module-i--booking-prediction-decision-tree)
14. [Module J — Neural Networks (Perceptron and MLP)](#14-module-j--neural-networks-perceptron-and-mlp)
15. [Model comparison page](#15-model-comparison-page)
16. [API additions](#16-api-additions)
17. [UI additions](#17-ui-additions)
18. [Testing strategy](#18-testing-strategy)
19. [Week-by-week plan](#19-week-by-week-plan)
20. [Acceptance criteria and definition of done](#20-acceptance-criteria-and-definition-of-done)
21. [Risks and mitigations](#21-risks-and-mitigations)
22. [Final demo and report outline](#22-final-demo-and-report-outline)
23. [Honest limitations](#23-honest-limitations)

---

## 1. What Project 2 adds, in simple words

Project 1 gave CaterIQ the everyday tools plus AI that **searches** for answers. Project 2 gives it AI that **learns from history and reasons with rules**.

| Real-life catering question | New AI helper | Course topic |
|---|---|---|
| "Who works which shift next week so every event is covered and nobody is overworked?" | Shift scheduler | Genetic Algorithm (Week 9) |
| "Which of my clients are big spenders, which are occasional, which are about to drift away?" | Client segmentation | K-Means (Week 10) |
| "Is this menu safe and compliant for these guests, and *why* was a dish blocked?" Also "what should I upsell?" | Rules engine with explanations | Forward/Backward chaining (Week 11) |
| "How much food should I prepare for an event of this type?" | Demand forecasting | Linear Regression (Week 12) |
| "Which leads are likely to book?" | Booking prediction | Decision Tree (Week 13) |
| "Can a neural network do better than the tree?" | Neural network classifiers | Single-layer (Week 14), Multi-layer (Week 15) |

**Project 2 delivers:** these six helpers integrated into the app, a synthetic-history data generator so models have something to learn from, and a **comparison page** that shows honestly which model works best and why.

---

## 2. Prerequisites from Project 1

Before starting, confirm all of these (see Project 1, Section 21):

- [ ] Release `v1.0-project1` is deployed and tagged
- [ ] Tables exist: `events`, `event_items`, `clients`, `invoices`, `payments`, `menu_items`, `locations`
- [ ] `ai_engine/` has the `search/` package and a stable layout
- [ ] CI is green with ≥ 90% coverage on `ai_engine`
- [ ] The `ai_runs` table and benchmark runner exist
- [ ] A placeholder `scripts/generate_data.py` exists

If something is missing, fix it in the first days of Week 9. Do not build on a shaky base.

---

## 3. Glossary (new terms)

| Term | Plain meaning |
|---|---|
| **Genetic Algorithm (GA)** | Evolution-inspired search: keep a population of candidate solutions, let the best "reproduce" with random mixing and small mutations, repeat for many generations. |
| **Chromosome** | One candidate solution, encoded as a list (e.g. "who works which shift"). |
| **Fitness function** | A score saying how good a chromosome is. |
| **Crossover** | Combining two parent solutions to make a child. |
| **Mutation** | A small random change to a solution. |
| **Selection** | Choosing which solutions get to reproduce (better ones more often). |
| **Elitism** | Copying the best few solutions unchanged to the next generation. |
| **K-Means** | Groups similar data points into K clusters by repeatedly moving cluster centers. |
| **Centroid** | The center of a cluster. |
| **Inertia** | How tight the clusters are (lower is tighter). |
| **Silhouette score** | A −1 to 1 measure of how well-separated clusters are. |
| **Forward chaining** | Start from known facts, apply rules to derive new facts until nothing new appears. |
| **Backward chaining** | Start from a goal/question and work back to see which facts would prove it. |
| **Knowledge base** | The list of rules and facts. |
| **Linear regression** | Fits a straight-line (or plane) relationship to predict a number. |
| **MSE / RMSE / MAE / R²** | Error and fit measurements for number predictions. |
| **Classification** | Predicting a category (e.g. will book / won't book). |
| **Decision tree** | A flowchart of yes/no questions that ends in a prediction. |
| **Gini / entropy** | Ways of measuring how "mixed" a group is, used to pick the best question to ask. |
| **Overfitting** | Memorizing the training data so well that it performs badly on new data. |
| **Train/validation/test split** | Separate data for learning, tuning, and final honest scoring. |
| **Accuracy / precision / recall / F1** | Ways of scoring a classifier. |
| **Confusion matrix** | A table of correct and wrong predictions by class. |
| **Perceptron** | The simplest neural network: one layer, one decision line. |
| **MLP** | Multi-layer perceptron: neural network with hidden layers. |
| **Activation function** | A non-linear step inside a neuron (sigmoid, ReLU, tanh). |
| **Backpropagation** | The method that adjusts network weights using the error. |
| **Epoch** | One full pass through the training data. |
| **Learning rate** | Size of each weight-adjustment step. |
| **Data leakage** | Accidentally letting the model see information it wouldn't have in real use. |
| **Synthetic data** | Artificial data generated by code to imitate real data. |
| **Random seed** | A number that makes "random" results repeatable. |

---

## 4. Goals, non-goals, priorities

### 4.1 Goals

1. Six AI modules, each implemented **from scratch in Python/NumPy** (to demonstrate understanding), and each **validated against a library implementation** (scikit-learn) where one exists.
2. A reproducible synthetic data generator, clearly labelled as simulated.
3. Every model evaluated with proper train/validation/test discipline.
4. A model comparison page and a "why did the AI say that?" explanation experience.
5. Everything integrated into the existing app, deployed, and tested.

### 4.2 Non-goals

- Claims about real-world accuracy (the data is simulated).
- Deep-learning frameworks (PyTorch/TensorFlow) as the main implementation.
- Real-time online learning, A/B testing, MLOps platforms.
- Predicting anything about real people beyond business-planning level.

### 4.3 Priorities (MoSCoW)

| Priority | Items |
|---|---|
| **Must have** | Data generator, GA scheduler, K-Means segmentation, rules engine (forward chaining at minimum), linear regression forecast, decision tree, perceptron, MLP, comparison page, tests, deployment |
| **Should have** | Backward chaining "explain why", feature importance display, saved model versions |
| **Could have** | Drag-and-drop schedule editor, what-if sliders for the forecast, export of model reports |
| **Won't have** | Real customer data, automatic retraining pipelines |

---

## 5. The data problem and the synthetic data plan

### 5.1 In simple words

Machine learning learns from past examples. A brand-new student app has no past events, so we **generate realistic fake history** with code. This is a normal, accepted practice for coursework, **as long as you say so**. Every chart and number in the report that comes from it must be labelled **"simulated data"**.

### 5.2 Why the generator must be designed carefully

If you generate data using a simple rule (for example, "leads from referrals always book"), a model will "discover" that rule and look brilliant. That tells you about your generator, not about the real world. To make the exercise meaningful:

- Add **noise** (some referral leads don't book; some cold leads do).
- Include **overlapping** patterns, not perfectly separable classes.
- Keep the generation logic **documented** so the report can state the assumptions.
- Never let the generator use the label to build the features (data leakage).

### 5.3 Generator specification (`scripts/generate_data.py`)

**Inputs:** `--seed 42 --orgs 1 --months 24 --events 600 --clients 120`

**Entities generated**

| Table | What is generated |
|---|---|
| `clients` | 120 clients with a hidden "type" (corporate-regular, one-off-personal, wedding, nonprofit, etc.) that influences behavior but is **not stored** as a column |
| `leads/events` | ~600 events over 24 months with seasonality (more weddings in summer/autumn, more corporate lunches mid-week, holiday-season parties) |
| `event_items` | Realistic dish choices by event type |
| `invoices/payments` | Deposits and balances; some late or unpaid |
| `staff` and `shifts` | 12–20 staff with roles, availability, and hour limits |

**Key simulated relationships (document these in the report)**

| Relationship | Simulation |
|---|---|
| Headcount → food quantity | Portions per head vary by event type, plus noise (±10–15%) |
| Event type + season → headcount | Wedding mean ~110, corporate lunch ~35, with spread |
| Lead → booking probability | A probability from lead source, lead time, budget fit, response speed, and event type; **then a random draw**, so outcomes are uncertain |
| Client behavior | Each hidden type gives different spend, frequency, and recency |

**Output:** rows inserted through the same SQLAlchemy models (so the app sees them as normal data), plus an exported `data/synthetic_v1.csv` for offline experiments.
**Reproducibility:** same seed ⇒ identical data. Record the seed and generator version in the report.
**Labelling:** a `data_source = 'synthetic'` column (or tag) on generated rows; the UI shows a visible "Simulated data" badge on AI pages.

### 5.4 Dataset sizes (targets)

| Dataset | Rows | Used by |
|---|---|---|
| Event history | ~600 | Forecasting (regression) |
| Leads with outcome | ~800 (about 35–45% booked) | Decision tree, perceptron, MLP |
| Client aggregates | ~120 | K-Means |
| Staff + shifts | ~15 staff, 4 weeks of events | Genetic algorithm |

---

## 6. Architecture changes

```
ai_engine/
├── search/                 # Project 1 (unchanged)
├── optimization/
│   ├── genetic.py          # generic GA framework
│   └── scheduling.py       # shift-scheduling problem (encoding, fitness)
├── ml/
│   ├── preprocessing.py    # scaling, encoding, train/val/test split
│   ├── metrics.py          # MSE, RMSE, MAE, R², accuracy, precision, recall, F1, confusion matrix, silhouette
│   ├── kmeans.py
│   ├── linear_regression.py
│   ├── decision_tree.py
│   ├── perceptron.py
│   └── mlp.py
├── expert_system/
│   ├── rules.py            # Rule, Fact, KnowledgeBase
│   ├── forward.py
│   └── backward.py
├── benchmarks/             # extended with model comparison runners
└── tests/
scripts/
└── generate_data.py
```

**Backend additions:** new routers under `/api/v1/ai/…`; a `model_registry` service that stores trained model parameters (JSON/NumPy) with a version number so the app can load a model without retraining on every request.

**Principle kept from Project 1:** `ai_engine` has **no web or database imports**. The backend loads data, converts it to NumPy arrays or plain Python objects, calls the engine, and returns results.

---

## 7. Data model additions

**staff**
`id, organization_id, location_id, full_name, role (cook|server|driver|lead), hourly_rate, max_hours_per_week, is_active`

**staff_availability**
`id, staff_id, weekday (0–6), start_time, end_time` (when they *can* work)

**shift_requirements** — generated from confirmed events
`id, event_id, role_needed, staff_count, shift_start, shift_end`

**shift_assignments** — the schedule output
`id, organization_id, schedule_run_id, staff_id, shift_requirement_id`

**schedule_runs**
`id, organization_id, week_start, params_json (population, generations, rates, seed), best_fitness, generations_run, runtime_ms, created_at`

**client_segments**
`id, organization_id, run_id, client_id, cluster_label, cluster_name`

**segmentation_runs**
`id, organization_id, k, features_json, inertia, silhouette, created_at`

**rules** — knowledge base (editable by Owners)
`id, organization_id, name, if_json (conditions), then_json (conclusions), category (allergen|compliance|upsell|operations), is_active`

**model_registry**
`id, organization_id, model_type (linreg|tree|perceptron|mlp), version, params_blob/json, train_metrics_json, test_metrics_json, trained_at, data_source, seed`

**predictions_log**
`id, organization_id, model_id, input_json, output_json, created_at` (for audit and the comparison page)

Also add `data_source` (`real|synthetic`) to `events`, `clients`, `invoices`, `payments`.

---

## 8. Machine-learning ground rules

*In simple words:* these are the habits that separate real ML from "it worked on my laptop once".

1. **Three-way split.** Randomly split into train (70%), validation (15%), test (15%) with a fixed seed. Tune using validation. Touch the test set **once**, at the end.
2. **Scale numeric features** (standardization) using statistics from the **training set only**; apply the same numbers to validation/test. Otherwise you leak information.
3. **Always compare against a baseline:** regression vs "predict the average"; classifiers vs "always predict the most common class". A model that doesn't beat the baseline is useless.
4. **Report multiple metrics**, not just accuracy: precision, recall, F1 and the confusion matrix for classifiers; RMSE, MAE and R² for regression.
5. **Fix random seeds** everywhere and record them.
6. **Implement from scratch, validate against scikit-learn.** Your own code must produce results close to the library's on the same data. This proves correctness and shows understanding.
7. **Watch for leakage.** Don't use features that only exist after the outcome (e.g. "deposit paid" to predict "will book").
8. **Show uncertainty and limits.** Predictions are estimates; say so in the UI.

---

## 9. Module E — Shift Scheduler (Genetic Algorithm)

**Course week:** 9 (Lab 09 — Genetic Algorithm)

### 9.1 In simple words

Every week a caterer must decide who works which event: enough cooks and servers, nobody overworked, nobody scheduled when they're unavailable, labor cost kept reasonable. There are far too many possible schedules to check them all. The genetic algorithm creates a "population" of random schedules, scores them, lets the better ones combine and mutate, and repeats. After many generations it usually finds a very good schedule.

### 9.2 Problem formulation

**Inputs:** staff list (role, availability, max hours, hourly rate); shift requirements for the week (event, role, number needed, start/end).

**Chromosome encoding:** for each *slot* (one required person-position in one shift), store the ID of the assigned staff member.

```
slots:      [S1:cook, S2:cook, S3:server, S4:server, S5:driver, ...]
chromosome: [  4,       7,        2,        9,        5,        ...]   # staff IDs
```

**Fitness function** (lower penalty = better; implement as `fitness = −total_penalty` or `1/(1+penalty)`):

| Rule | Type | Penalty |
|---|---|---|
| Staff has the wrong role for the slot | Hard | very large (e.g. 1000) |
| Staff is unavailable at that time | Hard | very large |
| Same person assigned to two overlapping shifts | Hard | very large |
| Weekly hours exceed the person's max | Hard/soft | large, scaled by hours over |
| Total labor cost above target | Soft | proportional to the excess |
| Unfair distribution of hours (high variance) | Soft | small × variance of hours |
| Long shift without rest day pattern, or a very late shift followed by an early shift | Soft | small |
| Preferred staff for a client/event (optional) | Soft | small bonus |

**Hard constraints** must reach zero for a schedule to be called *valid*. Soft constraints improve quality.

### 9.3 Algorithm

```
population = random_valid_ish_schedules(size=N)
for generation in range(G):
    scores = [fitness(c) for c in population]
    new_population = top_E(population, scores)            # elitism
    while len(new_population) < N:
        p1, p2 = tournament_select(population, scores), tournament_select(...)
        child = crossover(p1, p2) with probability Pc else copy(p1)
        child = mutate(child) with probability Pm per gene
        new_population.append(repair(child))              # optional fix-up of obvious violations
    population = new_population
    track best fitness, average fitness
    if no improvement for 40 generations: stop early
return best chromosome
```

**Operators to implement and compare**

| Operator | Options |
|---|---|
| Selection | Tournament (size 3–5) vs roulette-wheel |
| Crossover | One-point, two-point, uniform |
| Mutation | Replace a gene with another **eligible** staff member (same role); swap two genes |
| Elitism | Keep the top 2–5 solutions |

**Typical parameters (tune on validation scenarios):** population 100–200, generations 200–500, crossover rate 0.8, mutation rate 0.02–0.05 per gene.

### 9.4 Outputs and UI

- A weekly schedule grid (staff × days) with warnings for any remaining violations.
- Convergence chart: best and average fitness per generation.
- A manual-edit step: the manager can override, and the page recomputes the fitness and shows the new violations.
- Seed, parameters and runtime saved in `schedule_runs`.

### 9.5 Tests and validation

- **Tiny known case:** 3 staff, 3 slots with an obviously optimal schedule → GA finds it.
- **Hard-constraint test:** the returned best schedule has zero hard violations when a valid schedule exists.
- **Reproducibility:** the same seed yields the same result.
- **Convergence test:** best fitness is non-decreasing across generations when elitism is on.
- **Comparison experiment (report):** GA vs random search vs a greedy assignment; show GA's advantage with numbers.
- **Parameter study (report):** effect of mutation rate and population size on final fitness.

### 9.6 Honest notes

GA gives a **good** schedule, not a provably optimal one. Hard-constraint repair matters; without it GA wastes effort on illegal schedules.

---

## 10. Module F — Client Segmentation (K-Means)

**Course week:** 10 (Lab 10 — K-Means Clustering)

### 10.1 In simple words

Instead of treating all clients the same, group them by behavior so the caterer can act differently: look after the big regulars, win back the ones who've gone quiet, nurture the one-time buyers. No one labels the groups in advance; the algorithm finds them from the data. (This is "unsupervised learning".)

### 10.2 Features (one row per client)

This is the classic **RFM** idea plus extras:

| Feature | Meaning |
|---|---|
| Recency | Days since the last event |
| Frequency | Number of events in the period |
| Monetary | Total revenue from the client |
| Average headcount | Typical event size |
| Average lead time | Days between booking and event |
| Late-payment rate | Fraction of invoices paid late |

**Preprocessing:** log-transform skewed money values if needed, then **standardize** all features (K-Means uses distance, so scale matters).

### 10.3 Algorithm

```
choose K
centroids = k-means++ initialization (smarter than pure random)
repeat until centroids stop moving or max_iter:
    assign each client to the nearest centroid (Euclidean distance)
    move each centroid to the mean of its assigned clients
return assignments, centroids, inertia
```

Run with several random restarts and keep the lowest inertia.

### 10.4 Choosing K

- **Elbow method:** plot inertia for K = 2…10 and look for the "bend".
- **Silhouette score:** pick the K with the best separation.
- Show both charts in the app; let the user choose K, with a recommended default.

### 10.5 Making clusters useful

After clustering, name each cluster by its centroid (translate back from standardized units), for example:

| Cluster | Typical profile | Suggested action |
|---|---|---|
| "VIP regulars" | High frequency, high spend, recent | Priority service, loyalty offer |
| "At risk" | Previously frequent, now long inactive | Win-back message |
| "One-off big events" | Low frequency, high spend | Follow up before their next occasion |
| "Small occasional" | Low spend, low frequency | Low-touch email |

The naming rules are a simple lookup on centroid values; document them.

### 10.6 Tests and validation

- **Known clusters:** generate three clearly separated blobs → K-Means recovers them.
- **Match scikit-learn:** inertia within a small tolerance on the same data and initialization.
- **Empty cluster handling:** re-seed a centroid if a cluster ends up empty.
- **Determinism:** same seed ⇒ same clusters.
- **Report:** elbow chart, silhouette chart, cluster profile table, and an honest discussion that clusters are descriptive, not "truth".

### 10.7 UI

Client segmentation page: scatter plot (two chosen features or a 2D projection), cluster legend, a table of clients with their segment, and a segment filter on the clients list.

---

## 11. Module G — Rules Engine (Forward/Backward Chaining)

**Course week:** 11 (Lab 11 — Forward/Backward chaining)

### 11.1 In simple words

Some decisions are best made with **rules written by people**, not learned from data, especially when safety is involved. Example: "IF a guest has a gluten allergy AND the dish contains wheat THEN the dish is blocked for that guest." The rules engine applies such rules automatically, and, importantly, can **explain** why it reached a conclusion.

### 11.2 Knowledge representation

**Facts** are simple statements, e.g. `(guest_allergy, "gluten")`, `(dish_contains, "pasta", "wheat")`, `(headcount, 120)`, `(event_type, "wedding")`.
**Rules** have the form `IF condition₁ AND condition₂ … THEN conclusion`.

Example rule set (stored in the `rules` table, editable by Owners):

| Rule | If | Then |
|---|---|---|
| R1 | dish_contains(d, wheat) | dish_has_allergen(d, gluten) |
| R2 | dish_contains(d, peanut) | dish_has_allergen(d, peanut) |
| R3 | guest_allergy(a) AND dish_has_allergen(d, a) | dish_blocked(d, a) |
| R4 | event_type(wedding) AND headcount > 100 | requires(second_server_team) |
| R5 | headcount > 150 | requires(extra_van) |
| R6 | event_type(corporate) AND no_dessert_selected | suggest_upsell(dessert_box) |
| R7 | all_dishes_vegetarian_count = 0 AND headcount > 20 | warn(no_vegetarian_option) |
| R8 | event_within_days(3) AND balance_unpaid | alert(payment_overdue_risk) |

### 11.3 Forward chaining (data-driven)

*Question answered:* "Given everything we know about this event, what follows?"

```
facts = initial_facts(event)
changed = True
while changed:
    changed = False
    for rule in rules:
        if rule.conditions_hold(facts) and rule.conclusion not in facts:
            facts.add(rule.conclusion)
            record(rule, matched_facts)      # for explanations
            changed = True
return facts, derivation_log
```

Output on the event page: **blocked dishes**, **warnings**, **required resources**, **upsell suggestions**, each with the chain of rules that produced it.

### 11.4 Backward chaining (goal-driven)

*Question answered:* "Is this specific thing true, and what proves it?" For example: "Can dish X be served to guest Y?"

```
def prove(goal, facts, depth):
    if goal in facts: return True with trace
    for rule in rules_with_conclusion(goal):
        if all(prove(c, facts, depth+1) for c in rule.conditions):
            return True with trace
    return False
```

The result is a proof tree: "Dish X is blocked because it contains wheat (fact), wheat → gluten (R1), guest allergic to gluten (fact), so blocked (R3)."

**Loop protection:** keep a set of goals currently being proven to avoid infinite recursion.

### 11.5 Integration with earlier modules

- The **allergen BFS** module (Project 1) *fixes* a blocked dish by suggesting swaps. The rules engine *detects and explains* the block. Wire them together: "Dish blocked → Suggest substitutions."
- The **constraint solver** can use the rules engine's blocked list as hard constraints.

### 11.6 Tests

- Each rule fires on a hand-built fact set and not on a near-miss.
- Forward chaining terminates and reaches a fixed point; derivation log lists correct rules in a valid order.
- Backward chaining proves true goals, rejects false goals, and survives cyclic rules.
- Forward and backward agree: anything backward chaining proves is in forward chaining's final fact set.
- Rule edit test: disabling a rule removes its conclusions.

### 11.7 UI

An "Event check" panel: green checks, amber warnings, red blocks; clicking any item opens "Why?", which shows the rule chain from the backward-chaining trace. An Owner-only rule editor (Should).

> **Safety reminder:** rule output is decision support. The caterer must still verify ingredients and labelling. State this in the UI.

---

## 12. Module H — Demand Forecasting (Linear Regression)

**Course week:** 12 (Lab 12 — Linear Regression)

### 12.1 In simple words

How many kilograms of rice, or how many portions, should we prepare? Past events tell us how that quantity relates to things we know in advance (headcount, event type, season). Linear regression finds that relationship and uses it to predict the quantity for a new event. A better prediction means less waste and fewer shortages.

### 12.2 Problem formulation

- **Target (y):** total portions prepared (or total food cost) for the event.
- **Features (x):** headcount, event type (one-hot encoded), month/season (encoded), is_weekend, number of courses, average dish heaviness (a feature on the menu items).
- **Model:** ŷ = w₀ + w₁x₁ + … + w_nx_n

### 12.3 Implement three ways (all are in the course scope and make a great comparison)

| Method | Idea | Notes |
|---|---|---|
| **Normal equation** | Solve w = (XᵀX)⁻¹Xᵀy directly | Exact, quick for small data; use a stable solver (`np.linalg.lstsq`) |
| **Gradient descent** | Repeatedly nudge weights to reduce error | Tune the learning rate; plot the loss curve |
| **scikit-learn `LinearRegression`** | Library reference | Used to validate your two implementations |

**Loss function:** Mean Squared Error. Optionally add **Ridge (L2) regularization** as a "Should".

### 12.4 Evaluation

| Metric | Meaning |
|---|---|
| RMSE | Typical size of the error, in portions |
| MAE | Average absolute error |
| R² | Fraction of variation explained (1 = perfect, 0 = no better than average) |

Compare against the **baseline** "predict the average portions" and, as a stronger baseline, "headcount × average portions per head".
**Residual analysis:** plot predicted vs actual and residuals; check for patterns (a sign the straight-line assumption is weak).

### 12.5 Uncertainty (important for honesty)

Show a **prediction range** (e.g. ± 1.5 × RMSE, or an empirical residual interval) rather than a single exact number: "Prepare 420 portions (likely range 390–450)."

### 12.6 UI

On the event builder: "Suggested quantity" with the range, what drove the estimate (feature contributions = weight × value), and a note: "Estimate based on simulated history."

### 12.7 Tests

- Perfectly linear toy data → recovers the exact weights.
- Normal equation, gradient descent and scikit-learn agree within tolerance.
- Gradient descent loss is non-increasing with a suitable learning rate.
- Scaling features does not change normal-equation predictions.
- Report: a table of baselines vs model, plus plots.

---

## 13. Module I — Booking Prediction (Decision Tree)

**Course week:** 13 (Lab 13 — Linear Classification / Decision Tree)

### 13.1 In simple words

Not every inquiry becomes a booking. If the caterer can tell which leads are likely to book, they can spend their time on the right ones. A decision tree learns a flowchart of yes/no questions ("Was the lead a referral? Is the budget at least X per head? Did we reply within 2 hours?") that ends in "likely books" or "unlikely".

### 13.2 Problem formulation

- **Target:** `booked` (1 = became a confirmed event, 0 = did not).
- **Features available *at the time of the lead* (no leakage):** lead source, event type, headcount, budget per head vs our average price, days until the event, response time in hours, number of follow-ups, whether a tasting was offered, client's past events (0 for new).
- **Class balance:** about 35–45% booked; check and report it.

### 13.3 Algorithm (implemented from scratch)

```
def build_tree(rows, depth):
    if stopping_condition(rows, depth): return Leaf(majority_class, class_probabilities)
    best = None
    for each feature f, each candidate threshold t:      # or category split
        left, right = split(rows, f, t)
        gain = impurity(rows) − weighted_impurity(left, right)
        keep the split with the highest gain
    if best gain <= min_gain: return Leaf(...)
    return Node(best.f, best.t, build_tree(left, depth+1), build_tree(right, depth+1))
```

**Impurity:** Gini = 1 − Σ pₖ² (also implement entropy and compare).
**Stopping rules / pruning controls (to fight overfitting):** `max_depth`, `min_samples_split`, `min_samples_leaf`, `min_gain`.
**Prediction:** walk from the root following the answers; the leaf gives the class and a probability.

### 13.4 Evaluation

| Metric | Why |
|---|---|
| Accuracy | Overall correct rate (can mislead if classes are imbalanced) |
| Precision | Of the leads predicted to book, how many did |
| Recall | Of the leads that booked, how many we caught |
| F1 | Balance of precision and recall |
| Confusion matrix | See exactly which mistakes happen |

**Baseline:** always predict the majority class.
**Overfitting study (report):** plot training vs validation accuracy as `max_depth` grows 1…15. Choose the depth where validation peaks.
**Validate:** compare against `sklearn.tree.DecisionTreeClassifier` with matching settings.

### 13.5 Explainability

- A readable text/diagram view of the tree.
- Per-lead explanation: the path of questions taken ("source = referral → yes; budget ≥ $38/head → yes; reply < 4h → yes → 78% likely").
- **Feature importance:** total impurity reduction per feature.

### 13.6 UI

Lead list sorted by booking probability, with an explanation popover per lead and a "model quality" card (metrics, **marked as simulated**).

### 13.7 Tests

- Pure-class data → single leaf.
- A tiny dataset with a known best split → the tree picks it.
- Depth limit respected.
- Matches scikit-learn's predictions on the same data (allow small tie-breaking differences).
- No-leakage test: the feature list contains none of the forbidden post-outcome fields.

---

## 14. Module J — Neural Networks (Perceptron and MLP)

**Course weeks:** 14 (Single-layer network) and 15 (Multi-layer network)

### 14.1 In simple words

A neural network is a set of simple "neurons" that each take numbers in, weigh them, and pass on a result. We train it by showing examples and adjusting the weights to reduce mistakes. Week 14 builds the simplest version (one layer: draws one straight dividing line). Week 15 adds hidden layers so the network can learn curved, more complicated boundaries. We apply both to the **same booking-prediction task** so the comparison is fair.

### 14.2 Single-layer network (Perceptron / logistic unit) — Week 14

**Structure:** inputs → one output neuron.

```
z = w·x + b
output = step(z)               # classic perceptron (0/1)
          or sigmoid(z)        # logistic variant giving a probability
```

**Training (classic perceptron rule):**

```
for epoch in range(E):
    for each (x, y) in training data:
        y_hat = predict(x)
        error = y − y_hat
        w ← w + η · error · x
        b ← b + η · error
```

**Variant:** the sigmoid-output version trained with gradient descent on cross-entropy loss (a "logistic regression" neuron), which gives probabilities and converges even on non-separable data.
**Important limitation to demonstrate in the report:** a perceptron can only learn **linearly separable** patterns. Show it failing on the XOR toy problem — this motivates Week 15.
**Preprocessing:** standardize numeric features; one-hot encode categories.

### 14.3 Multi-layer network (MLP) — Week 15

**Structure:** inputs → hidden layer(s) → output.

Suggested starting architecture: `n_features → 16 → 8 → 1` with ReLU (or tanh) hidden activations and a sigmoid output.

**Forward pass:** for each layer, `a = activation(W·a_prev + b)`.
**Loss:** binary cross-entropy.
**Backpropagation (the key idea):** compute the output error, then pass it backwards layer by layer using the chain rule to get each weight's gradient; update weights with gradient descent.

```
for epoch in range(E):
    for each mini-batch:
        forward pass, store activations
        loss = cross_entropy(y, y_hat)
        backward pass: gradients for every W, b
        W ← W − η · dW ; b ← b − η · db
    log training and validation loss/accuracy
    early stop if validation loss hasn't improved for 20 epochs
```

**Implementation rules**

- Initialize weights sensibly (e.g. He or Xavier initialization), seeded.
- Verify gradients with **numerical gradient checking** on a tiny network (a classic correctness test).
- Mini-batch gradient descent; learning rate tuned on validation data.
- Optional extras: L2 weight decay, dropout (Could).

### 14.4 Evaluation protocol (the same for tree, perceptron, MLP)

Same train/validation/test split, same preprocessing, same metrics (accuracy, precision, recall, F1, confusion matrix), plus the **majority-class baseline**.
Additional measures: training time, prediction time, number of parameters, and **explainability** (tree: full; perceptron: weights; MLP: limited).

### 14.5 Tests

- XOR: perceptron fails (accuracy ≈ 50–75%), MLP solves it (100%).
- Linearly separable toy data: perceptron converges to zero training errors.
- Gradient check: analytical vs numerical gradients agree within ~1e-6 relative error.
- Loss decreases over epochs on training data.
- Same seed ⇒ same trained weights.
- Compare MLP accuracy with `sklearn.neural_network.MLPClassifier` of the same shape (results should be in the same range, not identical).

### 14.6 Honest expectation

On synthetic data built from simple noisy relationships, the decision tree, perceptron and MLP may perform **similarly**. That is a legitimate finding. Report what you see; do not tune until the MLP "wins". Discuss why (data size, noise level, how the data was generated).

---

## 15. Model comparison page

**In simple words:** one page that answers "which model should we trust, and why?"

**Booking prediction comparison**

| Model | Accuracy | Precision | Recall | F1 | Train time | Predict time | Explainable? |
|---|---|---|---|---|---|---|---|
| Baseline (majority class) | | | | | – | – | – |
| Decision tree | | | | | | | Yes (full) |
| Perceptron | | | | | | | Partly (weights) |
| MLP | | | | | | | Limited |

**Additional visuals:** confusion matrices side by side; training/validation curves; ROC curve (Could); the tree diagram.

**Other comparisons on the page**

| Module | Comparison shown |
|---|---|
| Forecasting | Baseline vs normal equation vs gradient descent vs scikit-learn |
| Scheduler | Random vs greedy vs genetic algorithm (fitness, hard violations, runtime) |
| Segmentation | Elbow and silhouette charts across K |

Every table and chart carries a **"Simulated data"** badge, the seed, and the generator version.

---

## 16. API additions

| Area | Endpoints |
|---|---|
| Data tools (admin) | `POST /admin/synthetic-data/generate`, `DELETE /admin/synthetic-data` |
| Scheduling | `POST /ai/schedule/solve`, `GET /ai/schedule/{run_id}`, `POST /ai/schedule/{run_id}/evaluate` (after manual edits) |
| Segmentation | `POST /ai/segments/run`, `GET /ai/segments/latest`, `GET /ai/segments/elbow` |
| Rules | `GET/POST /rules`, `PATCH /rules/{id}`, `POST /ai/rules/forward` (event check), `POST /ai/rules/prove` (backward, "why?") |
| Forecast | `POST /ai/forecast/train`, `POST /ai/forecast/predict` |
| Booking models | `POST /ai/leads/train` (tree | perceptron | mlp), `POST /ai/leads/predict`, `GET /ai/leads/explain/{lead_id}` |
| Comparison | `GET /ai/compare/leads`, `/ai/compare/forecast`, `/ai/compare/scheduler` |
| Registry | `GET /ai/models`, `GET /ai/models/{id}` |

Long-running operations (GA with many generations, MLP training) run as **background tasks** with a progress endpoint, so requests don't time out.

---

## 17. UI additions

| Page | Contents |
|---|---|
| **Scheduling** | Weekly grid, "Generate schedule" with parameter panel, convergence chart, violation list, manual edit with live re-scoring |
| **Client segments** | K selector (with elbow/silhouette charts), scatter plot, cluster cards with suggested actions |
| **Event check** | Rule results (blocks, warnings, upsells) with "Why?" explanations |
| **Event builder** | "Suggested quantity" with range and drivers |
| **Leads** | Probability column, explanation popover, model-quality card |
| **Model lab** | Comparison page (Section 15), training controls, model versions |
| **Everywhere AI is shown** | "Simulated data" badge and a short "what this means" tooltip written for non-technical users |

---

## 18. Testing strategy

| Level | What | Target |
|---|---|---|
| Unit — algorithms | Toy problems with known answers (see each module) | ≥ 90% coverage of new `ai_engine` code |
| Cross-validation vs library | Own implementation vs scikit-learn (K-Means inertia, linear regression weights, tree predictions, MLP accuracy range) | All within stated tolerances |
| Property tests | GA best-fitness non-decreasing with elitism; forward ⊇ backward conclusions; scaling invariance for normal equation | Pass |
| Reproducibility | Same seed ⇒ same data, clusters, weights, schedules | Pass |
| Data tests | Generator produces expected class balance, no nulls, no leakage columns, valid foreign keys | Pass |
| API tests | Each endpoint: success, validation error, auth, tenant isolation | All covered |
| Performance | GA run on the sample week < 30 s; MLP training < 60 s; predictions < 200 ms | Documented |
| Regression | All Project 1 tests still pass | Must |

**Rule:** CI stays green; model-training tests use small data and fixed seeds so they run in seconds.

---

## 19. Week-by-week plan

Course weeks 9–15. Weeks 9–11 are graded as lab work; weeks 12–15 as the final project.

| Week | Course lab | Build tasks | Output |
|---|---|---|---|
| **9** | Genetic Algorithm | Verify prerequisites; finish `generate_data.py` (staff, shifts, events); build the GA framework + scheduling problem + convergence chart; tests | Scheduler working on synthetic data |
| **10** | K-Means | Preprocessing + metrics modules; K-Means from scratch with k-means++; elbow/silhouette; segmentation page; scikit-learn comparison | Segments page live |
| **11** | Forward/Backward chaining | Rules data model and editor; forward chaining event check; backward chaining "Why?"; link to allergen BFS | Event check panel live |
| **12** | Linear Regression | Normal equation + gradient descent; features and baselines; forecasting UI with ranges; residual plots | Forecast live |
| **13** | Decision Tree | Tree from scratch (Gini/entropy); overfitting study; explanations; lead list UI | Lead scoring (tree) live |
| **14** | Single-layer NN | Perceptron + logistic variant; XOR demonstration; add to comparison | Perceptron in model lab |
| **15** | Multi-layer NN | MLP with backprop + gradient check; early stopping; full comparison page; final polish, documentation, deployment, rehearsal | Release `v2.0-project2` |

**Weekly rhythm:** implement the algorithm in the engine → test on toy data → compare with scikit-learn → integrate API → build UI → write the report section while it's fresh.

**If you fall behind:** drop in this order: drag-and-drop schedule editing → ROC curves → rule editor UI (keep rules in a seed file) → Ridge regularization → dropout. Never drop the six core modules, the tests, or the comparison page.

---

## 20. Acceptance criteria and definition of done

### 20.1 Module-level acceptance

- **Scheduler:** on the sample week, produces a schedule with **zero hard-constraint violations**, beats random and greedy baselines in fitness, and displays a convergence chart.
- **Segmentation:** K-Means recovers three planted clusters; inertia matches scikit-learn within tolerance; the UI names clusters from their centroids.
- **Rules engine:** forward chaining reaches a fixed point; every conclusion has a viewable "why" trace; backward chaining proves/rejects test goals correctly.
- **Forecast:** beats both baselines on the test set (lower RMSE); the UI shows the range; own implementations match scikit-learn.
- **Decision tree:** beats the majority baseline on F1; the validation-vs-depth chart is in the report; per-lead explanations work.
- **Perceptron:** converges on separable data; fails XOR as expected.
- **MLP:** solves XOR; passes gradient checking; reported fairly against the tree and perceptron.
- **Comparison page:** shows every model's metrics side by side with the simulated-data badge.

### 20.2 Project-level definition of done

- [ ] All **Must** modules implemented, tested, integrated and deployed
- [ ] Project 1 features still work (regression tests green)
- [ ] CI green; coverage targets met
- [ ] Synthetic data generator documented; seed and version recorded
- [ ] Every AI screen carries a "Simulated data" badge
- [ ] `docs/models.md` documents each model: formulation, parameters, metrics, limitations
- [ ] Model comparison page populated
- [ ] README updated with "how to regenerate data and retrain models"
- [ ] Release tagged `v2.0-project2`
- [ ] Final demo rehearsed

---

## 21. Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Synthetic data makes the results look too good or too bad | High | High | Add noise and overlap; document generator assumptions; discuss in the report |
| Backpropagation bugs | Medium | High | Gradient checking on a tiny network; compare to scikit-learn's range; build up from single-layer |
| Data leakage inflates accuracy | Medium | High | Explicit feature allow-list; leakage unit test |
| GA converges slowly or to illegal schedules | Medium | Medium | Repair operator, elitism, early stopping, tune on small scenarios first |
| Long-running training blocks the API | Medium | Medium | Background tasks + progress endpoint |
| Time crunch in weeks 12–15 (four modules) | High | High | Reuse the same dataset and metrics code; start the ML helpers (preprocessing, metrics) in Week 10 |
| Overclaiming in the report | Medium | Medium | Always say "simulated"; never claim real-world accuracy |
| Breaking Project 1 | Medium | High | Regression suite in CI; feature branches; tagged releases |

---

## 22. Final demo and report outline

### 22.1 Six-minute demo

1. (30 s) Recap: Project 1 features, now with learning-based AI.
2. (60 s) Generate a schedule: show the grid, convergence chart, and a manual edit with live re-scoring.
3. (45 s) Client segments: pick K, show clusters and suggested actions.
4. (60 s) Event check: show a blocked dish, click "Why?", then jump to substitution suggestions.
5. (45 s) Forecast: suggested quantity with a range.
6. (60 s) Leads: ranked by probability with an explanation.
7. (60 s) Model lab: tree vs perceptron vs MLP, with the XOR demonstration and an honest conclusion.

### 22.2 Report outline

1. Introduction and link to Project 1
2. Synthetic data: design, assumptions, and why it is acceptable here
3. Each module: problem, method (with the pseudocode above), parameters, results, limitations
4. Experimental method: splits, baselines, metrics, seeds
5. Comparison and discussion (why results look the way they do)
6. Testing and engineering quality
7. Ethics and limitations (simulated data, safety of rule-based allergen advice, fairness of scheduling, prediction caution)
8. Conclusion and future work (real data, more features, live retraining)

---

## 23. Honest limitations

State these plainly in the report and the app:

- **All learning results come from simulated data.** They demonstrate the methods, not real-world accuracy.
- **The scheduler finds good schedules, not guaranteed optimal ones.**
- **Clusters are descriptive.** Different K or features give different groups.
- **Linear regression assumes a straight-line relationship**, which is an approximation.
- **Rule-based allergen checks depend on correct ingredient data.** They support, but never replace, the caterer's own verification.
- **The neural network may not beat the tree** on this data, and that is an acceptable result.
- **No claim is made about market validation or real customers.**

*End of Project 2 specification.*
