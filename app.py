"""CaterIQ — AI Catering Intelligence Studio.

Student: Rayyan Mustafa
Registration: 2312335
Course: Artificial Intelligence Lab — Semester Project
Curriculum Focus: Weeks 1–5 Uninformed State-Space Search (BFS & DFS)
100% Pure Python UI (Streamlit) & In-Memory Data Structures.
"""

import streamlit as st
import time

# Import our pure Python data structures
from data import (
    ALLERGENS,
    INGREDIENT_ALLERGENS,
    ALLOWED_SUBSTITUTIONS,
    RECIPES,
    DISH_CATALOG,
    EVENTS,
)

# Import our pure Python AI search algorithms
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints

# Configure Streamlit page
st.set_page_config(
    page_title="CaterIQ — AI Search Studio",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for a sleek, clean, modern dark appearance
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }
    .metric-card {
        background: #131b2e;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
    }
    .metric-val {
        font-size: 26px;
        font-weight: 800;
        color: #818cf8;
    }
    .metric-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    .header-box {
        background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
        border: 1px solid #312e81;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🍽️ CaterIQ")
st.sidebar.caption("AI Search & Catering Engine")

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🔍 Module A: BFS Allergen Finder",
        "🧩 Module B: DFS Menu Solver",
        "📋 Events & Dietary Requests",
        "📖 Menu & Graph Catalog",
    ],
    index=0,
)

st.sidebar.divider()
st.sidebar.markdown(
    """
    **Student Info:**
    - **Name**: Rayyan Mustafa
    - **Reg #**: 2312335
    - **Course**: AI Lab (Weeks 1–5)
    - **Engine**: 100% Pure Python
    """
)

