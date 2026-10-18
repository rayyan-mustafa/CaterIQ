"""Script to generate a presentation for CaterIQ."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Colors
    BG_COLOR = RGBColor(11, 15, 25)        # Deep Navy / Dark slate
    CARD_BG = RGBColor(22, 30, 49)          # Card container navy
    CARD_BORDER = RGBColor(45, 55, 82)      # Card border
    PRIMARY = RGBColor(99, 102, 241)        # Indigo
    ACCENT_CYAN = RGBColor(56, 189, 248)    # Light Blue / Cyan
    EMERALD = RGBColor(16, 185, 129)       # Green
    TEXT_MAIN = RGBColor(248, 250, 252)     # White
    TEXT_MUTED = RGBColor(148, 163, 184)    # Slate muted
    AMBER = RGBColor(245, 158, 11)          # Amber

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="ARTIFICIAL INTELLIGENCE LAB • SEMESTER PROJECT"):
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf = cat_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category_text
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = PRIMARY

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MAIN

    def add_card(slide, left, top, width, height, title="", title_color=PRIMARY):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)

        if title:
            tb = slide.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.25), Inches(width - 0.6), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # ==========================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)

    # Accent decorative glow rectangle
    glow = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.1))
    glow.fill.solid()
    glow.fill.fore_color.rgb = CARD_BG
    glow.line.color.rgb = PRIMARY
    glow.line.width = Pt(1.5)

    # Pill badge
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.6), Inches(4.2), Inches(0.4))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 27, 75)
    pill.line.color.rgb = PRIMARY
    p_tf = pill.text_frame
    p_tf.margin_left = p_tf.margin_top = p_tf.margin_right = p_tf.margin_bottom = 0
    p = p_tf.paragraphs[0]
    p.text = "  ARTIFICIAL INTELLIGENCE LAB — SEMESTER PROJECT  "
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = ACCENT_CYAN

    # Title
    tb_title = s1.shapes.add_textbox(Inches(1.3), Inches(2.2), Inches(10.7), Inches(1.5))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CaterIQ: AI Catering Intelligence Studio"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    p2 = tf.add_paragraph()
    p2.text = "Uninformed State-Space Search (BFS & DFS) for Real-World Catering Optimization"
    p2.font.size = Pt(18)
    p2.font.color.rgb = ACCENT_CYAN
    p2.space_before = Pt(10)

    # Details Box (Author & Reg)
    tb_meta = s1.shapes.add_textbox(Inches(1.3), Inches(4.3), Inches(10.7), Inches(1.6))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True

    p = tf_m.paragraphs[0]
    p.text = "Student: Rayyan Mustafa"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN

    p2 = tf_m.add_paragraph()
    p2.text = "Registration Number: 2312335"
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(239, 68, 68)  # Bold red
    p2.space_before = Pt(4)

    p3 = tf_m.add_paragraph()
    p3.text = "Curriculum Scope: Labs 01–05 (OOP, BFS Allergen Safe-Paths, DFS Constraint Satisfaction)"
    p3.font.size = Pt(13)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(6)

    p4 = tf_m.add_paragraph()
    p4.text = "Implementation: 100% Pure Python • In-Memory Knowledge Graphs • Interactive Streamlit UI"
    p4.font.size = Pt(12)
    p4.font.color.rgb = EMERALD
    p4.space_before = Pt(4)

    # ==========================================
    # SLIDE 2: PROJECT OVERVIEW & LAB ALIGNMENT
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_header(s2, "Project Overview & Curriculum Alignment")

    # Card 1: Problem Statement
    add_card(s2, 0.8, 1.7, 5.6, 5.2, "Real-World Problem Formulation", ACCENT_CYAN)
    tb = s2.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    pts = [
        ("Catering Industry Bottleneck", "High-volume caterers struggle with complex guest allergies and tight budget constraints under strict deadlines."),
        ("Manual Trial-and-Error Fails", "Cross-referencing recipes against celiac, nut, and dairy allergies while preserving dish composition is error-prone."),
        ("Uninformed Search Solution", "State-space graph traversal guarantees mathematically optimal ingredient substitutions and compliant 3-course menus."),
        ("100% Pure Python", "Zero external database overhead (SQLite/PostgreSQL avoided). Uses in-memory adjacency sets for instant execution.")
    ]
    for i, (title, desc) in enumerate(pts):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    # Card 2: Lab Syllabus Mapping
    add_card(s2, 6.9, 1.7, 5.6, 5.2, "Syllabus Mapping (Weeks 1–5)", PRIMARY)
    tb2 = s2.shapes.add_textbox(Inches(7.2), Inches(2.4), Inches(5.0), Inches(4.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    labs = [
        ("Weeks 1 & 2: OOP & Data Modeling", "Russell & Norvig abstract classes (Problem, Node, SearchResult). In-memory knowledge graph in data.py."),
        ("Weeks 3 & 4: Lab 04 — BFS Search", "Breadth-First Search on ingredient substitution graph. Guarantees minimal number of recipe swaps."),
        ("Week 5: Lab 05 — DFS & Backtracking", "Depth-First Search for 3-course package construction with budget and dietary constraint satisfaction."),
        ("Branch-and-Bound Pruning", "Early constraint checks discard invalid subtrees before expanding deeper, preventing exponential explosion.")
    ]
    for i, (title, desc) in enumerate(labs):
        p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 3: RUSSELL & NORVIG THEORETICAL FOUNDATION
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_header(s3, "Theoretical Foundation: Russell & Norvig AI Paradigm")

    # 3 horizontal cards
    card_w = 3.65
    add_card(s3, 0.8, 1.7, card_w, 5.2, "1. Problem Abstraction", ACCENT_CYAN)
    tb = s3.shapes.add_textbox(Inches(1.05), Inches(2.4), Inches(3.15), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    c1_items = [
        ("initial_state()", "Returns the starting recipe state or empty meal slot."),
        ("actions(state)", "Generates legal actions (ingredient swap or next course dish)."),
        ("result(state, action)", "Computes transition to subsequent state."),
        ("is_goal(state)", "Verifies if goal state satisfies all allergen/course conditions."),
        ("prune(state)", "Backtracking hook: evaluates partial constraint violations.")
    ]
    for i, (fn, desc) in enumerate(c1_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"{fn}\n"
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = ACCENT_CYAN
        if i > 0:
            p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_MUTED

    add_card(s3, 4.85, 1.7, card_w, 5.2, "2. Node Bookkeeping", PRIMARY)
    tb = s3.shapes.add_textbox(Inches(5.1), Inches(2.4), Inches(3.15), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    c2_items = [
        ("State vs Node Separation", "A state represents world configuration; a Node is an active search tree bookkeeping structure."),
        ("parent pointer", "Tracks origin node to reconstruct full solution path from goal to root."),
        ("action", "The transition taken from parent to generate this node."),
        ("path_cost g(n)", "Cumulative path cost from start node."),
        ("depth", "Integer depth level of the search tree.")
    ]
    for i, (fn, desc) in enumerate(c2_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {fn}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_MUTED

    add_card(s3, 8.9, 1.7, card_w, 5.2, "3. SearchResult Container", EMERALD)
    tb = s3.shapes.add_textbox(Inches(9.15), Inches(2.4), Inches(3.15), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    c3_items = [
        ("solution_path", "Ordered sequence of states from initial to goal."),
        ("nodes_expanded", "Total number of nodes popped and tested from frontier."),
        ("nodes_generated", "Total child nodes produced by action successors."),
        ("max_frontier_size", "Peak queue/stack memory occupancy during search."),
        ("runtime_ms", "High-precision execution time measured in milliseconds.")
    ]
    for i, (fn, desc) in enumerate(c3_items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {fn}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(10)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 4: MODULE A — BREADTH-FIRST SEARCH (BFS)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_header(s4, "Module A: Breadth-First Search (BFS) for Allergen Safe-Paths", "LAB 04: UNINFORMED SEARCH (FIFO QUEUE)")

    add_card(s4, 0.8, 1.7, 5.6, 5.2, "Algorithmic Mechanics (bfs.py)", PRIMARY)
    tb = s4.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    bfs_points = [
        ("FIFO Frontier (collections.deque)", "Nodes explored in shallowest-first sequence using O(1) amortized popleft() and append()."),
        ("Explored Set Tracking", "Maintains visited frozenset states to eliminate cycles and redundant paths."),
        ("Mathematical Optimality", "Because every ingredient swap has uniform step cost (c = 1.0), BFS guarantees finding the minimum number of swaps."),
        ("Completeness", "Guaranteed to find a safe ingredient combination if one exists in the graph.")
    ]
    for i, (title, desc) in enumerate(bfs_points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    add_card(s4, 6.9, 1.7, 5.6, 5.2, "Live Catering Problem Formulation", ACCENT_CYAN)
    tb = s4.shapes.add_textbox(Inches(7.2), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    prob_points = [
        ("State Representation", "frozenset of recipe ingredients (e.g. {'Chicken', 'Peanut Butter', 'Soy Sauce'})."),
        ("Goal Condition", "is_goal(state) returns True when no ingredient contains any target client allergens."),
        ("Live Event Scenario", "TechCorp Summit: Keynote speaker with severe peanut anaphylaxis requested Thai Satay Skewers."),
        ("Optimal AI Solution", "Peanut Butter  -->  Sunflower Seed Butter (1 swap, 2 nodes expanded, 0.12 ms). Original dish flavor retained!")
    ]
    for i, (title, desc) in enumerate(prob_points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 5: MODULE B — DEPTH-FIRST SEARCH WITH PRUNING
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_header(s5, "Module B: Depth-First Search (DFS) with Early Pruning", "LAB 05: UNINFORMED SEARCH & BACKTRACKING (LIFO STACK)")

    add_card(s5, 0.8, 1.7, 5.6, 5.2, "Algorithmic Mechanics (dfs.py)", AMBER)
    tb = s5.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    dfs_points = [
        ("LIFO Frontier (stack.pop())", "Explores deepest branches first. Linear memory footprint O(b * m) vs BFS exponential O(b^d)."),
        ("Branch-and-Bound Pruning", "Evaluates problem.prune(child_state) before pushing child to stack. Avoids expanding doomed subtrees."),
        ("Multi-Solution Exploration", "Configurable find_all=True collects multiple valid client quotation packages ranked by budget utilization."),
        ("Completeness in Finite Trees", "Menu problem depth is strictly bound by courses (depth = 3), guaranteeing termination.")
    ]
    for i, (title, desc) in enumerate(dfs_points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    add_card(s5, 6.9, 1.7, 5.6, 5.2, "Menu Constraints & Pruning Criteria", EMERALD)
    tb = s5.shapes.add_textbox(Inches(7.2), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    prune_points = [
        ("State Representation", "Ordered tuple of selected Dish objects: (Starter, Main, Dessert)."),
        ("1. Budget Pruning", "if running_price > max_budget: return True. Truncates all child course combinations immediately."),
        ("2. Dietary Reachability Pruning", "if veg_so_far + remaining_slots < min_vegetarian: return True. Discards branches that cannot physically fulfill quotas."),
        ("Live Event Scenario", "Vance Board Dinner: $44/head budget, strictly >= 2 Gluten-Free dishes. Solves in 1.4 ms with 78% pruning reduction.")
    ]
    for i, (title, desc) in enumerate(prune_points):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {title}: "
        p.font.bold = True
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(12)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 6: EXPERIMENTAL BENCHMARK & COMPARISON
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_header(s6, "Experimental Benchmarking & Complexity Analysis")

    # Add comparison table
    rows, cols = 4, 5
    table_shape = s6.shapes.add_table(rows, cols, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.4))
    table = table_shape.table
    table.columns[0].width = Inches(2.7)
    table.columns[1].width = Inches(2.1)
    table.columns[2].width = Inches(2.1)
    table.columns[3].width = Inches(2.4)
    table.columns[4].width = Inches(2.4)

    headers = ["Algorithm Mode", "Frontier DS", "Nodes Expanded", "Space Complexity", "Optimality"]
    data_rows = [
        ["BFS (Allergen Path)", "FIFO Queue (deque)", "1 – 4 nodes", "O(b^d) Exponential", "Guaranteed (Unit Cost)"],
        ["Standard DFS (Menu)", "LIFO Stack (list)", "28 – 45 nodes", "O(b * m) Linear", "First Found (Not Opt.)"],
        ["DFS with Pruning (Menu)", "LIFO Stack + Pruning", "6 – 12 nodes (-73%)", "O(b * m) Linear", "Best Ranked in Budget"]
    ]

    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 41, 59)
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = ACCENT_CYAN
        p.alignment = PP_ALIGN.CENTER

    for row_idx, row_vals in enumerate(data_rows):
        for col_idx, val in enumerate(row_vals):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN if col_idx == 0 else TEXT_MUTED
            p.alignment = PP_ALIGN.CENTER

    # Lower takeaway cards
    add_card(s6, 0.8, 4.5, 5.6, 2.4, "Why BFS for Allergen Safe-Paths?", PRIMARY)
    tb = s6.shapes.add_textbox(Inches(1.1), Inches(5.1), Inches(5.0), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "In kitchen operations, each substitution alters recipe flavor and kitchen prep. BFS ensures we find the solution that requires the minimum number of ingredient changes before exploring deeper alternatives."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    add_card(s6, 6.9, 4.5, 5.6, 2.4, "Why DFS for Multi-Course Packages?", EMERALD)
    tb = s6.shapes.add_textbox(Inches(7.2), Inches(5.1), Inches(5.0), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Menu planning has a strict tree depth (Starter -> Main -> Dessert = 3). DFS navigates straight down to full meal candidate solutions, and early pruning drops node expansions by over 70%."
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 7: LIVE DEMONSTRATION & ARCHITECTURE
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_header(s7, "System Architecture & Live Demonstration Flow")

    add_card(s7, 0.8, 1.7, 5.6, 5.2, "Codebase Architecture (Pure Python)", ACCENT_CYAN)
    tb = s7.shapes.add_textbox(Inches(1.1), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    arch_files = [
        ("app.py", "Modern Next.js-inspired dark UI powered by Streamlit. Zero frontend JS build."),
        ("data.py", "In-memory knowledge graph of 18+ ingredients, allergen sets, and client events."),
        ("ai_engine/search/core.py", "Russell & Norvig Problem, Node, and SearchResult contracts."),
        ("ai_engine/search/bfs.py", "Queue-based breadth-first traversal implementation."),
        ("ai_engine/search/dfs.py", "Stack-based depth-first traversal with hook-based branch pruning."),
        ("ai_engine/problems/", "Problem formulations: allergen_substitution.py & menu_constraints.py.")
    ]
    for i, (fn, desc) in enumerate(arch_files):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {fn}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(8)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_MUTED

    add_card(s7, 6.9, 1.7, 5.6, 5.2, "Live Demo Scenarios to Present", PRIMARY)
    tb = s7.shapes.add_textbox(Inches(7.2), Inches(2.4), Inches(5.0), Inches(4.2))
    tf = tb.text_frame
    tf.word_wrap = True
    demos = [
        ("Scenario 1: TechCorp Summit", "Eliminate severe peanut anaphylaxis from Thai Satay Skewers via BFS in 1 swap."),
        ("Scenario 2: Vance Board Dinner", "Strict celiac safety (>= 2 Gluten-Free dishes) under $44/head via Pruned DFS in 1.4 ms."),
        ("Scenario 3: Greenfield BioTech Gala", "Dairy-Free dessert adaptation with multi-solution package ranking under $42/head."),
        ("Interactive Control", "Toggle pruning live to demonstrate exponential node explosion vs streamlined search.")
    ]
    for i, (fn, desc) in enumerate(demos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = f"• {fn}: "
        p.font.bold = True
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN
        if i > 0:
            p.space_before = Pt(12)
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.size = Pt(11)
        run.font.color.rgb = TEXT_MUTED

    # ==========================================
    # SLIDE 8: SUMMARY & Q&A
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)

    box = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.5), Inches(1.2), Inches(10.333), Inches(5.1))
    box.fill.solid()
    box.fill.fore_color.rgb = CARD_BG
    box.line.color.rgb = PRIMARY
    box.line.width = Pt(1.5)

    tb = s8.shapes.add_textbox(Inches(2.0), Inches(1.8), Inches(9.333), Inches(3.9))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "Key Takeaways & Conclusion"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_MAIN
    p.alignment = PP_ALIGN.CENTER

    summary_pts = [
        "1. Classical AI Solves Real Problems: Abstract search translates directly to catering safety & cost efficiency.",
        "2. Algorithmic Matching Matters: BFS guarantees fewest swaps; DFS + Pruning controls combinatorial explosion.",
        "3. Pure Python Simplicity: Clean Russell & Norvig structure without framework overhead.",
        "4. Ready for Live Evaluation: Interactive dashboard validates all theoretical concepts."
    ]
    for pt in summary_pts:
        p = tf.add_paragraph()
        p.text = pt
        p.font.size = Pt(14)
        p.font.color.rgb = ACCENT_CYAN
        p.space_before = Pt(12)
        p.alignment = PP_ALIGN.CENTER

    p_qa = tf.add_paragraph()
    p_qa.text = "\nThank You! Open for Questions."
    p_qa.font.size = Pt(20)
    p_qa.font.bold = True
    p_qa.font.color.rgb = EMERALD
    p_qa.space_before = Pt(18)
    p_qa.alignment = PP_ALIGN.CENTER

    # Save
    out_path = r"e:\uni\6th semester\ai lab\semester project\CaterIQ_Presentation_Rayyan_Mustafa_2312335.pptx"
    prs.save(out_path)
    print("SUCCESS: Saved presentation to", out_path)

if __name__ == "__main__":
    create_deck()
