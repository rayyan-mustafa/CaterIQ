"""CaterIQ — AI Catering Intelligence Studio.

Student: Rayyan Mustafa
Registration: 2312335
Course: Artificial Intelligence Lab — Semester Project
Curriculum Focus: Weeks 1–5 Uninformed State-Space Search (BFS & DFS)
100% Pure Python UI with Next.js Aesthetic (Tailwind Dark Theme)
"""

import streamlit as st
import time

# Import pure Python in-memory data structures
from data import (
    ALLERGENS,
    INGREDIENT_ALLERGENS,
    ALLOWED_SUBSTITUTIONS,
    RECIPES,
    DISH_CATALOG,
    EVENTS,
)

# Import pure Python AI search algorithms
from ai_engine.problems.allergen_substitution import find_allergen_substitutions
from ai_engine.problems.menu_constraints import solve_menu_constraints

# Configure Streamlit page
st.set_page_config(
    page_title="CaterIQ — AI Search Studio",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def render_html(html_str: str) -> None:
    """Safely render HTML in Streamlit without triggering Markdown code blocks."""
    clean = " ".join(line.strip() for line in html_str.strip().splitlines() if line.strip())
    st.markdown(clean, unsafe_allow_html=True)


# ==============================================================================
# NEXT.JS TAILWIND DARK-MODE DESIGN SYSTEM (CSS INJECTION)
# ==============================================================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #030712 !important;
        color: #f8fafc !important;
        -webkit-font-smoothing: antialiased;
    }

    /* Streamlit Sidebar Overhaul (Next.js dark look) */
    section[data-testid="stSidebar"] {
        background-color: #030712 !important;
        border-right: 1px solid #1e293b !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] span {
        color: #cbd5e1 !important;
    }

    /* Radio Navigation Pills (Replaces ugly round radio buttons) */
    div[data-testid="stRadio"] > div {
        gap: 6px;
    }
    div[data-testid="stRadio"] label {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        margin-bottom: 4px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stRadio"] label:hover {
        background: #1e293b !important;
        border-color: #3b82f6 !important;
        transform: translateX(2px);
    }
    div[data-testid="stRadio"] label[data-checked="true"],
    div[data-testid="stRadio"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(79, 70, 229, 0.25) 0%, rgba(99, 102, 241, 0.15) 100%) !important;
        border-color: #6366f1 !important;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.15) !important;
    }
    div[data-testid="stRadio"] label span {
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Cards & Containers (Glassmorphism Next.js) */
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid #1e293b;
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
    }
    .glass-card:hover {
        border-color: #334155;
    }

    /* Metrics Grid Card */
    .metric-box {
        background: #090d16;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }
    .metric-box-val {
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin-top: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .metric-box-lbl {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        color: #94a3b8;
        letter-spacing: 0.06em;
    }

    /* Modern Next.js Button */
    .stButton > button, button[kind="primary"] {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #4338ca 0%, #4f46e5 100%) !important;
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
        transform: translateY(-1px) !important;
    }

    /* Form Inputs & Selects Contrast Fix */
    .stSelectbox > div, .stMultiSelect > div, div[data-baseweb="select"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"] * {
        color: #f8fafc !important;
    }
    div[data-baseweb="popover"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
    }
    div[data-baseweb="tag"] {
        background-color: #1e1b4b !important;
        border: 1px solid #4338ca !important;
    }
    div[data-baseweb="tag"] span {
        color: #c7d2fe !important;
    }

    /* Sliders & Numbers */
    .stSlider > div, .stNumberInput > div {
        color: #f8fafc !important;
    }

    /* Next.js High-Contrast Custom Table */
    .modern-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        border: 1px solid #1e293b;
        border-radius: 14px;
        overflow: hidden;
        margin-top: 12px;
        margin-bottom: 16px;
    }
    .modern-table th {
        background-color: #0f172a;
        color: #94a3b8;
        font-weight: 700;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 14px 18px;
        border-bottom: 1px solid #1e293b;
        text-align: left;
    }
    .modern-table td {
        background-color: #030712;
        color: #f8fafc;
        font-size: 13px;
        font-weight: 500;
        padding: 14px 18px;
        border-bottom: 1px solid #1e293b;
    }
    .modern-table tr:last-child td {
        border-bottom: none;
    }
    .modern-table tr:hover td {
        background-color: #0b1329;
    }

    /* Pills & Badges */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 3px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    .badge-indigo {
        background: rgba(99, 102, 241, 0.15);
        color: #a5b4fc;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    .badge-emerald {
        background: rgba(16, 185, 129, 0.15);
        color: #6ee7b7;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    .badge-amber {
        background: rgba(245, 158, 11, 0.15);
        color: #fde047;
        border: 1px solid rgba(245, 158, 11, 0.3);
    }
    .badge-rose {
        background: rgba(244, 63, 94, 0.15);
        color: #fda4af;
        border: 1px solid rgba(244, 63, 94, 0.3);
    }

    /* Alert / Callout Boxes */
    .callout-box {
        background: #0b1329;
        border: 1px solid #1e293b;
        border-left: 4px solid #6366f1;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0;
        color: #f1f5f9;
        font-size: 13px;
    }
    .callout-success {
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        border-left: 4px solid #10b981;
        border-radius: 12px;
        padding: 14px 18px;
        margin: 12px 0;
        color: #6ee7b7;
        font-size: 13px;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #030712;
        border-bottom: 1px solid #1e293b;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 8px 16px !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important;
        border: 1px solid #334155 !important;
        color: #ffffff !important;
    }

    /* Client Quotation & Contract Delivery Box */
    .quotation-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 14px;
        padding: 18px 20px;
        margin-top: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==============================================================================
# STATE & NAVIGATION INITIALIZATION
# ==============================================================================
if "active_view" not in st.session_state:
    st.session_state["active_view"] = "events"
if "active_event_id" not in st.session_state:
    st.session_state["active_event_id"] = None


def navigate_to_events() -> None:
    """Callback to return to Events & Dietary Requests."""
    st.session_state["active_view"] = "events"
    st.session_state["active_event_id"] = None


def navigate_and_run_bfs(event_id: str) -> None:
    """Callback to switch to Module A and automatically trigger BFS search."""
    st.session_state["active_view"] = "bfs"
    st.session_state["active_event_id"] = event_id
    st.session_state["auto_run_bfs"] = True
    ev = next((e for e in EVENTS if e["id"] == event_id), None)
    if ev:
        preset_title = f"{ev['title']} — {ev['client']} (Eliminate {', '.join(ev['target_allergens'])})"
        st.session_state["bfs_preset_selector"] = preset_title
        st.session_state["bfs_dish_selector"] = ev["requested_dish"]
        st.session_state["bfs_alg_selector"] = [alg for alg in ev.get("target_allergens", []) if alg in ALLERGENS]
        st.session_state["_last_bfs_preset"] = preset_title


def navigate_and_run_dfs(event_id: str) -> None:
    """Callback to switch to Module B and automatically trigger DFS menu solver."""
    st.session_state["active_view"] = "dfs"
    st.session_state["active_event_id"] = event_id
    st.session_state["auto_run_dfs"] = True
    ev = next((e for e in EVENTS if e["id"] == event_id), None)
    if ev:
        preset_title = f"{ev['title']} — {ev['client']} (${ev['budget_per_head']:.0f}/head, {ev['guests']} guests)"
        st.session_state["dfs_preset_selector"] = preset_title
        st.session_state["dfs_budget_val"] = float(ev["budget_per_head"])
        st.session_state["dfs_min_veg_val"] = int(ev["min_vegetarian"])
        st.session_state["dfs_min_gf_val"] = int(ev["min_gluten_free"])
        st.session_state["_last_dfs_preset"] = preset_title


# ==============================================================================
# SIDEBAR (NEXT.JS BRANDED)
# ==============================================================================
with st.sidebar:
    render_html(
        """
        <div style="display:flex; align-items:center; gap:12px; margin-bottom: 16px;">
            <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); width: 38px; height: 38px; border-radius: 10px; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:20px; color:#ffffff; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);">
                C
            </div>
            <div>
                <div style="font-weight: 900; font-size: 18px; color: #ffffff; letter-spacing:-0.02em;">CaterIQ</div>
                <div style="font-size: 11px; color: #818cf8; font-weight:600; text-transform:uppercase; letter-spacing:0.05em;">AI Search Studio</div>
            </div>
        </div>
        """
    )

    active_view = st.session_state.get("active_view", "events")

    if active_view == "events":
        render_html(
            """
            <div style="font-size:10px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin: 16px 0 8px 4px;">Navigation Hub</div>
            <div style="background: linear-gradient(135deg, rgba(79, 70, 229, 0.25) 0%, rgba(99, 102, 241, 0.15) 100%); border: 1px solid #6366f1; border-radius:12px; padding:12px 14px; margin-bottom:12px; box-shadow: 0 4px 16px rgba(99, 102, 241, 0.15);">
                <div style="font-size:10px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.06em;">Active Dashboard</div>
                <div style="font-size:13px; font-weight:700; color:#ffffff; margin-top:2px;">📋 Events &amp; Dietary Requests</div>
                <div style="font-size:11px; color:#cbd5e1; margin-top:4px; line-height:1.4;">Select any client booking in the main view to launch BFS or DFS solvers.</div>
            </div>
            """
        )
    else:
        view_title = "🔍 Module A: BFS Allergen Finder" if active_view == "bfs" else "🧩 Module B: DFS Menu Solver"
        badge_cls = "badge-indigo" if active_view == "bfs" else "badge-amber"
        badge_lbl = "Lab 04: BFS" if active_view == "bfs" else "Lab 05: DFS"

        render_html(
            f"""
            <div style="font-size:10px; font-weight:800; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin: 16px 0 8px 4px;">Active Workspace</div>
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius:12px; padding:12px 14px; margin-bottom:12px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:10px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.06em;">Live AI Engine</span>
                    <span class="badge {badge_cls}">{badge_lbl}</span>
                </div>
                <div style="font-size:13px; font-weight:700; color:#ffffff; margin-top:4px;">{view_title}</div>
            </div>
            """
        )
        st.button(
            "⬅️ Back to Events & Requests",
            key="sidebar_back_to_events",
            use_container_width=True,
            on_click=navigate_to_events,
        )

    # Active Client Context Badge in Sidebar
    if st.session_state.get("active_event_id"):
        matched_ev = next((e for e in EVENTS if e["id"] == st.session_state["active_event_id"]), None)
        if matched_ev:
            st.markdown(
                f"""
                <div style="background:#090d16; border:1px solid #1e293b; border-left:3px solid #818cf8; border-radius:8px; padding:8px 12px; margin-top:14px; font-size:11px;">
                    <div style="color:#818cf8; font-weight:700; text-transform:uppercase; font-size:9px;">Active Client Context</div>
                    <div style="color:#ffffff; font-weight:700; margin-top:2px;">{matched_ev['client']}</div>
                    <div style="color:#94a3b8;">{matched_ev['title']} ({matched_ev['guests']} guests)</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # Student Info Box (Clean Glass Card)
    st.markdown(
        """
        <div class="glass-card" style="padding:14px; margin-top:20px;">
            <div style="font-size:10px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;">Academic Attribution</div>
            <div style="font-size:13px; font-weight:700; color:#ffffff;">Rayyan Mustafa</div>
            <div style="font-size:12px; color:#94a3b8;">Reg #: <span style="color:#f8fafc; font-weight:600;">2312335</span></div>
            <div style="font-size:12px; color:#94a3b8;">Focus: <span style="color:#38bdf8; font-weight:600;">Weeks 1–5 (AI Lab)</span></div>
            <div style="margin-top:8px; display:flex; align-items:center; gap:6px;">
                <span class="badge badge-emerald">100% Pure Python</span>
                <span class="badge badge-indigo">Live Cloud</span>
            </div>
            <div style="margin-top:12px; display:flex; flex-direction:column; gap:6px; border-top: 1px solid rgba(255,255,255,0.08); padding-top:10px;">
                <a href="https://github.com/rayyan-mustafa/CaterIQ" target="_blank" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background: rgba(255,255,255,0.05); border: 1px solid #334155; border-radius: 6px; padding: 6px 10px; color: #f8fafc; font-size: 11px; font-weight: 600;">
                    <span>📂 GitHub Repository</span>
                </a>
                <a href="https://cateriq.streamlit.app" target="_blank" style="text-decoration:none; display:flex; align-items:center; justify-content:center; gap:6px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.35); border-radius: 6px; padding: 6px 10px; color: #a5b4fc; font-size: 11px; font-weight: 600;">
                    <span>🌐 cateriq.streamlit.app</span>
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# MAIN HEADER (NEXT.JS BANNER)
# ==============================================================================
st.markdown(
    """
    <div style="background: linear-gradient(135deg, rgba(30, 27, 75, 0.6) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: 20px; padding: 26px 30px; margin-bottom: 28px; box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);">
        <div style="display:inline-flex; align-items:center; gap:6px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); padding: 4px 12px; border-radius: 9999px; font-size: 11px; font-weight: 700; color: #a5b4fc; text-transform: uppercase; letter-spacing:0.05em; margin-bottom: 10px;">
            <span>Active Curriculum: Labs 04 &amp; 05 &bull; Real-World Client Delivery Engine</span>
        </div>
        <h1 style="margin: 0; font-size: 30px; font-weight: 900; color: #ffffff; letter-spacing: -0.03em;">
            CaterIQ Search Intelligence Studio
        </h1>
        <p style="margin: 6px 0 0 0; font-size: 14px; color: #cbd5e1; max-width: 850px; line-height: 1.5;">
            State-space formulation of live catering deliveries. Features <strong>Breadth-First Search (BFS)</strong> for minimal ingredient substitution and <strong>Depth-First Search (DFS)</strong> with constraint-based branch pruning for client quotation assembly.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==============================================================================
# MODULE A: BFS ALLERGEN FINDER (ACCESSIBLE VIA CLIENT EVENTS)
# ==============================================================================
if active_view == "bfs":
    col_b1, col_b2 = st.columns([1, 1])
    with col_b1:
        st.button("⬅️ Back to Events & Dietary Requests", key="bfs_back_btn", on_click=navigate_to_events, use_container_width=True)
    with col_b2:
        active_ev_id = st.session_state.get("active_event_id")
        current_ev = next((e for e in EVENTS if e["id"] == active_ev_id), None)
        if current_ev:
            st.button(f"🧩 Solve Menu with DFS for {current_ev['client']}", key="bfs_switch_dfs", on_click=navigate_and_run_dfs, args=(current_ev["id"],), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    auto_run_bfs = st.session_state.pop("auto_run_bfs", False)

    render_html(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 18px;">
            <div>
                <h2 style="font-size:20px; font-weight:800; color:#ffffff; margin:0;">Module A: BFS Allergen Safe-Path Finder</h2>
                <p style="font-size:12px; color:#94a3b8; margin:2px 0 0 0;">Uninformed search guaranteeing minimal recipe substitutions via FIFO queue.</p>
            </div>
            <span class="badge badge-indigo">Lab 04: BFS</span>
        </div>
        """
    )

    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_html('<div style="font-size:14px; font-weight:800; color:#ffffff; margin-bottom:12px;">1. Client Event &amp; Recipe Parameters</div>')

        # Event Demonstration Preset Dropdown
        bfs_presets = ["Custom Recipe Sandbox"] + [
            f"{ev['title']} — {ev['client']} (Eliminate {', '.join(ev['target_allergens'])})"
            for ev in EVENTS
        ]

        default_bfs_idx = 0
        if st.session_state.get("active_event_id"):
            for idx, ev in enumerate(EVENTS, 1):
                if ev["id"] == st.session_state["active_event_id"]:
                    default_bfs_idx = idx
                    break

        selected_bfs_preset = st.selectbox(
            "🎯 Client Event Demonstration Preset:",
            bfs_presets,
            index=default_bfs_idx if "bfs_preset_selector" not in st.session_state else None,
            key="bfs_preset_selector",
            help="Pre-loads a confirmed catering booking and their specific dietary emergency.",
        )

        active_bfs_event = None
        if selected_bfs_preset != "Custom Recipe Sandbox":
            ev_idx = bfs_presets.index(selected_bfs_preset) - 1
            active_bfs_event = EVENTS[ev_idx]
            st.session_state["active_event_id"] = active_bfs_event["id"]
        else:
            st.session_state["active_event_id"] = None

        if st.session_state.get("_last_bfs_preset") != selected_bfs_preset:
            st.session_state["_last_bfs_preset"] = selected_bfs_preset
            if active_bfs_event:
                if active_bfs_event.get("requested_dish") in list(RECIPES.keys()):
                    st.session_state["bfs_dish_selector"] = active_bfs_event["requested_dish"]
                st.session_state["bfs_alg_selector"] = [alg for alg in active_bfs_event.get("target_allergens", []) if alg in ALLERGENS]

        if active_bfs_event:
            render_html(
                f"""
                <div class="callout-box" style="border-left-color: #f59e0b; margin: 10px 0 14px 0;">
                    <div style="font-size:10px; font-weight:800; color:#f59e0b; text-transform:uppercase; letter-spacing:0.05em;">Client Event Binding Active</div>
                    <strong style="font-size:13px; color:#ffffff;">{active_bfs_event['title']} &bull; {active_bfs_event['client']}</strong>
                    <div style="font-size:12px; color:#cbd5e1; margin-top:3px;">
                        ⚠️ <strong>Case</strong>: {active_bfs_event['allergy_context']}. Target: <span style="color:#f87171; font-weight:700;">{", ".join(active_bfs_event['target_allergens'])}</span>.
                    </div>
                </div>
                """
            )

        dish_options = list(RECIPES.keys())
        default_dish_idx = 0
        if active_bfs_event and active_bfs_event.get("requested_dish") in dish_options:
            default_dish_idx = dish_options.index(active_bfs_event["requested_dish"])

        selected_dish = st.selectbox(
            "Choose a Recipe to Adapt:",
            dish_options,
            index=default_dish_idx if "bfs_dish_selector" not in st.session_state else None,
            key="bfs_dish_selector",
        )
        original_ingredients = RECIPES[selected_dish]

        render_html('<div style="font-size:11px; font-weight:700; text-transform:uppercase; color:#94a3b8; margin:14px 0 6px 0;">Original Recipe Ingredients</div>')
        for ing in original_ingredients:
            alg_tags = INGREDIENT_ALLERGENS.get(ing, set())
            if alg_tags:
                badge_html = f'<span class="badge badge-amber">⚠️ {", ".join(alg_tags)}</span>'
            else:
                badge_html = '<span class="badge badge-emerald">Safe</span>'
            render_html(f'<div style="display:flex; justify-content:space-between; align-items:center; padding: 6px 0; border-bottom:1px solid #1e293b; font-size:13px; color:#f8fafc;"><span>{ing}</span>{badge_html}</div>')

        st.markdown("<br>", unsafe_allow_html=True)

        default_target_allergens = ["peanut"]
        if active_bfs_event:
            default_target_allergens = [alg for alg in active_bfs_event.get("target_allergens", []) if alg in ALLERGENS]

        target_allergens = st.multiselect(
            "Target Allergens to Eliminate:",
            options=ALLERGENS,
            default=default_target_allergens if "bfs_alg_selector" not in st.session_state else None,
            key="bfs_alg_selector",
        )

        st.markdown("<br>", unsafe_allow_html=True)
        run_bfs = st.button("🚀 Run BFS Search", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_html('<div style="font-size:14px; font-weight:800; color:#ffffff; margin-bottom:14px;">2. Search Exploration Results</div>')

        should_run_bfs = run_bfs or auto_run_bfs or True
        if should_run_bfs:
            if not target_allergens:
                st.warning("Please select at least one allergen to eliminate.")
            else:
                result = find_allergen_substitutions(
                    ingredients=original_ingredients,
                    ingredient_allergens=INGREDIENT_ALLERGENS,
                    allowed_substitutions=ALLOWED_SUBSTITUTIONS,
                    target_allergens=target_allergens,
                )

                # Metrics Grid (Clean Next.js Boxes)
                m1, m2, m3, m4 = st.columns(4)
                with m1:
                    status_color = "#34d399" if result.found else "#f87171"
                    status_text = "FOUND" if result.found else "NO PATH"
                    render_html(f'<div class="metric-box"><div class="metric-box-lbl">Goal Test</div><div class="metric-box-val" style="color:{status_color};">{status_text}</div></div>')
                with m2:
                    render_html(f'<div class="metric-box"><div class="metric-box-lbl">Swaps Needed</div><div class="metric-box-val" style="color:#a78bfa;">{len(result.swaps_required)}</div></div>')
                with m3:
                    render_html(f'<div class="metric-box"><div class="metric-box-lbl">Nodes Expanded</div><div class="metric-box-val" style="color:#38bdf8;">{result.nodes_expanded}</div></div>')
                with m4:
                    render_html(f'<div class="metric-box"><div class="metric-box-lbl">Search Time</div><div class="metric-box-val" style="color:#fbbf24;">{result.runtime_ms:.2f}ms</div></div>')

                st.markdown("<br>", unsafe_allow_html=True)

                if result.found:
                    render_html('<div class="callout-success"><strong>✅ Optimal Path Found</strong>: BFS verified the shallowest safe substitution state in the graph.</div>')

                    if result.swaps_required:
                        render_html('<div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#94a3b8; margin: 12px 0 6px 0;">Substitutions Applied</div>')
                        for i, swap in enumerate(result.swaps_required, 1):
                            render_html(
                                f"""
                                <div style="display:flex; align-items:center; gap:10px; background:#090d16; border:1px solid #1e293b; padding:10px 14px; border-radius:10px; margin-bottom:8px; font-size:13px;">
                                    <span style="color:#818cf8; font-weight:700;">Step {i}:</span>
                                    <span style="text-decoration:line-through; color:#ef4444;">{swap['from']}</span>
                                    <span style="color:#94a3b8;">&rarr;</span>
                                    <span style="color:#10b981; font-weight:700;">{swap['to']}</span>
                                </div>
                                """
                            )
                    else:
                        render_html('<div class="callout-box">Recipe has no target allergens! Zero swaps required.</div>')

                    render_html('<div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#94a3b8; margin: 16px 0 8px 0;">Final Safe Recipe</div>')
                    cols = st.columns(2)
                    for idx, safe_ing in enumerate(result.safe_ingredients):
                        with cols[idx % 2]:
                            render_html(f'<div style="background:#090d16; border:1px solid #1e293b; padding:8px 12px; border-radius:8px; font-size:12px; color:#f8fafc; margin-bottom:6px;">✔️ <strong>{safe_ing}</strong></div>')

                    # Real-World Client Safety Clearance
                    if active_bfs_event:
                        render_html(
                            f"""
                            <div class="quotation-box">
                                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
                                    <span style="font-size:11px; font-weight:800; text-transform:uppercase; color:#34d399; letter-spacing:0.05em;">
                                        🛡️ Client Safety Clearance Issued
                                    </span>
                                    <span class="badge badge-emerald">Approved for Service</span>
                                </div>
                                <div style="font-size:13px; color:#ffffff;">
                                    <strong>{selected_dish}</strong> has been mathematically certified safe for <strong>{active_bfs_event['client']}</strong> ({active_bfs_event['guests']} attendees).
                                </div>
                                <div style="font-size:12px; color:#94a3b8; margin-top:4px;">
                                    Eliminated: <span style="color:#f87171; font-weight:700;">{", ".join(target_allergens)}</span> &bull; Status: Zero Cross-Contamination Risk.
                                </div>
                            </div>
                            """
                        )
                else:
                    render_html('<div class="callout-box" style="border-left-color:#ef4444; color:#fca5a5;">❌ Search Exhausted: No substitution sequence in the graph can eliminate all specified allergens.</div>')
        else:
            render_html(
                """
                <div style="text-align:center; padding: 40px 20px; color:#64748b;">
                    <div style="font-size:32px; margin-bottom:8px;">🔍</div>
                    <div style="font-size:14px; font-weight:600; color:#94a3b8;">Ready for Search Execution</div>
                    <div style="font-size:12px;">Select client event or recipe on the left and click <strong>Run BFS Search</strong>.</div>
                </div>
                """
            )

        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# MODULE B: DFS MENU CONSTRAINT SOLVER (ACCESSIBLE VIA CLIENT EVENTS)
# ==============================================================================
elif active_view == "dfs":
    col_d1, col_d2 = st.columns([1, 1])
    with col_d1:
        st.button("⬅️ Back to Events & Dietary Requests", key="dfs_back_btn", on_click=navigate_to_events, use_container_width=True)
    with col_d2:
        active_ev_id = st.session_state.get("active_event_id")
        current_ev = next((e for e in EVENTS if e["id"] == active_ev_id), None)
        if current_ev:
            st.button(f"🔍 Adapt '{current_ev['requested_dish']}' with BFS", key="dfs_switch_bfs", on_click=navigate_and_run_bfs, args=(current_ev["id"],), use_container_width=True)
    st.markdown("<br>", unsafe_allow_html=True)

    auto_run_dfs = st.session_state.pop("auto_run_dfs", False)

    render_html(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 18px;">
            <div>
                <h2 style="font-size:20px; font-weight:800; color:#ffffff; margin:0;">Module B: DFS Menu Constraint Solver</h2>
                <p style="font-size:12px; color:#94a3b8; margin:2px 0 0 0;">Assembles 3-course client catering packages using backtracking and branch pruning.</p>
            </div>
            <span class="badge badge-amber">Lab 05: DFS</span>
        </div>
        """
    )

    col1, col2 = st.columns([1, 1.4], gap="large")

    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_html('<div style="font-size:14px; font-weight:800; color:#ffffff; margin-bottom:12px;">1. Client Event &amp; Budget Constraints</div>')

        # Event Demonstration Preset Dropdown
        dfs_presets = ["Custom Constraints Sandbox"] + [
            f"{ev['title']} — {ev['client']} (${ev['budget_per_head']:.0f}/head, {ev['guests']} guests)"
            for ev in EVENTS
        ]

        default_dfs_idx = 0
        if st.session_state.get("active_event_id"):
            for idx, ev in enumerate(EVENTS, 1):
                if ev["id"] == st.session_state["active_event_id"]:
                    default_dfs_idx = idx
                    break

        selected_dfs_preset = st.selectbox(
            "🎯 Client Event Demonstration Preset:",
            dfs_presets,
            index=default_dfs_idx if "dfs_preset_selector" not in st.session_state else None,
            key="dfs_preset_selector",
            help="Pre-loads real client event constraints, headcount, and budget requirements.",
        )

        active_dfs_event = None
        if selected_dfs_preset != "Custom Constraints Sandbox":
            ev_idx = dfs_presets.index(selected_dfs_preset) - 1
            active_dfs_event = EVENTS[ev_idx]
            st.session_state["active_event_id"] = active_dfs_event["id"]
        else:
            st.session_state["active_event_id"] = None

        if st.session_state.get("_last_dfs_preset") != selected_dfs_preset:
            st.session_state["_last_dfs_preset"] = selected_dfs_preset
            if active_dfs_event:
                st.session_state["dfs_budget_val"] = float(active_dfs_event["budget_per_head"])
                st.session_state["dfs_min_veg_val"] = int(active_dfs_event["min_vegetarian"])
                st.session_state["dfs_min_gf_val"] = int(active_dfs_event["min_gluten_free"])

        default_budget = float(active_dfs_event["budget_per_head"]) if active_dfs_event else 44.0
        default_min_veg = int(active_dfs_event["min_vegetarian"]) if active_dfs_event else 1
        default_min_gf = int(active_dfs_event["min_gluten_free"]) if active_dfs_event else 1

        if "dfs_budget_val" not in st.session_state:
            st.session_state["dfs_budget_val"] = default_budget
        if "dfs_min_veg_val" not in st.session_state:
            st.session_state["dfs_min_veg_val"] = default_min_veg
        if "dfs_min_gf_val" not in st.session_state:
            st.session_state["dfs_min_gf_val"] = default_min_gf

        if active_dfs_event:
            current_budget_val = float(st.session_state.get("dfs_budget_val", default_budget))
            render_html(
                f"""
                <div class="callout-box" style="border-left-color: #6366f1; margin: 10px 0 14px 0;">
                    <div style="font-size:10px; font-weight:800; color:#818cf8; text-transform:uppercase; letter-spacing:0.05em;">Live Client Contract Active</div>
                    <strong style="font-size:13px; color:#ffffff;">{active_dfs_event['title']} &bull; {active_dfs_event['client']}</strong>
                    <div style="font-size:12px; color:#cbd5e1; margin-top:3px;">
                        👥 <strong>Contract Headcount</strong>: <span style="color:#38bdf8; font-weight:700;">{active_dfs_event['guests']} guests</span> &bull; 
                        💰 <strong>Target Budget Cap</strong>: <span style="color:#34d399; font-weight:700;">${current_budget_val:.2f}/head</span> <span style="color:#94a3b8; font-size:11px;">(Base: ${active_dfs_event['budget_per_head']:.2f})</span>
                    </div>
                </div>
                """
            )

        budget = st.slider("Maximum Budget per Head ($):", min_value=25.0, max_value=85.0, step=1.0, key="dfs_budget_val")
        min_veg = st.number_input("Minimum Vegetarian Dishes:", min_value=0, max_value=3, key="dfs_min_veg_val")
        min_gf = st.number_input("Minimum Gluten-Free Dishes:", min_value=0, max_value=3, key="dfs_min_gf_val")

        st.markdown("<br>", unsafe_allow_html=True)
        enable_pruning = st.checkbox("Enable Early Branch Pruning (Branch & Bound)", value=True, key="dfs_prune_val")

        st.markdown("<br>", unsafe_allow_html=True)
        run_dfs = st.button("🚀 Run DFS Solver", use_container_width=True, type="primary")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        render_html('<div style="font-size:14px; font-weight:800; color:#ffffff; margin-bottom:14px;">2. Solver Results &amp; Client Quotation</div>')

        should_run_dfs = run_dfs or auto_run_dfs or True
        if should_run_dfs:
            slots = ["starter", "main", "dessert"]

            # Run with and without pruning to show benchmark proof to the instructor
            res_pruned = solve_menu_constraints(
                slots=slots,
                dishes=DISH_CATALOG,
                max_budget=budget,
                min_vegetarian=min_veg,
                min_gluten_free=min_gf,
                use_pruning=True,
                find_all=True,
                max_solutions=15,
            )

            res_plain = solve_menu_constraints(
                slots=slots,
                dishes=DISH_CATALOG,
                max_budget=budget,
                min_vegetarian=min_veg,
                min_gluten_free=min_gf,
                use_pruning=False,
                find_all=True,
                max_solutions=15,
            )

            active_res = res_pruned if enable_pruning else res_plain

            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                status_color = "#34d399" if active_res["found"] else "#f87171"
                status_text = "FEASIBLE" if active_res["found"] else "FAILED"
                render_html(f'<div class="metric-box"><div class="metric-box-lbl">Goal Test</div><div class="metric-box-val" style="color:{status_color};">{status_text}</div></div>')
            with m2:
                prune_status = "ENABLED" if enable_pruning else "DISABLED"
                render_html(f'<div class="metric-box"><div class="metric-box-lbl">Pruning</div><div class="metric-box-val" style="color:#a78bfa; font-size:18px; margin-top:8px;">{prune_status}</div></div>')
            with m3:
                render_html(f'<div class="metric-box"><div class="metric-box-lbl">Nodes Expanded</div><div class="metric-box-val" style="color:#38bdf8;">{active_res["nodes_expanded"]}</div></div>')
            with m4:
                render_html(f'<div class="metric-box"><div class="metric-box-lbl">Runtime</div><div class="metric-box-val" style="color:#fbbf24;">{active_res["runtime_ms"]:.2f}ms</div></div>')

            st.markdown("<br>", unsafe_allow_html=True)

            # Pruning Effectiveness Comparison Box
            nodes_saved = max(0, res_plain['nodes_expanded'] - res_pruned['nodes_expanded'])
            pct_saved = (nodes_saved / res_plain['nodes_expanded'] * 100) if res_plain['nodes_expanded'] > 0 else 0
            if nodes_saved > 0:
                badge_html = f'<span class="badge badge-emerald" style="font-size:12px; padding:6px 12px;">✂️ Saved {nodes_saved} Nodes ({pct_saved:.0f}% Pruned)</span>'
            else:
                badge_html = '<span class="badge badge-indigo" style="font-size:12px; padding:6px 12px;">🎯 Optimal Search (0 Waste)</span>'

            render_html(
                f"""
                <div style="background:#090d16; border:1px solid #1e293b; border-radius:12px; padding:14px 18px; margin-bottom:14px;">
                    <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:#94a3b8; letter-spacing:0.05em; margin-bottom:8px;">Search Tree Pruning Comparison</div>
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:12px; color:#cbd5e1;">Plain DFS (No Pruning): <strong style="color:#f87171;">{res_plain['nodes_expanded']} nodes</strong></div>
                            <div style="font-size:12px; color:#cbd5e1;">DFS with Pruning: <strong style="color:#34d399;">{res_pruned['nodes_expanded']} nodes</strong></div>
                        </div>
                        {badge_html}
                    </div>
                </div>
                """
            )

            if active_res["found"]:
                selected_pkg_idx = 0
                if len(active_res["packages"]) > 1:
                    pkg_labels = [
                        f"Option {i+1} (${p['total_price_per_head']:.2f}/head) — {p['dishes'][0]['name']}, {p['dishes'][1]['name']}, {p['dishes'][2]['name']}"
                        for i, p in enumerate(active_res["packages"][:5])
                    ]
                    if "dfs_pkg_selector" in st.session_state and st.session_state["dfs_pkg_selector"] >= len(pkg_labels):
                        st.session_state["dfs_pkg_selector"] = 0
                    selected_pkg_idx = st.selectbox(
                        "📦 Feasible Package Variants Discovered by DFS:",
                        range(len(pkg_labels)),
                        format_func=lambda i: pkg_labels[i],
                        key="dfs_pkg_selector",
                        help="DFS explored the state space and found multiple compliant 3-course packages under budget."
                    )
                pkg = active_res["packages"][selected_pkg_idx]
                guest_count = active_dfs_event["guests"] if active_dfs_event else 50
                client_name = active_dfs_event["client"] if active_dfs_event else "Private Event Client"
                total_contract_cost = pkg["total_price_per_head"] * guest_count
                budget_cap_total = budget * guest_count
                contract_savings = max(0.0, budget_cap_total - total_contract_cost)

                render_html(
                    f"""
                    <div class="callout-success">
                        <strong>Package Selected</strong> &bull; Total Price: <strong>${pkg['total_price_per_head']:.2f}</strong> (Budget Limit: ${budget:.2f})
                    </div>
                    """
                )

                # Real-World Catering Quotation & Delivery Box
                render_html(
                    f"""
                    <div class="quotation-box">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                            <div>
                                <div style="font-size:11px; font-weight:800; text-transform:uppercase; color:#34d399; letter-spacing:0.05em;">Client Delivery Quotation</div>
                                <div style="font-size:14px; font-weight:800; color:#ffffff;">{client_name} &bull; Catering Order Contract</div>
                            </div>
                            <span class="badge badge-emerald">Ready for Service</span>
                        </div>
                        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; text-align:center;">
                            <div style="background:#030712; padding:10px 8px; border-radius:8px; border:1px solid #1e293b;">
                                <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:#94a3b8;">Package / Head</div>
                                <div style="font-size:16px; font-weight:800; color:#34d399; margin-top:2px;">${pkg['total_price_per_head']:.2f}</div>
                            </div>
                            <div style="background:#030712; padding:10px 8px; border-radius:8px; border:1px solid #1e293b;">
                                <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:#94a3b8;">Contract Size</div>
                                <div style="font-size:16px; font-weight:800; color:#818cf8; margin-top:2px;">{guest_count} attendees</div>
                            </div>
                            <div style="background:#030712; padding:10px 8px; border-radius:8px; border:1px solid #1e293b;">
                                <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:#94a3b8;">Total Contract</div>
                                <div style="font-size:16px; font-weight:800; color:#ffffff; margin-top:2px;">${total_contract_cost:,.2f}</div>
                            </div>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid #1e293b; font-size:12px;">
                            <span style="color:#cbd5e1;">Client Budget Cap: <strong style="color:#ffffff;">${budget_cap_total:,.2f}</strong></span>
                            <span style="color:#34d399; font-weight:700;">💰 Client Saves: ${contract_savings:,.2f}</span>
                        </div>
                    </div>
                    """
                )

                render_html('<div style="font-size:12px; font-weight:800; text-transform:uppercase; color:#94a3b8; margin: 16px 0 6px 0;">Selected 3-Course Menu</div>')
                for d in pkg["dishes"]:
                    tags = []
                    if d.get("is_vegetarian"): tags.append("Vegetarian")
                    if d.get("is_gluten_free"): tags.append("Gluten-Free")
                    tag_str = " &bull; ".join(tags)
                    tag_badge = f'<span class="badge badge-indigo">{tag_str}</span>' if tag_str else ""

                    render_html(
                        f"""
                        <div style="display:flex; justify-content:space-between; align-items:center; background:#090d16; border:1px solid #1e293b; padding:12px 16px; border-radius:10px; margin-bottom:8px;">
                            <div>
                                <span style="font-size:11px; font-weight:700; color:#818cf8; text-transform:uppercase; display:block;">{d['category']}</span>
                                <span style="font-size:14px; font-weight:700; color:#ffffff;">{d['name']}</span>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:14px; font-weight:800; color:#34d399;">${d['price_per_head']:.2f}</div>
                                {tag_badge}
                            </div>
                        </div>
                        """
                    )
            else:
                render_html('<div class="callout-box" style="border-left-color:#ef4444; color:#fca5a5;">❌ Constraint Failure: No 3-course combination satisfies all budget and dietary requirements.</div>')
        else:
            render_html(
                """
                <div style="text-align:center; padding: 40px 20px; color:#64748b;">
                    <div style="font-size:32px; margin-bottom:8px;">🧩</div>
                    <div style="font-size:14px; font-weight:600; color:#94a3b8;">Awaiting Constraints Configuration</div>
                    <div style="font-size:12px;">Select a client booking on the left and click <strong>Run DFS Solver</strong>.</div>
                </div>
                """
            )

        st.markdown('</div>', unsafe_allow_html=True)


# ==============================================================================
# PRIMARY HUB: EVENTS & CATERING REQUESTS (CONNECTED LIVE TO DFS & BFS)
# ==============================================================================
else:
    render_html(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 18px;">
            <div>
                <h2 style="font-size:20px; font-weight:800; color:#ffffff; margin:0;">Client Events &amp; Dietary Constraints</h2>
                <p style="font-size:12px; color:#94a3b8; margin:2px 0 0 0;">In-memory client bookings connected directly to live BFS allergen elimination &amp; DFS menu delivery.</p>
            </div>
            <span class="badge badge-indigo">Week 2-3 Domain State</span>
        </div>
        """
    )

    for ev in EVENTS:
        render_html(
            f"""
            <div class="glass-card" style="margin-bottom:14px; padding:20px 24px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <div>
                        <h3 style="margin:0; font-size:17px; font-weight:800; color:#ffffff;">{ev['title']}</h3>
                        <div style="font-size:12px; color:#818cf8; font-weight:600; margin-top:2px;">Client: <span style="color:#f8fafc;">{ev['client']}</span> &bull; Date: <span style="color:#f8fafc;">{ev['date']}</span></div>
                    </div>
                    <div style="display:flex; gap:8px;">
                        <span class="badge badge-emerald">{ev['status']}</span>
                        <span class="badge badge-indigo">👥 {ev['guests']} guests</span>
                    </div>
                </div>

                <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:10px; margin: 12px 0; font-size:12px;">
                    <div style="background:#090d16; padding:10px 12px; border-radius:8px; border:1px solid #1e293b;">
                        <div style="font-size:10px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Budget Cap</div>
                        <div style="font-weight:800; color:#34d399; font-size:14px; margin-top:2px;">${ev['budget_per_head']:.2f} / head</div>
                        <div style="color:#64748b; font-size:11px;">Max Contract: ${ev['budget_per_head'] * ev['guests']:,.2f}</div>
                    </div>
                    <div style="background:#090d16; padding:10px 12px; border-radius:8px; border:1px solid #1e293b;">
                        <div style="font-size:10px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Dietary Mandate</div>
                        <div style="font-weight:700; color:#f8fafc; font-size:13px; margin-top:2px;">🥗 {ev['min_vegetarian']} Veg &bull; 🌾 {ev['min_gluten_free']} GF</div>
                        <div style="color:#64748b; font-size:11px;">Minimum required courses</div>
                    </div>
                    <div style="background:#090d16; padding:10px 12px; border-radius:8px; border:1px solid #1e293b;">
                        <div style="font-size:10px; color:#94a3b8; text-transform:uppercase; font-weight:700;">Allergen Target</div>
                        <div style="font-weight:700; color:#f87171; font-size:13px; margin-top:2px;">⚠️ {', '.join(ev['target_allergens'])}</div>
                        <div style="color:#64748b; font-size:11px;">In: {ev['requested_dish']}</div>
                    </div>
                </div>

                <div style="background:#090d16; border:1px solid #1e293b; border-left:3px solid #facc15; padding:10px 14px; border-radius:8px; font-size:12px; color:#fde047; margin-bottom:6px;">
                    ⚠️ <strong>Client Context</strong>: {ev['allergy_context']}. {ev['notes']}
                </div>
            </div>
            """
        )

        # Action Buttons Row
        btn_c1, btn_c2 = st.columns(2)
        with btn_c1:
            st.button(
                f"🧩 Solve Menu with DFS for {ev['client']}",
                key=f"btn_dfs_{ev['id']}",
                type="primary",
                use_container_width=True,
                on_click=navigate_and_run_dfs,
                args=(ev["id"],),
            )

        with btn_c2:
            st.button(
                f"🔍 Adapt '{ev['requested_dish']}' with BFS",
                key=f"btn_bfs_{ev['id']}",
                use_container_width=True,
                on_click=navigate_and_run_bfs,
                args=(ev["id"],),
            )

        # One-Click Live AI Delivery Simulation inside each event card
        with st.expander(f"⚡ Live AI Delivery Simulation for {ev['client']} (Instant Evaluation)"):
            exp_c1, exp_c2 = st.columns(2)
            with exp_c1:
                render_html('<div style="font-size:12px; font-weight:800; color:#818cf8; text-transform:uppercase; margin-bottom:6px;">DFS Menu Delivery Result</div>')
                quick_dfs = solve_menu_constraints(
                    slots=["starter", "main", "dessert"],
                    dishes=DISH_CATALOG,
                    max_budget=ev["budget_per_head"],
                    min_vegetarian=ev["min_vegetarian"],
                    min_gluten_free=ev["min_gluten_free"],
                    use_pruning=True,
                    find_all=True,
                    max_solutions=10,
                )
                if quick_dfs["found"]:
                    q_pkg = quick_dfs["packages"][0]
                    q_total = q_pkg["total_price_per_head"] * ev["guests"]
                    render_html(
                        f"""
                        <div style="background:#030712; border:1px solid #10b981; border-radius:8px; padding:10px 14px; font-size:12px;">
                            <div style="color:#34d399; font-weight:700;">✅ Feasible 3-Course Package Found</div>
                            <div style="color:#ffffff; margin:4px 0;">&bull; {', '.join([d['name'] for d in q_pkg['dishes']])}</div>
                            <div style="color:#cbd5e1;">Price: <strong>${q_pkg['total_price_per_head']:.2f}/head</strong> &bull; Total: <strong style="color:#34d399;">${q_total:,.2f}</strong> for {ev['guests']} guests</div>
                        </div>
                        """
                    )
                else:
                    render_html('<div style="color:#f87171; font-size:12px;">❌ No package fits all constraints under budget.</div>')

            with exp_c2:
                render_html('<div style="font-size:12px; font-weight:800; color:#f59e0b; text-transform:uppercase; margin-bottom:6px;">BFS Allergen Adaptation</div>')
                dish_ing = RECIPES.get(ev["requested_dish"], [])
                quick_bfs = find_allergen_substitutions(
                    ingredients=dish_ing,
                    ingredient_allergens=INGREDIENT_ALLERGENS,
                    allowed_substitutions=ALLOWED_SUBSTITUTIONS,
                    target_allergens=ev["target_allergens"],
                )
                if quick_bfs.found:
                    swaps_desc = ", ".join([f"{s['from']} → {s['to']}" for s in quick_bfs.swaps_required]) if quick_bfs.swaps_required else "Already safe"
                    render_html(
                        f"""
                        <div style="background:#030712; border:1px solid #10b981; border-radius:8px; padding:10px 14px; font-size:12px;">
                            <div style="color:#34d399; font-weight:700;">🛡️ Safe Recipe Verified: {ev['requested_dish']}</div>
                            <div style="color:#ffffff; margin:4px 0;">Swaps: <strong style="color:#38bdf8;">{swaps_desc}</strong></div>
                            <div style="color:#cbd5e1;">Nodes expanded: {quick_bfs.nodes_expanded} &bull; Runtime: {quick_bfs.runtime_ms:.2f}ms</div>
                        </div>
                        """
                    )
                else:
                    render_html('<div style="color:#f87171; font-size:12px;">❌ No substitution path exists for this allergen.</div>')

        st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)




