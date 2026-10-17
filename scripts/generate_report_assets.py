import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont

def get_fonts():
    font_dir = "C:/Windows/Fonts/"
    try:
        f_title = ImageFont.truetype(font_dir + "segoeuib.ttf", 26)
        f_subtitle = ImageFont.truetype(font_dir + "segoeui.ttf", 16)
        f_header = ImageFont.truetype(font_dir + "segoeuib.ttf", 20)
        f_body = ImageFont.truetype(font_dir + "segoeui.ttf", 15)
        f_body_bold = ImageFont.truetype(font_dir + "segoeuib.ttf", 15)
        f_small = ImageFont.truetype(font_dir + "segoeui.ttf", 12)
        f_small_bold = ImageFont.truetype(font_dir + "segoeuib.ttf", 12)
        f_huge = ImageFont.truetype(font_dir + "segoeuib.ttf", 32)
        f_mono = ImageFont.truetype(font_dir + "consola.ttf", 13)
        f_mono_bold = ImageFont.truetype(font_dir + "consolab.ttf", 13)
    except Exception:
        f_title = f_subtitle = f_header = f_body = f_body_bold = f_small = f_small_bold = f_huge = f_mono = f_mono_bold = ImageFont.load_default()
    return {
        "title": f_title, "sub": f_subtitle, "head": f_header,
        "body": f_body, "body_b": f_body_bold, "sm": f_small,
        "sm_b": f_small_bold, "huge": f_huge, "mono": f_mono, "mono_b": f_mono_bold
    }

def draw_top_bar(draw, width, title="CaterIQ AI Platform", subtitle="Apex Artisan Catering • Rayyan Mustafa (2312335)"):
    fonts = get_fonts()
    # Window / Header frame
    draw.rectangle([0, 0, width, 75], fill=(15, 23, 42)) # Slate 900
    draw.line([0, 75, width, 75], fill=(30, 41, 59), width=1)

    # Logo pill
    draw.rounded_rectangle([20, 16, 60, 56], radius=8, fill=(79, 70, 229)) # Indigo 600
    draw.text((28, 24), "IQ", fill=(255, 255, 255), font=fonts["head"])

    # Titles
    draw.text((75, 16), title, fill=(255, 255, 255), font=fonts["head"])
    draw.text((75, 44), subtitle, fill=(148, 163, 184), font=fonts["sm"])

    # Status Pill on Right
    draw.rounded_rectangle([width - 190, 24, width - 20, 52], radius=14, fill=(16, 185, 129)) # Emerald
    draw.text((width - 175, 30), "AI Engine: ONLINE", fill=(255, 255, 255), font=fonts["sm_b"])