# --- HEADER BLOCK ---
st.markdown(
    """
    <div class="header-box">
        <h1 style="margin:0; font-size: 28px; font-weight: 900; color: #ffffff;">
            CaterIQ — AI Catering Intelligence Studio
        </h1>
        <p style="margin: 6px 0 0 0; font-size: 14px; color: #cbd5e1;">
            Classical Uninformed Search Engine • <strong>Breadth-First Search (BFS)</strong> and <strong>Depth-First Search (DFS)</strong> with constraint pruning.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# TAB 1: BFS ALLERGEN FINDER (MODULE A - LAB 04)
# ==============================================================================
if nav_choice == "🔍 Module A: BFS Allergen Finder":
    st.subheader("Module A: Breadth-First Search (BFS) Allergen Safe-Path Finder")
    st.caption("Finds the guaranteed minimum number of ingredient swaps to eliminate target allergens from a recipe.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 1. Select Recipe & Allergens")
        selected_dish = st.selectbox("Choose a Recipe to Adapt:", list(RECIPES.keys()), index=0)
        original_ingredients = RECIPES[selected_dish]

        st.markdown("**Original Recipe Ingredients:**")
        for ing in original_ingredients:
            alg_tags = INGREDIENT_ALLERGENS.get(ing, set())
            tag_str = f" ⚠️ ({', '.join(alg_tags)})" if alg_tags else " ✅ (Safe)"
            st.write(f"- {ing}{tag_str}")

        target_allergens = st.multiselect(
            "Guest Allergens to Eliminate:",
            options=ALLERGENS,
            default=["peanut"],
        )

        run_bfs = st.button("🚀 Run BFS Search", use_container_width=True, type="primary")

    with col2:
        st.markdown("### 2. Search Engine Results (BFS)")

        if run_bfs:
            if not target_allergens:
                st.warning("Please select at least one allergen to eliminate.")
            else:
                with st.spinner("Executing Breadth-First Search over state space..."):
                    result = find_allergen_substitutions(
                        ingredients=original_ingredients,
                        ingredient_allergens=INGREDIENT_ALLERGENS,
                        allowed_substitutions=ALLOWED_SUBSTITUTIONS,
                        target_allergens=target_allergens,
                    )

                # Show Search Metrics
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    status_text = "Found Safe" if result.found else "No Path"
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Status</div><div class="metric-val">{status_text}</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Swaps</div><div class="metric-val">{len(result.swaps_required)}</div></div>', unsafe_allow_html=True)
                with m3:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Nodes Expanded</div><div class="metric-val">{result.nodes_expanded}</div></div>', unsafe_allow_html=True)
                with m4:
                    st.markdown(f'<div class="metric-card"><div class="metric-label">Runtime</div><div class="metric-val">{result.runtime_ms:.2f} ms</div></div>', unsafe_allow_html=True)

                st.markdown("---")

                if result.found:
                    st.success("✅ Safe substitution path discovered via BFS (Guaranteed Minimal Swaps)!")

                    if result.swaps_required:
                        st.markdown("#### 🔄 Ingredient Substitutions Applied:")
                        for i, swap in enumerate(result.swaps_required, 1):
                            st.info(f"**Step {i}**: Replace `{swap['from']}` ➡️ **`{swap['to']}`**")
                    else:
                        st.info("The original dish is already completely safe from these allergens! No swaps needed.")

                    st.markdown("#### 🥗 Final Safe Recipe Ingredients:")
                    cols = st.columns(2)
                    for idx, safe_ing in enumerate(result.safe_ingredients):
                        with cols[idx % 2]:
                            st.write(f"✔️ **{safe_ing}**")
                else:
                    st.error("❌ No valid safe version found in the substitution graph for these allergens.")
        else:
            st.info("👈 Select a recipe and target allergens on the left, then click **Run BFS Search**.")


# ==============================================================================
# TAB 2: DFS MENU CONSTRAINT SOLVER (MODULE B - LAB 05)
# ==============================================================================
elif nav_choice == "🧩 Module B: DFS Menu Solver":
    st.subheader("Module B: Depth-First Search (DFS) Menu Constraint Satisfaction")
    st.caption("Assembles a 3-course package (Starter, Main, Dessert) satisfying budget and dietary requirements using backtracking with early pruning.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 1. Set Menu Constraints")
        budget = st.slider("Max Budget per Head ($):", min_value=25.0, max_value=60.0, value=42.0, step=1.0)
        min_veg = st.number_input("Minimum Vegetarian Dishes:", min_value=0, max_value=3, value=1)
        min_gf = st.number_input("Minimum Gluten-Free Dishes:", min_value=0, max_value=3, value=1)

        enable_pruning = st.checkbox("Enable Early Branch Pruning", value=True)

        run_dfs = st.button("🚀 Run DFS Solver", use_container_width=True, type="primary")

    with col2:
        st.markdown("### 2. Search Engine Results (DFS)")

        if run_dfs:
            slots = ["starter", "main", "dessert"]

            # Run solver with pruning and without pruning to show benchmark comparison!
            res_pruned = solve_menu_constraints(
                slots=slots,
                dishes=DISH_CATALOG,
                max_budget=budget,
                min_vegetarian=min_veg,
                min_gluten_free=min_gf,
                use_pruning=True,
            )

            res_plain = solve_menu_constraints(
                slots=slots,
                dishes=DISH_CATALOG,
                max_budget=budget,
                min_vegetarian=min_veg,
                min_gluten_free=min_gf,
                use_pruning=False,
            )

            active_res = res_pruned if enable_pruning else res_plain

            # Show Search Metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                status_text = "Found" if active_res["found"] else "Unfeasible"
                st.markdown(f'<div class="metric-card"><div class="metric-label">Status</div><div class="metric-val">{status_text}</div></div>', unsafe_allow_html=True)
            with m2:
                prune_label = "Active" if enable_pruning else "Off"
                st.markdown(f'<div class="metric-card"><div class="metric-label">Pruning</div><div class="metric-val">{prune_label}</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Nodes Expanded</div><div class="metric-val">{active_res["nodes_expanded"]}</div></div>', unsafe_allow_html=True)
            with m4:
                st.markdown(f'<div class="metric-card"><div class="metric-label">Runtime</div><div class="metric-val">{active_res["runtime_ms"]:.2f} ms</div></div>', unsafe_allow_html=True)

            st.markdown("---")

            # Pruning Benchmark Demonstration
            st.markdown("#### ⚡ Pruning Effectiveness Comparison")
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                st.metric("Nodes Expanded WITH Pruning", res_pruned["nodes_expanded"])
            with comp_col2:
                st.metric("Nodes Expanded WITHOUT Pruning", res_plain["nodes_expanded"], delta=f"-{res_plain['nodes_expanded'] - res_pruned['nodes_expanded']} nodes pruned", delta_color="inverse")

            st.markdown("---")

            if active_res["found"]:
                st.success("✅ Valid 3-Course Menu Package Constructed!")
                pkg = active_res["packages"][0]
                st.markdown(f"**Total Price per Head**: `${pkg['total_price_per_head']:.2f}` (Budget: `${budget:.2f}`)")

                for d in pkg["dishes"]:
                    tags = []
                    if d.get("is_vegetarian"): tags.append("Vegetarian")
                    if d.get("is_gluten_free"): tags.append("Gluten-Free")
                    tag_str = f" ({', '.join(tags)})" if tags else ""

                    st.markdown(f"- **{d['category'].capitalize()}**: {d['name']} — `${d['price_per_head']:.2f}`{tag_str}")
            else:
                st.error("❌ No menu combination can satisfy all specified constraints within this budget.")
        else:
            st.info("👈 Set your budget and dietary constraints, then click **Run DFS Solver**.")


# ==============================================================================
# TAB 3: EVENTS & CATERING REQUESTS
# ==============================================================================
elif nav_choice == "📋 Events & Dietary Requests":
    st.subheader("Client Catering Events & Dietary Constraints")
    st.caption("Real-world client requests containing guest counts, allergy restrictions, and budgets that feed into the AI search solvers.")

    for ev in EVENTS:
        with st.container():
            st.markdown(
                f"""
                <div style="background:#131b2e; border: 1px solid #1e293b; border-radius:12px; padding:16px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4 style="margin:0; color:#ffffff;">{ev['title']}</h4>
                        <span style="background:#1e293b; color:#818cf8; padding:3px 10px; border-radius:8px; font-size:12px; font-weight:700;">{ev['status']}</span>
                    </div>
                    <p style="margin:4px 0 8px 0; color:#94a3b8; font-size:13px;">Client: <strong>{ev['client']}</strong> &bull; Date: {ev['date']} &bull; Guests: <strong>{ev['guests']}</strong></p>
                    <div style="background:#0f172a; padding:8px 12px; border-radius:8px; font-size:12px; color:#fde047; border-left:3px solid #facc15;">
                        ⚠️ <strong>Dietary Constraint</strong>: {ev['notes']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# TAB 4: MENU & GRAPH CATALOG
# ==============================================================================
elif nav_choice == "📖 Menu & Graph Catalog":
    st.subheader("Catering Domain Data (Pure Python Lists & Dicts)")
    st.caption("The state space dataset used by BFS and DFS search routines. Zero database dependency.")

    t1, t2 = st.tabs(["Dishes Catalog (DFS Space)", "Substitution Graph (BFS Edges)"])

    with t1:
        st.markdown("#### All Candidate Dishes")
        formatted_dishes = [
            {
                "Category": d["category"].capitalize(),
                "Dish Name": d["name"],
                "Price ($)": f"${d['price_per_head']:.2f}",
                "Vegetarian": "Yes" if d["is_vegetarian"] else "No",
                "Gluten-Free": "Yes" if d["is_gluten_free"] else "No",
            }
            for d in DISH_CATALOG
        ]
        st.table(formatted_dishes)

    with t2:
        st.markdown("#### Ingredient Substitution Graph")
        st.write("Directed graph edges defining which ingredient can substitute for another:")
        sub_list = []
        for src, subs in ALLOWED_SUBSTITUTIONS.items():
            for dest, cost in subs:
                sub_list.append({"From Ingredient": src, "To Substitute": dest, "Cost": cost})
        st.table(sub_list)