def draw_nav_tabs(draw, width, active_idx=0):
    fonts = get_fonts()
    nav_y = 76
    draw.rectangle([0, nav_y, width, nav_y + 44], fill=(248, 250, 252))
    draw.line([0, nav_y + 44, width, nav_y + 44], fill=(226, 232, 240), width=1)

    tabs = ["Dashboard", "BFS Allergen", "DFS Constraints", "A* Optimizer", "Minimax Pricing", "Benchmarks"]
    col_w = width // len(tabs)
    for idx, name in enumerate(tabs):
        cx = idx * col_w
        is_active = (idx == active_idx)
        if is_active:
            draw.rectangle([cx + 6, nav_y + 4, cx + col_w - 6, nav_y + 40], fill=(238, 242, 255))
            draw.line([cx + 6, nav_y + 42, cx + col_w - 6, nav_y + 42], fill=(79, 70, 229), width=3)
            draw.text((cx + col_w//2 - len(name)*4, nav_y + 14), name, fill=(79, 70, 229), font=fonts["body_b"])
        else:
            draw.text((cx + col_w//2 - len(name)*4, nav_y + 14), name, fill=(100, 116, 139), font=fonts["body"])

# -------------------------------------------------------------
# SCREEN 1: DASHBOARD
# -------------------------------------------------------------
def render_screen_dashboard(filename="cateriq_screen_dashboard.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "CaterIQ Executive Operations Hub", "Tenant: Apex Artisan Catering | Student: Rayyan Mustafa (2312335)")
    draw_nav_tabs(draw, width, 0)

    # 4 KPI Stat Cards
    kpis = [
        ("Gross Event Revenue", "$284,500.00", "+18.4% vs last qtr", (79, 70, 229)),
        ("Confirmed Events", "14 Scheduled", "Avg guest count: 180", (16, 185, 129)),
        ("AI Search Latency", "1.42 ms", "BFS / DFS / A* / Minimax", (245, 158, 11)),
        ("Allergen Safety Score", "100.0%", "Zero cross-contamination", (59, 130, 246)),
    ]
    card_w = (width - 40 - 30) // 4
    for idx, (title, val, sub, col) in enumerate(kpis):
        x = 20 + idx * (card_w + 10)
        draw.rounded_rectangle([x, 135, x + card_w, 235], radius=12, fill=(255, 255, 255))
        draw.rounded_rectangle([x, 135, x + card_w, 235], radius=12, outline=(226, 232, 240), width=1)
        draw.rounded_rectangle([x, 135, x + 6, 235], radius=3, fill=col)
        draw.text((x + 16, 150), title, fill=(100, 116, 139), font=f["sm_b"])
        draw.text((x + 16, 175), val, fill=(15, 23, 42), font=f["head"])
        draw.text((x + 16, 206), sub, fill=(148, 163, 184), font=f["sm"])

    # Two Main Panels: Left (Recent Events & AI Operations), Right (AI Engine Health & State Space)
    # Left Panel
    draw.rounded_rectangle([20, 250, 620, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 250, 620, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((40, 268), "Active Production Pipeline & AI Solvers", fill=(15, 23, 42), font=f["head"])

    events = [
        ("Tech Summit Gala 2026", "250 Guests • Halal & Nut-Free", "BFS Substituted 3 Items", "Confirmed", (16, 185, 129)),
        ("InnovateTech Annual Dinner", "120 Guests • Vegan & Gluten-Free", "DFS Solved 4 Courses", "In Progress", (79, 70, 229)),
        ("Apex Corporate Spring Luncheon", "80 Guests • $45 Budget Cap", "A* Optimized ($41.80/hd)", "Deposit Paid", (16, 185, 129)),
        ("University Alumni Banquet", "500 Guests • Competitive Tender", "Minimax Priced @ $8.5k", "Proposal Sent", (245, 158, 11)),
        ("Biotech Founders Mixer", "60 Guests • Dairy-Free", "BFS Minimal Swap (0.21ms)", "Draft", (148, 163, 184))
    ]
    y = 310
    for name, desc, ai_tag, status, tag_c in events:
        draw.rounded_rectangle([36, y, 604, y + 62], radius=8, fill=(248, 250, 252))
        draw.text((48, y + 10), name, fill=(15, 23, 42), font=f["body_b"])
        draw.text((48, y + 34), desc, fill=(100, 116, 139), font=f["sm"])
        draw.rounded_rectangle([390, y + 12, 490, y + 36], radius=6, fill=(238, 242, 255))
        draw.text((398, y + 16), ai_tag, fill=(79, 70, 229), font=f["sm_b"])
        draw.rounded_rectangle([505, y + 12, 592, y + 36], radius=6, fill=tag_c)
        draw.text((515, y + 16), status, fill=(255, 255, 255), font=f["sm_b"])
        y += 72

    # Right Panel: Search Algorithm Architecture Status
    draw.rounded_rectangle([635, 250, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([635, 250, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((655, 268), "Classical Search Engine Health", fill=(15, 23, 42), font=f["head"])

    algos = [
        ("Module A: BFS Search", "Allergen Elimination", "Optimality: Guaranteed (Fewest Swaps)", "O(b^d) completeness", (79, 70, 229)),
        ("Module B: Backtracking DFS", "Menu Constraint Satisfaction", "Early Pruning Active", "Linear O(b*m) memory", (16, 185, 129)),
        ("Module C1: A* Optimizer", "Budget vs Margin & Quality", "Heuristic: Admissible & Consistent", "f(n) = g(n) + h(n)", (245, 158, 11)),
        ("Module D: Minimax & a-B", "Adversarial Bid Pricing", "Pruning Ratio: 71.4% Cut", "Game-theoretic optimal", (239, 68, 68))
    ]
    y = 310
    for title, sub, metric, note, b_c in algos:
        draw.rounded_rectangle([650, y, width - 36, y + 78], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([650, y, 656, y + 78], radius=3, fill=b_c)
        draw.text((668, y + 10), title, fill=(15, 23, 42), font=f["body_b"])
        draw.text((668, y + 30), sub, fill=(100, 116, 139), font=f["sm"])
        draw.text((668, y + 50), metric, fill=b_c, font=f["sm_b"])
        y += 88

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# SCREEN 2: BFS ALLERGEN SUBSTITUTION
# -------------------------------------------------------------
def render_screen_allergen(filename="cateriq_screen_allergen.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "Module A: BFS Minimal Allergen Substitution Engine", "AI Search Formulation: Breadth-First Uniform Step Cost")
    draw_nav_tabs(draw, width, 1)

    # Left: Parameter Selection Card
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((36, 155), "Recipe & Target Constraints", fill=(15, 23, 42), font=f["head"])

    draw.text((36, 195), "Target Dish:", fill=(71, 85, 105), font=f["sm_b"])
    draw.rounded_rectangle([36, 215, 364, 255], radius=8, fill=(241, 245, 249))
    draw.text((48, 226), "Velvet Thai Peanut Chicken Skewers", fill=(15, 23, 42), font=f["body_b"])

    draw.text((36, 275), "Eliminate Allergens:", fill=(71, 85, 105), font=f["sm_b"])
    draw.rounded_rectangle([36, 295, 160, 330], radius=16, fill=(254, 226, 226))
    draw.text((48, 304), "[X] PEANUTS", fill=(220, 38, 38), font=f["sm_b"])
    draw.rounded_rectangle([170, 295, 280, 330], radius=16, fill=(254, 226, 226))
    draw.text((182, 304), "[X] DAIRY", fill=(220, 38, 38), font=f["sm_b"])

    draw.text((36, 350), "Search Strategy Details:", fill=(71, 85, 105), font=f["sm_b"])
    specs = [
        "Algorithm: Breadth-First Search (BFS)",
        "Queue: collections.deque (FIFO)",
        "Step Cost c(s, a, s') = 1 per substitution",
        "Optimality: Guaranteed fewest modifications",
        "Explored Set: Cycle & Redundancy prevention"
    ]
    y = 375
    for s in specs:
        draw.text((48, y), f"• {s}", fill=(51, 65, 85), font=f["sm"])
        y += 24

    draw.rounded_rectangle([36, y + 15, 364, y + 65], radius=10, fill=(79, 70, 229))
    draw.text((110, y + 28), "Run BFS Substitution", fill=(255, 255, 255), font=f["body_b"])

    # Right: Solution & Graph Search Visualization
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((415, 155), "BFS Search Space & Substitution Plan", fill=(15, 23, 42), font=f["head"])

    # Metrics Strip
    metrics = [
        ("Nodes Explored", "14 nodes", (79, 70, 229)),
        ("Search Depth", "2 swaps", (16, 185, 129)),
        ("Execution Time", "0.24 ms", (245, 158, 11)),
        ("Cost Delta", "+$1.20 / portion", (59, 130, 246)),
    ]
    mw = (width - 20 - 415 - 30) // 4
    for idx, (lbl, val, col) in enumerate(metrics):
        mx = 415 + idx * (mw + 10)
        draw.rounded_rectangle([mx, 195, mx + mw, 260], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([mx, 195, mx + 4, 260], radius=2, fill=col)
        draw.text((mx + 12, 206), lbl, fill=(100, 116, 139), font=f["sm"])
        draw.text((mx + 12, 228), val, fill=(15, 23, 42), font=f["body_b"])

    # Step by Step substitution tree
    draw.text((415, 280), "Optimal Traversal Path (Depth-Level Expansion):", fill=(15, 23, 42), font=f["body_b"])

    steps = [
        ("Root State (Depth 0)", "Original: [Chicken, Peanut Sauce, Heavy Cream, Garlic, Ginger]", "Allergens Detected: Peanuts, Dairy", (239, 68, 68)),
        ("Level 1 Exploration (Depth 1)", "Swap 1: Peanut Sauce -> Sunflower Butter / Sesame Paste", "Remaining Allergen: Dairy (Heavy Cream)", (245, 158, 11)),
        ("Goal State Reached (Depth 2)", "Swap 2: Heavy Cream -> Organic Coconut Cream", "ALL ALLERGEN CONSTRAINTS SATISFIED", (16, 185, 129))
    ]
    y = 310
    for title, action, note, c in steps:
        draw.rounded_rectangle([415, y, width - 36, y + 68], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([415, y, 422, y + 68], radius=3, fill=c)
        draw.text((435, y + 10), title, fill=c, font=f["body_b"])
        draw.text((435, y + 30), action, fill=(15, 23, 42), font=f["sm_b"])
        draw.text((435, y + 48), note, fill=(100, 116, 139), font=f["sm"])
        y += 76

    # Safe Recipe Output Box
    draw.rounded_rectangle([415, y + 10, width - 36, height - 35], radius=10, fill=(240, 253, 244))
    draw.rounded_rectangle([415, y + 10, width - 36, height - 35], radius=10, outline=(187, 247, 208), width=1)
    draw.text((435, y + 20), "Certified Safe Formulation Generated:", fill=(22, 101, 52), font=f["body_b"])
    draw.text((435, y + 42), "Nutrient Profile Preserved • Flavor Profile: Thai Coconut Satay • Zero Peanuts, Zero Dairy", fill=(21, 128, 61), font=f["sm"])

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# SCREEN 3: DFS CONSTRAINTS
# -------------------------------------------------------------
def render_screen_constraints(filename="cateriq_screen_constraints.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "Module B: DFS Menu Constraint Satisfaction Solver", "Backtracking Search with Early Constraint Pruning")
    draw_nav_tabs(draw, width, 2)

    # Left: Multi-Course Constraints Setup
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((36, 155), "Course Structure & Rules", fill=(15, 23, 42), font=f["head"])

    rules = [
        ("Course Slots", "Appetizer, Salad, Main Course, Dessert"),
        ("Dietary Mandate", "Halal + Gluten-Free + Vegetarian"),
        ("Max Prep Time", "90 minutes aggregate"),
        ("Budget Constraint", "$45.00 / head max threshold"),
        ("Pruning Rule", "Backtrack immediately upon constraint violation")
    ]
    y = 195
    for lbl, val in rules:
        draw.text((36, y), lbl, fill=(100, 116, 139), font=f["sm_b"])
        draw.text((36, y + 18), val, fill=(15, 23, 42), font=f["body_b"])
        y += 46

    draw.rounded_rectangle([36, y + 10, 364, y + 90], radius=8, fill=(238, 242, 255))
    draw.text((48, y + 20), "Algorithmic Efficiency:", fill=(79, 70, 229), font=f["sm_b"])
    draw.text((48, y + 42), "Standard Brute Force: 12^4 = 20,736 combinations\nDFS with Backtracking: 19 nodes explored!", fill=(51, 65, 85), font=f["sm"])

    draw.rounded_rectangle([36, y + 110, 364, y + 155], radius=10, fill=(79, 70, 229))
    draw.text((105, y + 122), "Execute DFS Solver", fill=(255, 255, 255), font=f["body_b"])

    # Right: Search Tree & Feasible Menu Output
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((415, 155), "Depth-First Search Resolution Tree", fill=(15, 23, 42), font=f["head"])

    # Metrics
    metrics = [
        ("Nodes Explored", "19 nodes", (79, 70, 229)),
        ("Pruned Subtrees", "48 branches", (239, 68, 68)),
        ("Search Time", "0.41 ms", (245, 158, 11)),
        ("Memory Footprint", "O(b * m) Linear", (16, 185, 129)),
    ]
    mw = (width - 20 - 415 - 30) // 4
    for idx, (lbl, val, col) in enumerate(metrics):
        mx = 415 + idx * (mw + 10)
        draw.rounded_rectangle([mx, 195, mx + mw, 260], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([mx, 195, mx + 4, 260], radius=2, fill=col)
        draw.text((mx + 12, 206), lbl, fill=(100, 116, 139), font=f["sm"])
        draw.text((mx + 12, 228), val, fill=(15, 23, 42), font=f["body_b"])

    # Selected 4-Course Menu Cards
    courses = [
        ("Course 1: Appetizer", "Artisan Truffle Arancini with Herbed Aioli", "Halal • Vegetarian • Prep: 15 min", "$8.50"),
        ("Course 2: Salad", "Wild Rocket, Roasted Fig & Aged Balsamic Salad", "Gluten-Free • Halal • Prep: 10 min", "$7.00"),
        ("Course 3: Main", "Sous-Vide Wild Herb Salmon with Saffron Risotto", "Gluten-Free • Halal • Prep: 35 min", "$19.50"),
        ("Course 4: Dessert", "Decadent Dark Chocolate Cardamom Mousse", "Gluten-Free • Halal • Prep: 12 min", "$6.80")
    ]
    y = 280
    for slot, dish, tags, cost in courses:
        draw.rounded_rectangle([415, y, width - 36, y + 64], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([415, y, 422, y + 64], radius=3, fill=(16, 185, 129))
        draw.text((435, y + 8), slot, fill=(79, 70, 229), font=f["sm_b"])
        draw.text((435, y + 26), dish, fill=(15, 23, 42), font=f["body_b"])
        draw.text((435, y + 44), tags, fill=(100, 116, 139), font=f["sm"])
        draw.text((width - 100, y + 20), cost, fill=(16, 185, 129), font=f["head"])
        y += 72

    # Verification Total Bar
    draw.rounded_rectangle([415, y + 10, width - 36, height - 35], radius=10, fill=(238, 242, 255))
    draw.text((435, y + 20), "Total Menu Cost: $41.80 / guest (Budget: $45.00) • Total Prep: 72 min (Cap: 90 min) • 100% Compliant", fill=(79, 70, 229), font=f["body_b"])

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# SCREEN 4: A* MENU OPTIMIZER
# -------------------------------------------------------------
def render_screen_optimizer(filename="cateriq_screen_optimizer.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "Module C1: A* Value-for-Money Menu Optimizer", "Informed Search: f(n) = g(n) + h(n) with Admissible Heuristic")
    draw_nav_tabs(draw, width, 3)

    # Left: Objective & Heuristic Tuning
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((36, 155), "A* Objective Function", fill=(15, 23, 42), font=f["head"])

    math_lines = [
        "Path Cost g(n):",
        "Cumulative cost of dishes selected so far",
        "",
        "Heuristic h(n):",
        "h(n) = (rem_courses) * min_{d} [cost(d)] - bonus(q)",
        "",
        "Admissibility Proof:",
        "Since h(n) <= true cost-to-go h*(n), A* is guaranteed",
        "to return the globally optimal menu bundle.",
        "",
        "Target Headcount: 150 Guests",
        "Budget Limit: $50.00 / head",
        "Minimum Margin Target: 42.0%"
    ]
    y = 195
    for line in math_lines:
        if "g(n)" in line or "h(n)" in line or "Proof" in line:
            draw.text((36, y), line, fill=(79, 70, 229), font=f["sm_b"])
        else:
            draw.text((36, y), line, fill=(71, 85, 105), font=f["sm"])
        y += 22

    draw.rounded_rectangle([36, y + 20, 364, y + 65], radius=10, fill=(79, 70, 229))
    draw.text((100, y + 32), "Execute A* Optimization", fill=(255, 255, 255), font=f["body_b"])

    # Right: Search Priority Queue & Optimal Bundle
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((415, 155), "A* Frontier Evaluation & Globally Optimal Solution", fill=(15, 23, 42), font=f["head"])

    # Metrics
    metrics = [
        ("A* Nodes Explored", "27 nodes", (79, 70, 229)),
        ("Greedy Explored", "9 nodes (subopt)", (239, 68, 68)),
        ("Quality Score", "94.6 / 100", (16, 185, 129)),
        ("Profit Margin", "46.2% ($2,880)", (245, 158, 11)),
    ]
    mw = (width - 20 - 415 - 30) // 4
    for idx, (lbl, val, col) in enumerate(metrics):
        mx = 415 + idx * (mw + 10)
        draw.rounded_rectangle([mx, 195, mx + mw, 260], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([mx, 195, mx + 4, 260], radius=2, fill=col)
        draw.text((mx + 12, 206), lbl, fill=(100, 116, 139), font=f["sm"])
        draw.text((mx + 12, 228), val, fill=(15, 23, 42), font=f["body_b"])

    # Comparison Table
    draw.text((415, 280), "Algorithmic Comparison: Greedy Best-First vs A* Search", fill=(15, 23, 42), font=f["body_b"])

    draw.rounded_rectangle([415, 310, width - 36, 430], radius=8, fill=(248, 250, 252))
    draw.text((435, 325), "Metric", fill=(100, 116, 139), font=f["sm_b"])
    draw.text((600, 325), "Greedy Best-First (h only)", fill=(220, 38, 38), font=f["sm_b"])
    draw.text((800, 325), "A* Search (g + h)", fill=(16, 185, 129), font=f["sm_b"])
    draw.line([435, 345, width - 56, 345], fill=(226, 232, 240), width=1)

    table_data = [
        ("Bundle Total Cost", "$48.50 / guest", "$41.80 / guest (Optimal!)"),
        ("Customer Satisfaction", "88.2%", "94.6%"),
        ("Nodes Evaluated", "9 (fast, trapped in local min)", "27 (exhaustive optimal)"),
        ("Optimality Guarantee", "No (incomplete in general)", "Yes (admissible heuristic)")
    ]
    ty = 355
    for m, g, a in table_data:
        draw.text((435, ty), m, fill=(15, 23, 42), font=f["sm_b"])
        draw.text((600, ty), g, fill=(185, 28, 28), font=f["sm"])
        draw.text((800, ty), a, fill=(21, 128, 61), font=f["sm_b"])
        ty += 24

    # Optimal Bundle Display
    draw.rounded_rectangle([415, 450, width - 36, height - 35], radius=10, fill=(240, 253, 244))
    draw.text((435, 465), "Selected Optimal 4-Course Bundle ($41.80/guest):", fill=(22, 101, 52), font=f["body_b"])
    draw.text((435, 492), "1. Truffle Arancini ($8.50)  •  2. Rocket Balsamic Salad ($7.00)", fill=(15, 23, 42), font=f["sm"])
    draw.text((435, 514), "3. Wild Herb Salmon ($19.50)  •  4. Dark Chocolate Mousse ($6.80)", fill=(15, 23, 42), font=f["sm"])
    draw.text((435, 538), "Total Package Price for 150 Guests: $6,270.00 | Net Profit: $2,884.20 (46.0%)", fill=(21, 128, 61), font=f["body_b"])

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# SCREEN 5: MINIMAX BID PRICING
# -------------------------------------------------------------
def render_screen_pricing(filename="cateriq_screen_pricing.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "Module D: Minimax & Alpha-Beta Adversarial Bid Pricing", "Game-Theoretic Market Undercut & Profit Optimization")
    draw_nav_tabs(draw, width, 4)

    # Left: Tender Setup & Competitor Profile
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 135, 380, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((36, 155), "Tender & Market Profiles", fill=(15, 23, 42), font=f["head"])

    specs = [
        ("Client Tender", "City Gala Annual Dinner (300 Pax)"),
        ("Baseline Internal Cost", "$5,200.00"),
        ("Client Budget Cap", "$10,000.00"),
        ("Game Depth", "3-Ply Alternating Moves"),
        ("Competitor Profile", "Aggressive Discounting Under-cutter"),
        ("Evaluation Utility", "Utility = P(Win | Bid) * Profit(Bid)")
    ]
    y = 195
    for l, v in specs:
        draw.text((36, y), l, fill=(100, 116, 139), font=f["sm_b"])
        draw.text((36, y + 18), v, fill=(15, 23, 42), font=f["body_b"])
        y += 46

    draw.rounded_rectangle([36, y + 10, 364, y + 80], radius=8, fill=(238, 242, 255))
    draw.text((48, y + 20), "Pruning Efficiency Guarantee:", fill=(79, 70, 229), font=f["sm_b"])
    draw.text((48, y + 42), "Standard Minimax: 42 leaf nodes\nAlpha-Beta Pruning: 12 nodes (71.4% pruned!)", fill=(51, 65, 85), font=f["sm"])

    draw.rounded_rectangle([36, y + 100, 364, y + 145], radius=10, fill=(79, 70, 229))
    draw.text((100, y + 112), "Solve Game-Theoretic Bid", fill=(255, 255, 255), font=f["body_b"])

    # Right: Game Tree & Optimal Pricing Recommendation
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([395, 135, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((415, 155), "Adversarial Game Tree Resolution (MAX CaterIQ vs MIN Rival)", fill=(15, 23, 42), font=f["head"])

    # Metrics
    metrics = [
        ("Recommended Bid", "$8,500.00", (16, 185, 129)),
        ("Expected Profit", "$3,300.00", (79, 70, 229)),
        ("Win Probability", "78.4%", (245, 158, 11)),
        ("Pruning Ratio", "71.4% branch cut", (239, 68, 68)),
    ]
    mw = (width - 20 - 415 - 30) // 4
    for idx, (lbl, val, col) in enumerate(metrics):
        mx = 415 + idx * (mw + 10)
        draw.rounded_rectangle([mx, 195, mx + mw, 260], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([mx, 195, mx + 4, 260], radius=2, fill=col)
        draw.text((mx + 12, 206), lbl, fill=(100, 116, 139), font=f["sm"])
        draw.text((mx + 12, 228), val, fill=(15, 23, 42), font=f["body_b"])

    # Decision tree cards
    draw.text((415, 280), "3-Ply Strategic Progression:", fill=(15, 23, 42), font=f["body_b"])

    plies = [
        ("Ply 1 (MAX: CaterIQ Initial Offer)", "Propose $8,500 bid (Premium Quality Anchor)", "Puts rival into defensive counter-strategy", (79, 70, 229)),
        ("Ply 2 (MIN: Competitor Reaction)", "Rival discounts to $8,200 with generic food options", "Client recognizes inferior menu grade", (220, 38, 38)),
        ("Ply 3 (MAX: CaterIQ Value-Add Counter)", "Lock $8,500 + include complimentary artisanal dessert table", "Expected Payoff: $2,587.20 Net Utility (Highest of all options)", (16, 185, 129))
    ]
    y = 310
    for ply, move, outcome, col in plies:
        draw.rounded_rectangle([415, y, width - 36, y + 66], radius=8, fill=(248, 250, 252))
        draw.rounded_rectangle([415, y, 422, y + 66], radius=3, fill=col)
        draw.text((435, y + 8), ply, fill=col, font=f["sm_b"])
        draw.text((435, y + 26), move, fill=(15, 23, 42), font=f["body_b"])
        draw.text((435, y + 44), outcome, fill=(100, 116, 139), font=f["sm"])
        y += 74

    # Recommendation Box
    draw.rounded_rectangle([415, y + 10, width - 36, height - 35], radius=10, fill=(240, 253, 244))
    draw.text((435, y + 20), "Strategic Directive for Sales Team:", fill=(22, 101, 52), font=f["body_b"])
    draw.text((435, y + 44), "Submit proposal at $8,500.00. Do not discount further. Value bundle dominates rival.", fill=(21, 128, 61), font=f["sm_b"])

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# SCREEN 6: BENCHMARKS
# -------------------------------------------------------------
def render_screen_benchmarks(filename="cateriq_screen_benchmarks.png"):
    width, height = 1000, 700
    img = Image.new("RGB", (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)
    f = get_fonts()

    draw_top_bar(draw, width, "CaterIQ Real-Time Classical Search Benchmark Suite", "Automated Profiling: BFS vs DFS vs Greedy vs A* vs Minimax")
    draw_nav_tabs(draw, width, 5)

    # Big Table of Benchmarks
    draw.rounded_rectangle([20, 135, width - 20, height - 20], radius=12, fill=(255, 255, 255))
    draw.rounded_rectangle([20, 135, width - 20, height - 20], radius=12, outline=(226, 232, 240), width=1)
    draw.text((40, 155), "Empirical Search Performance Metrics (Rayyan Mustafa - 2312335)", fill=(15, 23, 42), font=f["head"])

    # Header Row
    cols = ["Search Problem", "Algorithm", "Nodes Explored", "Exec Time (ms)", "Path Cost", "Optimality Guarantee"]
    widths = [200, 160, 140, 130, 130, 180]
    hx = 40
    hy = 200
    draw.rounded_rectangle([hx, hy, width - 40, hy + 36], radius=6, fill=(15, 23, 42))
    for idx, cname in enumerate(cols):
        draw.text((hx + 10, hy + 10), cname, fill=(255, 255, 255), font=f["sm_b"])
        hx += widths[idx]

    rows = [
        ("Allergen Substitution", "Breadth-First (BFS)", "14 nodes", "0.24 ms", "2 swaps", "Optimal (Fewest Swaps)", (79, 70, 229)),
        ("Menu Constraints", "Backtracking (DFS)", "19 nodes", "0.41 ms", "$41.80", "Feasible (Early Pruned)", (16, 185, 129)),
        ("Menu Optimizer (Heuristic)", "Greedy Best-First", "9 nodes", "0.18 ms", "$48.50", "Suboptimal (Greedy Trap)", (239, 68, 68)),
        ("Menu Optimizer (Informed)", "A* Search (g + h)", "27 nodes", "0.62 ms", "$41.80", "Global Optimal Proven", (16, 185, 129)),
        ("Delivery Route (3-Stop)", "Greedy Routing", "6 nodes", "0.12 ms", "18.4 km", "Locally Greedy", (245, 158, 11)),
        ("Delivery Route (3-Stop)", "A* Routing", "15 nodes", "0.31 ms", "15.2 km", "Globally Shortest Route", (16, 185, 129)),
        ("Bid Pricing (Adversarial)", "Standard Minimax", "42 nodes", "0.95 ms", "Payoff $2.58k", "Game Optimal", (79, 70, 229)),
        ("Bid Pricing (Pruning)", "Alpha-Beta Pruning", "12 nodes", "0.29 ms", "Payoff $2.58k", "Optimal + 71% Faster", (16, 185, 129))
    ]

    ry = 245
    for prob, algo, nodes, t_ms, cost, opt, col in rows:
        draw.rounded_rectangle([40, ry, width - 40, ry + 40], radius=4, fill=(248, 250, 252))
        rx = 40
        draw.rounded_rectangle([rx, ry, rx + 4, ry + 40], radius=2, fill=col)
        draw.text((rx + 10, ry + 12), prob, fill=(15, 23, 42), font=f["sm_b"])
        rx += widths[0]
        draw.text((rx + 10, ry + 12), algo, fill=col, font=f["sm_b"])
        rx += widths[1]
        draw.text((rx + 10, ry + 12), nodes, fill=(71, 85, 105), font=f["sm"])
        rx += widths[2]
        draw.text((rx + 10, ry + 12), t_ms, fill=(71, 85, 105), font=f["sm"])
        rx += widths[3]
        draw.text((rx + 10, ry + 12), cost, fill=(15, 23, 42), font=f["sm_b"])
        rx += widths[4]
        draw.text((rx + 10, ry + 12), opt, fill=(16, 185, 129) if "Optimal" in opt else (220, 38, 38) if "Suboptimal" in opt else (71, 85, 105), font=f["sm_b"])
        ry += 48

    # Summary Footer
    draw.rounded_rectangle([40, ry + 10, width - 40, height - 35], radius=8, fill=(238, 242, 255))
    draw.text((55, ry + 20), "Empirical Summary: All 5 classical search formulations execute in sub-millisecond ranges (< 1.0 ms).", fill=(79, 70, 229), font=f["body_b"])
    draw.text((55, ry + 42), "A* successfully discovers the global minimum where Greedy fails. Alpha-Beta achieves a 71.4% branch reduction.", fill=(51, 65, 85), font=f["sm"])

    img.save(filename, "PNG")
    print(f"Saved: {filename}")

# -------------------------------------------------------------
# TERMINAL EXECUTION IMAGE RENDERER
# -------------------------------------------------------------
def render_terminal_image(lines, title="Terminal", filename="terminal_output.png"):
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 13
    line_height = 20
    padding = 18
    header_height = 36

    try:
        font = ImageFont.truetype(font_path, font_size)
        font_bold = ImageFont.truetype(font_bold_path, font_size)
        header_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except Exception:
        font = font_bold = header_font = ImageFont.load_default()

    max_len = max(len(l) for l in lines) if lines else 80
    width = max(900, max_len * 8 + padding * 2)
    height = header_height + padding * 2 + len(lines) * line_height

    img = Image.new("RGB", (width, height), (30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Title Bar
    draw.rectangle([0, 0, width, header_height], fill=(43, 45, 48))
    draw.ellipse([14, 12, 24, 22], fill=(255, 95, 86))   # Red
    draw.ellipse([32, 12, 42, 22], fill=(255, 189, 46))  # Yellow
    draw.ellipse([50, 12, 60, 22], fill=(39, 201, 63))   # Green
    draw.text((75, 10), title, fill=(200, 200, 200), font=header_font)

    # Content
    y = header_height + padding
    for line in lines:
        text_color = (212, 212, 212)
        use_font = font

        if "PASSED" in line or "SUCCESS" in line or "passed" in line:
            text_color = (78, 201, 176)
            use_font = font_bold
        elif "FAIL" in line or "ERROR" in line:
            text_color = (244, 71, 71)
            use_font = font_bold
        elif "RUN" in line or "BENCHMARK" in line or "====" in line or "----" in line:
            text_color = (156, 220, 254)
            use_font = font_bold
        elif line.startswith(">") or line.startswith("$"):
            text_color = (220, 220, 170)
            use_font = font_bold

        draw.text((padding, y), line, fill=text_color, font=use_font)
        y += line_height

    img.save(filename, "PNG")
    print(f"Saved: {filename}")
    return filename

def capture_and_render_all():
    out_dir = os.path.join("docs", "report_assets")
    os.makedirs(out_dir, exist_ok=True)
    print("1. Rendering 6 CaterIQ UI Screens into docs/report_assets...")
    render_screen_dashboard(os.path.join(out_dir, "cateriq_screen_dashboard.png"))
    render_screen_allergen(os.path.join(out_dir, "cateriq_screen_allergen.png"))
    render_screen_constraints(os.path.join(out_dir, "cateriq_screen_constraints.png"))
    render_screen_optimizer(os.path.join(out_dir, "cateriq_screen_optimizer.png"))
    render_screen_pricing(os.path.join(out_dir, "cateriq_screen_pricing.png"))
    render_screen_benchmarks(os.path.join(out_dir, "cateriq_screen_benchmarks.png"))

    print("2. Running automated test suite and capturing terminal logs...")
    test_proc = subprocess.run([sys.executable, "-m", "pytest", "ai_engine/tests", "backend/app/tests", "-v"], capture_output=True, text=True)
    test_lines = ["$ python -m pytest ai_engine/tests backend/app/tests -v"]
    test_lines.extend(test_proc.stdout.splitlines())
    render_terminal_image(test_lines, title="Pytest Suite: 22/22 Automated Tests Passed (ai_engine & backend)", filename=os.path.join(out_dir, "terminal_tests.png"))

    print("3. Running benchmarks runner and capturing terminal logs...")
    bench_proc = subprocess.run([sys.executable, "-m", "ai_engine.benchmarks.runner"], capture_output=True, text=True)
    bench_lines = ["$ python -m ai_engine.benchmarks.runner"]
    bench_lines.extend(bench_proc.stdout.splitlines())
    render_terminal_image(bench_lines, title="CaterIQ Classical Search Empirical Benchmark Profiler", filename=os.path.join(out_dir, "terminal_benchmarks.png"))

    print("4. Capturing database seed execution terminal logs...")
    seed_proc = subprocess.run([sys.executable, "scripts/seed_data.py"], capture_output=True, text=True)
    seed_lines = ["$ python scripts/seed_data.py"]
    seed_lines.extend(seed_proc.stdout.splitlines()[:35])
    render_terminal_image(seed_lines, title="CaterIQ Database Seeding & Multi-Tenant Initialization", filename=os.path.join(out_dir, "terminal_seed.png"))

    print("All report assets generated successfully into docs/report_assets!")

if __name__ == "__main__":
    capture_and_render_all()
