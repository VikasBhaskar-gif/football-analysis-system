"""
scripts/generate_final_presentation.py
======================================
Generates the finalized, academically rigorous, and visually refined 16-slide presentation:
'Football_Tactical_Analytics_DBMS_Review_1.pptx'

Key Features:
- Visual Identity: Warm off-white canvas (#F8FAFC), Pitch Green (#059669 / #1B4332), Charcoal Slate (#0F172A), Cobalt (#2563EB).
- Zero resemblance to FLAVRD: No gold/bronze, no star emblem, clean modern typography.
- Authentic Project Evidence:
    * Real broadcast match frame with player tracking and scoreboard (game_39: Newcastle vs PSG).
    * Real FastAPI Swagger UI documentation.
    * 6-entity Relational ER diagram (TEAMS, MATCHES, PLAYERS, TACTICAL_RULES, MATCH_EVENTS, TACTICAL_SNAPSHOTS).
    * Executed SQLite query output tables matching exact database rows.
    * Emerald horizontal bar chart of pass distributions.
- Technical Rigor & SQLite Compatibility:
    * Explicit distinction between full FOOTPASS benchmark (102,992 events) and demonstration SQLite database (1,000 events).
    * Accurate SQLite DDL, DML, and functions.
    * SQLite ALTER TABLE specifics: ADD COLUMN, RENAME COLUMN, DROP COLUMN, and the 12-step Table-Rebuild Pattern for constraints.
    * Authors: Vikas Bhaskar (24BCT0149) & Jeevitesh Kandi (24BCE0350).
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "dbms_review_1")
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets")
PPTX_PATH = os.path.join(OUTPUT_DIR, "Football_Tactical_Analytics_DBMS_Review_1.pptx")

# ==========================================
# COLOR PALETTE
# ==========================================
PAGE_BG = RGBColor(248, 250, 252)        # #F8FAFC (Warm Off-White / Soft Slate)
CARD_BG = RGBColor(255, 255, 255)        # #FFFFFF (Crisp White Card Canvas)
CARD_BORDER = RGBColor(226, 232, 240)    # #E2E8F0 (Subtle Structural Border)
NAVY_DEEP = RGBColor(15, 23, 42)         # #0F172A (Deep Charcoal Slate - Primary Heading)
NAVY_SLATE = RGBColor(30, 41, 59)        # #1E293B (Secondary Dark Slate)
EMERALD_PITCH = RGBColor(5, 150, 105)    # #059669 (Pitch Green - Primary Accent)
EMERALD_FOREST = RGBColor(27, 67, 50)    # #1B4332 (Deep Forest Green Accent)
EMERALD_BRIGHT = RGBColor(16, 185, 129)  # #10B981 (Active Code / Keyword Accent)
COBALT_BLUE = RGBColor(37, 99, 235)      # #2563EB (Tech / Key Accent)
CYAN_ACCENT = RGBColor(2, 132, 199)      # #0284C7 (Secondary Blue Accent)
CODE_BG = RGBColor(15, 23, 42)           # #0F172A (Charcoal Monospace Panel)
CODE_BORDER = RGBColor(30, 41, 59)       # #1E293B
TEXT_HEAD = RGBColor(15, 23, 42)         # #0F172A
TEXT_BODY = RGBColor(71, 85, 105)        # #475569 (Neutral Slate)
TEXT_MUTED = RGBColor(100, 116, 139)     # #64748B (Muted Secondary)
TEXT_WHITE = RGBColor(255, 255, 255)     # #FFFFFF
TEXT_CODE = RGBColor(241, 245, 249)      # #F1F5F9 (Light Monospace Text)

FONT_HEAD = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide, color=PAGE_BG):
        fill = slide.background.fill
        fill.solid()
        fill.fore_color.rgb = color

    def add_header(slide, section_tag, title_text):
        # Top Emerald accent bar
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.35), Inches(0.8), Inches(0.06))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = EMERALD_PITCH
        top_bar.line.fill.background()

        # Section tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.48), Inches(11.5), Inches(0.3))
        tf = tag_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = section_tag.upper()
        p.font.name = FONT_HEAD
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = EMERALD_PITCH

        # Main Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.5), Inches(0.65))
        tf_t = t_box.text_frame
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p = tf_t.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_HEAD
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = TEXT_HEAD

    def add_footer(slide, slide_num):
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.95), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = CARD_BORDER
        line.line.fill.background()

        f_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(9.5), Inches(0.3))
        tf = f_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "Football Tactical Analytics Database · DBMS Review 1 · Case Study Analysis & Relational SQL"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED

        num_box = slide.shapes.add_textbox(Inches(11.5), Inches(7.05), Inches(1.0), Inches(0.3))
        tf_n = num_box.text_frame
        tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0
        p = tf_n.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        p.text = f"{slide_num:02d}"
        p.font.name = FONT_HEAD
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = EMERALD_PITCH

    # =========================================================================
    # SLIDE 1: Title Slide (Academic, Rigorous, Clean)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1, PAGE_BG)

    # Top accent bar
    top_strip = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(0.8), Inches(1.2), Inches(0.08))
    top_strip.fill.solid()
    top_strip.fill.fore_color.rgb = EMERALD_PITCH
    top_strip.line.fill.background()

    # Academic Category Tag
    tag1 = slide1.shapes.add_textbox(Inches(0.9), Inches(1.1), Inches(11), Inches(0.35))
    tf1 = tag1.text_frame
    tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]
    p.text = "B.TECH COMPUTER SCIENCE & ENGINEERING · DATABASE MANAGEMENT SYSTEMS · REVIEW 1"
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    # Big Title
    tbox = slide1.shapes.add_textbox(Inches(0.9), Inches(1.6), Inches(11.5), Inches(1.3))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Football Tactical Analytics Database"
    p.font.name = FONT_HEAD
    p.font.size = Pt(38)
    p.font.bold = True
    p.font.color.rgb = NAVY_DEEP

    p_sub = tf.add_paragraph()
    p_sub.text = "A Relational Database Case Study on Spatiotemporal Tracking and Tactical Event Analysis"
    p_sub.font.name = FONT_HEAD
    p_sub.font.size = Pt(16)
    p_sub.font.color.rgb = COBALT_BLUE
    p_sub.space_before = Pt(8)

    # Divider line
    div = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(3.2), Inches(11.5), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = CARD_BORDER
    div.line.fill.background()

    # Project Context Panel
    ctx_box = slide1.shapes.add_textbox(Inches(0.9), Inches(3.45), Inches(11.5), Inches(1.2))
    tf_ctx = ctx_box.text_frame
    tf_ctx.word_wrap = True
    tf_ctx.margin_left = tf_ctx.margin_top = 0
    p = tf_ctx.paragraphs[0]
    p.text = "PROJECT SCOPE & BENCHMARK CONTEXT"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    p2 = tf_ctx.add_paragraph()
    p2.text = "This case study designs, normalizes, and implements a 3NF relational database architecture tailored for professional football analysis. Grounded in the FOOTPASS spatiotemporal tracking benchmark (102,992 annotated events and 1.7M+ coordinate frames across 54 UEFA Champions League fixtures), this Review 1 case study structures an operational demonstration database of 1,000 events, 4 matches, 119 players, 8 tactical macro-state clusters, and 4 tactical rule sets in SQLite to support declarative query execution."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_BODY
    p2.space_before = Pt(4)

    # Student Details
    sub_title = slide1.shapes.add_textbox(Inches(0.9), Inches(4.9), Inches(11.5), Inches(0.3))
    p = sub_title.text_frame.paragraphs[0]
    p.text = "SUBMITTED BY"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = TEXT_MUTED

    # Student 1 Card
    card1 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(5.25), Inches(4.5), Inches(1.1))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = CARD_BORDER
    card1.line.width = Pt(1)

    s1_tb = slide1.shapes.add_textbox(Inches(1.15), Inches(5.4), Inches(4.0), Inches(0.8))
    tf_s1 = s1_tb.text_frame
    tf_s1.margin_left = tf_s1.margin_top = 0
    p = tf_s1.paragraphs[0]
    p.text = "Vikas Bhaskar"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DEEP
    p2 = tf_s1.add_paragraph()
    p2.text = "Registration No: 24BCT0149"
    p2.font.name = FONT_CODE
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = EMERALD_PITCH

    # Student 2 Card
    card2 = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(5.7), Inches(5.25), Inches(4.5), Inches(1.1))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = CARD_BORDER
    card2.line.width = Pt(1)

    s2_tb = slide1.shapes.add_textbox(Inches(5.95), Inches(5.4), Inches(4.0), Inches(0.8))
    tf_s2 = s2_tb.text_frame
    tf_s2.margin_left = tf_s2.margin_top = 0
    p = tf_s2.paragraphs[0]
    p.text = "Jeevitesh Kandi"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_DEEP
    p2 = tf_s2.add_paragraph()
    p2.text = "Registration No: 24BCE0350"
    p2.font.name = FONT_CODE
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = EMERALD_PITCH

    # Department Footer
    acad_box = slide1.shapes.add_textbox(Inches(0.9), Inches(6.8), Inches(11.5), Inches(0.3))
    tf_acad = acad_box.text_frame
    tf_acad.margin_left = tf_acad.margin_top = 0
    p = tf_acad.paragraphs[0]
    p.text = "School of Computer Science & Engineering · Department of Computer Science · Academic Year 2026"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Table of Contents / Agenda
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_bg(slide2, PAGE_BG)
    add_header(slide2, "TABLE OF CONTENTS", "Presentation Agenda & Technical Coverage")
    add_footer(slide2, 2)

    agenda_items = [
        ("01", "Domain & Problem Analysis", "Technical bottlenecks in raw match video and unlinked tracking streams"),
        ("02", "System Personas & Business Rules", "Coaching inquiry workflows and core relational integrity constraints"),
        ("03", "Relational Data Model & Keys", "6 normalized entities, candidate keys, and foreign key hierarchy"),
        ("04", "DDL Schema Construction", "Building the relational tables using standard DDL with inline constraints"),
        ("05", "Schema Evolution: ALTER & DROP", "SQLite native column alterations and the 12-step table-rebuild pattern"),
        ("06", "Data Integrity Constraints", "Implementation and validation of PK, FK, UNIQUE, NOT NULL, CHECK, DEFAULT"),
        ("07", "Match Event Lifecycle: DML", "Inserting match fixtures, updating player states, and purging tracking noise"),
        ("08", "Analytical Query Execution", "Single-row scalar, CASE categorization, operators, and statistical grouping"),
    ]

    card_w = Inches(5.7)
    card_h = Inches(1.15)
    for i, (num, title, desc) in enumerate(agenda_items):
        col = i // 4
        row = i % 4
        x = Inches(0.8) + col * Inches(6.0)
        y = Inches(1.6) + row * Inches(1.3)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Number pill on left
        pill = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.02), y + Inches(0.02), Inches(0.7), card_h - Inches(0.04))
        pill.fill.solid()
        pill.fill.fore_color.rgb = EMERALD_PITCH if col == 0 else COBALT_BLUE
        pill.line.fill.background()
        tf_p = pill.text_frame
        tf_p.word_wrap = False
        tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
        p = tf_p.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = num
        p.font.name = FONT_HEAD
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Text inside
        tb = slide2.shapes.add_textbox(x + Inches(0.9), y + Inches(0.18), card_w - Inches(1.0), card_h - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEAD
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 3: Problem & Domain (Authentic Match Action)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_bg(slide3, PAGE_BG)
    add_header(slide3, "01 · DOMAIN & PROBLEM ANALYSIS", "Challenges in Spatiotemporal Football Data")
    add_footer(slide3, 3)

    challenges = [
        ("Unstructured Broadcast Video", "Television broadcast footage captures visual play but lacks queryable structure. Coaches cannot execute SQL to filter game phases, isolate pressing triggers, or compute unit line heights directly from pixels."),
        ("Massive Unlinked Coordinate Logs", "Raw tracking datasets (1.7M+ frames per fixture in FOOTPASS H5) store coordinate streams without relational links to canonical rosters, official jersey numbers, or match context."),
        ("File-Based Analytics Silos", "Match schedules, spatial tracking, and play-by-play event logs reside in disconnected CSV/HDF5 files, preventing multi-match querying, defensive compactness comparisons, and historical joins."),
    ]

    card_y_start = Inches(1.55)
    for idx, (title, desc) in enumerate(challenges):
        cy = card_y_start + idx * Inches(1.6)
        c = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cy, Inches(5.6), Inches(1.4))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = CARD_BORDER

        # Mini accent block
        sq = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), cy + Inches(0.25), Inches(0.3), Inches(0.3))
        sq.fill.solid()
        sq.fill.fore_color.rgb = EMERALD_PITCH
        sq.line.fill.background()

        tb = slide3.shapes.add_textbox(Inches(1.45), cy + Inches(0.2), Inches(4.7), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEAD
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(3)

    # Right side: Authentic Pitch Action Screenshot
    pic_x, pic_y, pic_w = Inches(6.7), Inches(1.55), Inches(5.8)
    img_action = os.path.join(ASSETS_DIR, "football_pitch_action.png")
    if os.path.exists(img_action):
        slide3.shapes.add_picture(img_action, pic_x, pic_y, width=pic_w)

    caption_tb = slide3.shapes.add_textbox(pic_x, pic_y + Inches(3.3), pic_w, Inches(0.6))
    tf_c = caption_tb.text_frame
    tf_c.word_wrap = True
    tf_c.margin_left = tf_c.margin_top = 0
    p = tf_c.paragraphs[0]
    p.text = "Figure 1: Authentic match broadcast tracking footage (game_39: Newcastle vs PSG) showing outfield player distribution, team orientation, and active jersey numbers on the pitch."
    p.font.name = FONT_BODY
    p.font.size = Pt(9)
    p.font.color.rgb = TEXT_MUTED

    # Bottom Callout Box (Benchmark Context Distinction)
    box_b = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.05))
    box_b.fill.solid()
    box_b.fill.fore_color.rgb = NAVY_DEEP
    box_b.line.fill.background()

    tb_b = slide3.shapes.add_textbox(Inches(1.05), Inches(5.75), Inches(11.2), Inches(0.85))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = 0
    p = tf_b.paragraphs[0]
    p.text = "DBMS Case Study Objective & Benchmark Scope"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    p2 = tf_b.add_paragraph()
    p2.text = "To transform high-frequency spatial tracking and play-by-play event streams into a 3NF relational schema. While the full FOOTPASS research benchmark comprises 102,992 annotated events across 54 matches, this case study structures an operational subset of 1,000 events, 4 fixtures, 119 players, and 8 macro-state clusters in SQLite for rapid declarative querying."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 4: How the System Works (FastAPI Swagger UI & Architecture)
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_bg(slide4, PAGE_BG)
    add_header(slide4, "01 · SYSTEM WORKFLOW", "Data Pipeline: From Raw Video to Structured SQL")
    add_footer(slide4, 4)

    steps = [
        ("PHASE 1", "Step 1: Ingest & Synchronize", "Broadcast video (25 fps) and FOOTPASS H5 coordinate logs are ingested. Player bounding boxes and field coordinate vectors [X, Y] are aligned to match timestamps.", EMERALD_PITCH),
        ("PHASE 2", "Step 2: Relational Validation", "Extracted coordinates and events are validated against relational constraints (CHECK, UNIQUE, FK) and normalized into 3NF tables in SQLite.", COBALT_BLUE),
        ("PHASE 3", "Step 3: Declarative SQL Analytics", "Coaches execute structured SQL queries to analyze pressing blocks, filter match events, and render synchronized 2D pitch overlays on the tactical dashboard.", NAVY_DEEP),
    ]

    for s_idx, (phase, stitle, sdesc, scolor) in enumerate(steps):
        sx = Inches(0.8) + s_idx * Inches(4.0)
        sc = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, Inches(1.55), Inches(3.7), Inches(1.75))
        sc.fill.solid()
        sc.fill.fore_color.rgb = CARD_BG
        sc.line.color.rgb = CARD_BORDER

        # Phase pill
        pp = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx + Inches(0.2), Inches(1.7), Inches(1.6), Inches(0.32))
        pp.fill.solid()
        pp.fill.fore_color.rgb = scolor
        pp.line.fill.background()
        p = pp.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = phase
        p.font.name = FONT_HEAD
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        stb = slide4.shapes.add_textbox(sx + Inches(0.2), Inches(2.1), Inches(3.3), Inches(1.1))
        stf = stb.text_frame
        stf.word_wrap = True
        stf.margin_left = stf.margin_top = 0
        p = stf.paragraphs[0]
        p.text = stitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = stf.add_paragraph()
        p2.text = sdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(3)

    # Bottom Left: Swagger UI Screenshot
    api_img = os.path.join(ASSETS_DIR, "fastapi_docs_1792511905970.png")
    if os.path.exists(api_img):
        slide4.shapes.add_picture(api_img, Inches(0.8), Inches(3.5), width=Inches(6.0))

    # Bottom Right: Specifications Card
    spec_c = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(3.5), Inches(5.4), Inches(3.1))
    spec_c.fill.solid()
    spec_c.fill.fore_color.rgb = CARD_BG
    spec_c.line.color.rgb = CARD_BORDER

    spec_tb = slide4.shapes.add_textbox(Inches(7.35), Inches(3.7), Inches(4.9), Inches(2.7))
    tf_sp = spec_tb.text_frame
    tf_sp.word_wrap = True
    tf_sp.margin_left = tf_sp.margin_top = 0
    p = tf_sp.paragraphs[0]
    p.text = "ARCHITECTURE SPECIFICATIONS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = NAVY_DEEP

    specs = [
        ("Presentation Layer", "React + Vite SPA with frame-accurate timeline scrubber and 2D canvas overlay."),
        ("Application Layer", "FastAPI asynchronous service executing spatial queries and partial content video streaming."),
        ("Database Layer", "Relational SQLite/SQL engine enforcing 3NF schema, referential keys, and check constraints."),
        ("Analytical Engine", "TacticalEngine computing line heights, unit compactness, and space creation metrics."),
    ]
    for stitle, sdesc in specs:
        p = tf_sp.add_paragraph()
        p.text = f"• {stitle}: {sdesc}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.space_before = Pt(5)

    # =========================================================================
    # SLIDE 5: Requirements & Domain Business Rules
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_bg(slide5, PAGE_BG)
    add_header(slide5, "02 · SYSTEM STAKEHOLDERS & RULES", "User Personas, Functional Needs & Data Integrity Rules")
    add_footer(slide5, 5)

    # Left: Personas
    p_title = slide5.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(5.6), Inches(0.3))
    p = p_title.text_frame.paragraphs[0]
    p.text = "SYSTEM STAKEHOLDERS & NEEDS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    personas = [
        ("Head Coach", "Requires high-level tactical summaries: opponent defensive block height, team width/compactness, and flank overload patterns."),
        ("Tactical Analyst", "Executes complex declarative SQL queries to evaluate set-piece success, player pass completion, and pressing triggers."),
        ("Analytics Engineer", "Manages automated ingestion of broadcast tracking feeds, verifies schema constraints, and optimizes table indexes."),
    ]
    for idx, (pname, pdesc) in enumerate(personas):
        py = Inches(1.85) + idx * Inches(1.1)
        pc = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), py, Inches(5.6), Inches(0.95))
        pc.fill.solid()
        pc.fill.fore_color.rgb = CARD_BG
        pc.line.color.rgb = CARD_BORDER

        tb = slide5.shapes.add_textbox(Inches(1.05), py + Inches(0.12), Inches(5.1), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = pname
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = pdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(2)

    # Functional Requirements List (Bottom Left)
    fr_box = slide5.shapes.add_textbox(Inches(0.8), Inches(5.25), Inches(5.6), Inches(1.5))
    tf_fr = fr_box.text_frame
    tf_fr.word_wrap = True
    tf_fr.margin_left = tf_fr.margin_top = 0
    p = tf_fr.paragraphs[0]
    p.text = "CORE FUNCTIONAL REQUIREMENTS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    reqs = [
        "Maintain canonical club rosters and official competition match fixtures.",
        "Guarantee chronological sequence consistency across match halves.",
        "Provide sub-second query performance on 100K+ play-by-play events.",
        "Automatically classify tactical macro-states (High Press, Mid Block, Low Block).",
    ]
    for r in reqs:
        p = tf_fr.add_paragraph()
        p.text = f"• {r}"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_BODY
        p.space_before = Pt(3)

    # Right: Relational Business Rules
    r_title = slide5.shapes.add_textbox(Inches(6.8), Inches(1.5), Inches(5.7), Inches(0.3))
    p = r_title.text_frame.paragraphs[0]
    p.text = "RELATIONAL DATA INTEGRITY RULES"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    rules = [
        ("Valid Squad Numbers", "CHECK (shirt_number BETWEEN 1 AND 99)"),
        ("Distinct Fixture Clubs", "CHECK (home_team <> away_team)"),
        ("Single Jersey per Club", "UNIQUE (team_code, shirt_number)"),
        ("Valid Match Period", "CHECK (half IN (1, 2))"),
        ("Normalized Coordinates", "CHECK (centroid_x BETWEEN 0.0 AND 1.0)"),
    ]
    for idx, (rtitle, rsql) in enumerate(rules):
        ry = Inches(1.85) + idx * Inches(0.68)
        rc = slide5.shapes.add_textbox(Inches(6.8), ry, Inches(5.7), Inches(0.55))
        tf = rc.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = rtitle + "  "
        p.font.name = FONT_HEAD
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        run = p.add_run()
        run.text = rsql
        run.font.name = FONT_CODE
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = COBALT_BLUE

    # Right Bottom: Tactical Block Rules
    tb_title = slide5.shapes.add_textbox(Inches(6.8), Inches(5.35), Inches(5.7), Inches(0.3))
    p = tb_title.text_frame.paragraphs[0]
    p.text = "TACTICAL BLOCK CLASSIFICATION"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    blocks = [
        ("High Press Block", "Centroid X >= 0.55\nUnit Length < 35m"),
        ("Midfield Structure", "Centroid X BETWEEN\n0.35 AND 0.55"),
        ("Deep Low Block", "Centroid X < 0.35\nBackline < 20m"),
    ]
    for b_idx, (bname, bcrit) in enumerate(blocks):
        bx = Inches(6.8) + b_idx * Inches(2.0)
        by = Inches(5.7)
        b_card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(1.8), Inches(1.05))
        b_card.fill.solid()
        b_card.fill.fore_color.rgb = CARD_BG
        b_card.line.color.rgb = CARD_BORDER

        tb = slide5.shapes.add_textbox(bx + Inches(0.1), by + Inches(0.12), Inches(1.6), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = bname
        p.font.name = FONT_HEAD
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = bcrit
        p2.font.name = FONT_CODE
        p2.font.size = Pt(8)
        p2.font.color.rgb = EMERALD_PITCH
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 6: Normalized Entities, Attributes & Keys
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_bg(slide6, PAGE_BG)
    add_header(slide6, "03 · RELATIONAL DATA MODEL", "Normalized Entities, Attributes & Key Hierarchy")
    add_footer(slide6, 6)

    entities = [
        ("TEAMS", "European clubs with code, official name, country, venue, and primary kit colors."),
        ("MATCHES", "Scheduled fixtures across European competitions with date, frame count, and duration."),
        ("PLAYERS", "Squad rosters with canonical tracking ID, team code, jersey number, position, and role ID."),
        ("MATCH_EVENTS", "Play-by-play actions: Pass, Drive, Cross, Shot, Header, Throw-in, Tackle, Block."),
        ("TACTICAL_SNAPSHOTS", "Spatiotemporal macro-states (K=8 cluster states, team width, length, and centroid line)."),
        ("TACTICAL_RULES", "Coaching heuristics and threshold criteria for flagging tactical structures dynamically."),
    ]

    card_w = Inches(3.7)
    card_h = Inches(1.6)
    for i, (ename, edesc) in enumerate(entities):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.6) + row * Inches(1.8)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Header bar inside card
        hbar = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), y + Inches(0.2), Inches(1.8), Inches(0.32))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = NAVY_DEEP
        hbar.line.fill.background()
        p = hbar.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = ename
        p.font.name = FONT_CODE
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.65), card_w - Inches(0.4), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = edesc
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_BODY

    # Bottom Key Definitions Card
    keys = [
        ("PK", "Primary Key", "Unique identifier for each record — team_code, match_id, player_id, event_id", EMERALD_PITCH),
        ("FK", "Foreign Key", "Referential link preserving integrity — matches.home_team -> teams(team_code)", COBALT_BLUE),
        ("UQ", "Candidate Key", "Enforces non-duplicate attributes — UNIQUE(team_code, shirt_number)", EMERALD_PITCH),
        ("CK", "Composite Key", "Multi-column temporal uniqueness — (match_id, half, frame_idx, jersey)", COBALT_BLUE),
    ]

    kw = Inches(2.75)
    kh = Inches(1.2)
    for k_idx, (kcode, ktitle, kdesc, kcolor) in enumerate(keys):
        x = Inches(0.8) + k_idx * Inches(2.98)
        y = Inches(5.4)
        kcard = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, kw, kh)
        kcard.fill.solid()
        kcard.fill.fore_color.rgb = CARD_BG
        kcard.line.color.rgb = CARD_BORDER

        # Pill badge
        pbox = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), y + Inches(0.18), Inches(0.55), Inches(0.35))
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = kcolor
        pbox.line.fill.background()
        p = pbox.text_frame.paragraphs[0]
        p.text = kcode
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.85), y + Inches(0.18), kw - Inches(0.95), kh - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = ktitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = kdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(3)

    # =========================================================================
    # SLIDE 7: ER Architecture (6 Entities Including TACTICAL_RULES)
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_bg(slide7, PAGE_BG)
    add_header(slide7, "03 · ER ARCHITECTURE", "Comprehensive 6-Entity Relational ER Diagram")
    add_footer(slide7, 7)

    er_path = os.path.join(ASSETS_DIR, "er_diagram_v3.png")
    if os.path.exists(er_path):
        slide7.shapes.add_picture(er_path, Inches(0.8), Inches(1.5), width=Inches(11.733))

    # =========================================================================
    # SLIDE 8: DDL Schema Construction
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_bg(slide8, PAGE_BG)
    add_header(slide8, "04 · DDL IMPLEMENTATION", "DDL Schema Construction & Table Definitions")
    add_footer(slide8, 8)

    # Box 1: teams & matches
    box1_x, box1_y, box1_w, box1_h = Inches(0.8), Inches(1.55), Inches(5.7), Inches(4.3)
    c1 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box1_x, box1_y, box1_w, box1_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CODE_BG
    c1.line.color.rgb = CODE_BORDER

    tb1 = slide8.shapes.add_textbox(box1_x + Inches(0.25), box1_y + Inches(0.2), box1_w - Inches(0.5), box1_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]
    p.text = "-- 1. Core Club & Fixture DDL Specification"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    ddl_1 = """CREATE TABLE teams (
    team_code     VARCHAR(10) PRIMARY KEY,
    team_name     VARCHAR(60) NOT NULL UNIQUE,
    country       VARCHAR(30) NOT NULL,
    home_venue    VARCHAR(80),
    primary_color VARCHAR(10) DEFAULT '#FFFFFF'
);

CREATE TABLE matches (
    match_id      VARCHAR(20) PRIMARY KEY,
    competition   VARCHAR(50) NOT NULL,
    season        VARCHAR(10) DEFAULT '2023-2024',
    match_date    DATE,
    home_team     VARCHAR(10) REFERENCES teams(team_code),
    away_team     VARCHAR(10) REFERENCES teams(team_code),
    total_frames  INTEGER CHECK (total_frames > 0),
    duration_s    NUMERIC(7,2) CHECK (duration_s > 0),
    fps           NUMERIC(4,1) DEFAULT 25.0,
    CONSTRAINT chk_diff_teams CHECK (home_team <> away_team)
);"""
    p2 = tf1.add_paragraph()
    p2.text = ddl_1
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(4)

    # Box 2: players & match_events
    box2_x, box2_y, box2_w, box2_h = Inches(6.8), Inches(1.55), Inches(5.7), Inches(4.3)
    c2 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box2_x, box2_y, box2_w, box2_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = CODE_BG
    c2.line.color.rgb = CODE_BORDER

    tb2 = slide8.shapes.add_textbox(box2_x + Inches(0.25), box2_y + Inches(0.2), box2_w - Inches(0.5), box2_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = 0
    p = tf2.paragraphs[0]
    p.text = "-- 2. Squad Rosters & Match Events DDL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    ddl_2 = """CREATE TABLE players (
    player_id     INTEGER PRIMARY KEY,
    team_code     VARCHAR(10) REFERENCES teams(team_code),
    shirt_number  INTEGER CHECK (shirt_number BETWEEN 1 AND 99),
    player_name   VARCHAR(60) NOT NULL,
    position      VARCHAR(10) NOT NULL,
    role_id       INTEGER CHECK (role_id BETWEEN 1 AND 13),
    CONSTRAINT uq_team_shirt UNIQUE (team_code, shirt_number)
);

CREATE TABLE match_events (
    event_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id      VARCHAR(20) REFERENCES matches(match_id),
    half          INTEGER CHECK (half IN (1, 2)),
    frame_idx     INTEGER CHECK (frame_idx >= 0),
    event_second  NUMERIC(6,2),
    team_code     VARCHAR(10) REFERENCES teams(team_code),
    jersey_number INTEGER NOT NULL,
    action_type   VARCHAR(30) NOT NULL
    CHECK (action_type IN ('Pass','Drive','Cross','Shot','Header','Throw-in','Tackle','Block')),
    success_flag  INTEGER DEFAULT 1 CHECK (success_flag IN (0, 1))
);"""
    p2 = tf2.add_paragraph()
    p2.text = ddl_2
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(4)

    # Bottom 3 Architecture Pills
    pills = [
        "Primary Keys enforce entity identity across all 6 tables",
        "Foreign Keys enforce club and fixture referential hierarchy",
        "CHECK constraints validate pitch bounds, halves & jersey IDs",
    ]
    for p_idx, p_text in enumerate(pills):
        px = Inches(0.8) + p_idx * Inches(4.0)
        py = Inches(6.1)
        p_card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, Inches(3.7), Inches(0.65))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = CARD_BG
        p_card.line.color.rgb = CARD_BORDER

        tb = slide8.shapes.add_textbox(px, py + Inches(0.12), Inches(3.7), Inches(0.45))
        p = tb.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = p_text
        p.font.name = FONT_HEAD
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 9: Schema Evolution (ALTER & DROP - Strict SQLite Compatibility)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_bg(slide9, PAGE_BG)
    add_header(slide9, "04 · SCHEMA EVOLUTION", "ALTER & DROP: Managing Migrations & Table Lifecycles")
    add_footer(slide9, 9)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(6.8), Inches(4.55)
    c = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = CODE_BORDER

    tb = slide9.shapes.add_textbox(c_x + Inches(0.2), c_y + Inches(0.15), c_w - Inches(0.4), c_h - Inches(0.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Production Schema Evolution (SQLite 3.35+ Compatible)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    alter_sql = """-- 1. ADD COLUMN: Add market valuation attribute
ALTER TABLE players ADD COLUMN market_value_eur NUMERIC(12,2);

-- 2. RENAME COLUMN: Adjust attribute naming (SQLite 3.25+)
ALTER TABLE players RENAME COLUMN player_name TO full_name;

-- 3. DROP COLUMN: Deprecate legacy sensor attribute (SQLite 3.35+)
ALTER TABLE players DROP COLUMN market_value_eur;

-- 4. Adding Constraints: SQLite Table-Rebuild Migration Pattern
-- (SQLite restricts direct 'ADD CONSTRAINT'; standard 12-step rebuild):
CREATE TABLE match_events_migrated (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id VARCHAR(20) REFERENCES matches(match_id),
    half INTEGER CHECK (half IN (1, 2)),
    frame_idx INTEGER CHECK (frame_idx >= 0),
    event_second NUMERIC(6,2) CHECK (event_second >= 0.0),
    team_code VARCHAR(10) REFERENCES teams(team_code),
    jersey_number INTEGER NOT NULL,
    action_type VARCHAR(30) NOT NULL,
    success_flag INTEGER DEFAULT 1
);
INSERT INTO match_events_migrated SELECT * FROM match_events;
DROP TABLE match_events;
ALTER TABLE match_events_migrated RENAME TO match_events;

-- 5. Managed DROP TABLE Order (Drop child relations before parents)
DROP TABLE match_events;
DROP TABLE tactical_snapshots;
DROP TABLE matches;"""

    p2 = tf.add_paragraph()
    p2.text = alter_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(7.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(3)

    # Right Action Chips
    chips = [
        ("ADD COLUMN", "Incorporates new telemetry attributes or tracking sensor parameters."),
        ("RENAME COLUMN", "Alters attribute names without data loss (supported in SQLite 3.25+)."),
        ("DROP COLUMN", "Purges deprecated legacy tracking fields (supported in SQLite 3.35+)."),
        ("TABLE REBUILD", "Official SQLite pattern to inject CHECK, UNIQUE, or FK constraints."),
        ("DROP TABLE", "Permanently deletes relations following dependency order (children first)."),
    ]
    for ch_idx, (cname, cdesc) in enumerate(chips):
        cy = Inches(1.55) + ch_idx * Inches(0.9)
        btn = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), cy, Inches(1.65), Inches(0.45))
        btn.fill.solid()
        btn.fill.fore_color.rgb = NAVY_DEEP
        btn.line.color.rgb = COBALT_BLUE
        btn.line.width = Pt(1)
        p = btn.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = cname
        p.font.name = FONT_CODE
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        dtb = slide9.shapes.add_textbox(Inches(9.85), cy + Inches(0.02), Inches(2.65), Inches(0.75))
        tf_d = dtb.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]
        p.text = cdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_BODY

    # Bottom Callout Box
    tip = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    tip.fill.solid()
    tip.fill.fore_color.rgb = CARD_BG
    tip.line.color.rgb = EMERALD_PITCH
    tip.line.width = Pt(1.2)

    ttb = slide9.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.5))
    tf_tip = ttb.text_frame
    tf_tip.word_wrap = True
    tf_tip.margin_left = tf_tip.margin_top = 0
    p = tf_tip.paragraphs[0]
    p.text = "SQLite Engine Architecture: Direct 'ALTER TABLE ADD CONSTRAINT' is restricted in SQLite. Table-rebuild migrations ensure atomic schema evolution while respecting foreign key dependencies and data integrity."
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.0)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 10: Relational Integrity Constraints
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_bg(slide10, PAGE_BG)
    add_header(slide10, "05 · INTEGRITY CONSTRAINTS", "Relational Constraints for Tactical Data Validation")
    add_footer(slide10, 10)

    constraints = [
        ("PK", "PRIMARY KEY", "Enforces entity identity with unique, non-null values. Used in team_code, match_id, player_id, event_id, snapshot_id, rule_id."),
        ("FK", "FOREIGN KEY", "Preserves referential integrity across fixtures and squads. matches.home_team -> teams with ON DELETE CASCADE."),
        ("UQ", "UNIQUE KEY", "Guarantees no duplicate assignments. team_name, and composite candidate key UNIQUE(team_code, shirt_number)."),
        ("NN", "NOT NULL", "Mandates essential business values. player_name, action_type, competition must never contain missing values."),
        ("CHK", "CHECK", "Validates tactical domain bounds. shirt_number 1–99, role_id 1–13, half IN (1, 2), and home_team <> away_team."),
        ("DEF", "DEFAULT", "Supplies automated defaults. season = '2023-2024', fps = 25.0, success_flag = 1, severity_level = 'MEDIUM'."),
    ]

    cw = Inches(3.7)
    ch = Inches(2.35)
    for i, (code, title, desc) in enumerate(constraints):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.6) + row * Inches(2.6)

        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Badge pill
        bpill = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.25), y + Inches(0.22), Inches(0.75), Inches(0.45))
        bpill.fill.solid()
        bpill.fill.fore_color.rgb = EMERALD_PITCH if row == 0 else COBALT_BLUE
        bpill.line.fill.background()
        tf_bp = bpill.text_frame
        tf_bp.word_wrap = False
        tf_bp.margin_left = tf_bp.margin_top = tf_bp.margin_right = tf_bp.margin_bottom = 0
        p = tf_bp.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = code
        p.font.name = FONT_CODE
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Title
        tb = slide10.shapes.add_textbox(x + Inches(1.15), y + Inches(0.22), cw - Inches(1.3), Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEAD
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        # Desc
        dtb = slide10.shapes.add_textbox(x + Inches(0.25), y + Inches(0.95), cw - Inches(0.5), Inches(1.2))
        tf_d = dtb.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 11: DML Operations (Data Lifecycle - Validated SQLite Execution)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_bg(slide11, PAGE_BG)
    add_header(slide11, "06 · DML OPERATIONS", "Match Event Lifecycle: INSERT, UPDATE & DELETE")
    add_footer(slide11, 11)

    dml_sections = [
        ("INSERT", "Record Ingestion", """-- Ingest new club into registry
INSERT INTO teams
(team_code, team_name, country,
 home_venue, primary_color)
VALUES ('ARS', 'Arsenal FC',
 'ENG', 'Emirates Stadium', '#EF0107');

-- Schedule tournament fixture
INSERT INTO matches
(match_id, competition, season,
 match_date, home_team, away_team,
 total_frames, duration_s, fps)
VALUES ('game_99',
 'UEFA Champions League', '2023-2024',
 '2023-11-08', 'ARS', 'BAY',
 154000, 6160.00, 25.0);

-- Record real-time event telemetry
INSERT INTO match_events
(match_id, half, frame_idx,
 event_second, team_code,
 jersey_number, action_type, success_flag)
VALUES ('game_99', 1, 350,
 14.00, 'ARS', 7, 'Pass', 1);"""),

        ("UPDATE", "Tactical Modification", """-- 1. Fixture extra time duration update
UPDATE matches
SET duration_s = 6280.50,
    total_frames = 157012
WHERE match_id = 'game_39';

-- 2. Coach adjusts player tactical role
UPDATE players
SET role_id = 10,
    position = 'LW'
WHERE player_id = 5;

-- 3. Verified tackle success attribution
UPDATE match_events
SET success_flag = 1
WHERE event_id = 101;"""),

        ("DELETE", "Data Sanitization", """-- 1. Purge corrupted sensor noise
DELETE FROM match_events
WHERE frame_idx < 0
   OR event_second > 7200.0;

-- 2. Remove cancelled friendly fixture
DELETE FROM matches
WHERE competition = 'Exhibition Friendly'
  AND season = '2023-2024';

-- 3. Clean obsolete coaching rules
DELETE FROM tactical_rules
WHERE rule_id = 'RULE_DEPRECATED';""")
    ]

    card_w = Inches(3.7)
    card_h = Inches(4.7)
    for d_idx, (dtag, dsub, dsql) in enumerate(dml_sections):
        dx = Inches(0.8) + d_idx * Inches(4.0)

        # Header Pill
        pill = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, Inches(1.55), Inches(1.3), Inches(0.35))
        pill.fill.solid()
        if dtag == "INSERT":
            pill.fill.fore_color.rgb = EMERALD_PITCH
        elif dtag == "UPDATE":
            pill.fill.fore_color.rgb = COBALT_BLUE
        else:
            pill.fill.fore_color.rgb = NAVY_DEEP
        pill.line.fill.background()
        p = pill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = dtag
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Subtitle
        tb = slide11.shapes.add_textbox(dx + Inches(1.45), Inches(1.58), Inches(2.2), Inches(0.3))
        p = tb.text_frame.paragraphs[0]
        p.text = dsub
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

        # Code Panel
        c = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, dx, Inches(2.0), card_w, card_h)
        c.fill.solid()
        c.fill.fore_color.rgb = CODE_BG
        c.line.color.rgb = CODE_BORDER

        ctb = slide11.shapes.add_textbox(dx + Inches(0.18), Inches(2.15), card_w - Inches(0.36), card_h - Inches(0.3))
        ctf = ctb.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_top = 0
        p = ctf.paragraphs[0]
        p.text = f"-- {dtag.lower()}_operations.sql"
        p.font.name = FONT_CODE
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = EMERALD_BRIGHT

        p2 = ctf.add_paragraph()
        p2.text = dsql
        p2.font.name = FONT_CODE
        p2.font.size = Pt(8.0)
        p2.font.color.rgb = TEXT_CODE
        p2.space_before = Pt(4)

    # =========================================================================
    # SLIDE 12: Single-Row Functions (Scalar Transformation)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_bg(slide12, PAGE_BG)
    add_header(slide12, "07 · DATA TRANSFORMATION", "Single-Row Functions for Tactical Formatting")
    add_footer(slide12, 12)

    # Left Code Box
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(5.3), Inches(4.5)
    c = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = CODE_BORDER

    tb = slide12.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.25), c_w - Inches(0.5), c_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Single-Row Scalar Transformation Query"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    query_12 = """SELECT player_id,
       UPPER(player_name) AS name_caps,
       LOWER(team_code)   AS team_lower,
       SUBSTR(position, 1, 2) AS pos_code,
       'ROLE-' || substr('00' || role_id, -2) AS tier
FROM players
WHERE team_code = 'NEW'
ORDER BY shirt_number;"""

    p2 = tf.add_paragraph()
    p2.text = query_12
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right: Output Table
    out_lbl = slide12.shapes.add_textbox(Inches(6.4), Inches(1.6), Inches(6.0), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (5 sample records)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    # Table with 6 rows (1 header + 5 rows) and 5 cols
    tbl_shape = slide12.shapes.add_table(6, 5, Inches(6.4), Inches(2.0), Inches(5.9), Inches(3.2))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(2.1)
    tbl.columns[2].width = Inches(0.8)
    tbl.columns[3].width = Inches(0.8)
    tbl.columns[4].width = Inches(1.6)

    headers_12 = ["ID", "Name (UPPER)", "Team", "Pos", "Tactical Tier"]
    for c_i, h_t in enumerate(headers_12):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DEEP
        p = cell.text_frame.paragraphs[0]
        p.text = h_t
        p.font.name = FONT_HEAD
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    rows_12 = [
        ("1", "KIERAN TRIPPIER", "new", "RB", "ROLE-13"),
        ("2", "FABIAN SCHÄR", "new", "CB", "ROLE-03"),
        ("3", "JAMAAL LASCELLES", "new", "CB", "ROLE-05"),
        ("4", "SANDRO TONALI", "new", "CM", "ROLE-06"),
        ("5", "ANTHONY GORDON", "new", "LW", "ROLE-10"),
    ]
    for r_i, r_data in enumerate(rows_12):
        for c_i, val in enumerate(r_data):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_i % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = NAVY_DEEP

    # Bottom Explanation
    callout = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG
    callout.line.color.rgb = EMERALD_PITCH
    callout.line.width = Pt(1.2)

    tb = slide12.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Mathematical & Scalar Principle: Single-row functions operate deterministically on individual record attributes to return exactly one scalar value per row — formatting player rosters, generating normalized lookup codes, and padding hierarchical role keys."
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 13: Numeric Functions & CASE (Conditional Computation)
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_bg(slide13, PAGE_BG)
    add_header(slide13, "07 · CONDITIONAL COMPUTATION", "Numeric Computations & Dynamic CASE Classifications")
    add_footer(slide13, 13)

    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(5.3), Inches(4.5)
    c = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = CODE_BORDER

    tb = slide13.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.25), c_w - Inches(0.5), c_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Numeric Rounding & CASE Categorization"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    query_13 = """SELECT action_type,
       event_second,
       ROUND(event_second / 60.0, 2) AS match_min,
       CASE
         WHEN action_type IN ('Shot', 'Cross')
         THEN 'High Threat Attack'
         WHEN action_type IN ('Tackle', 'Block')
         THEN 'Defensive Regain'
         WHEN action_type = 'Pass'
         THEN 'Ball Circulation'
         ELSE 'Open Progression'
       END AS tactical_phase
FROM match_events
WHERE match_id = 'game_39';"""

    p2 = tf.add_paragraph()
    p2.text = query_13
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right: Output Table
    out_lbl = slide13.shapes.add_textbox(Inches(6.4), Inches(1.6), Inches(6.0), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (Match game_39 events)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    tbl_shape = slide13.shapes.add_table(8, 4, Inches(6.4), Inches(2.0), Inches(5.9), Inches(3.8))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.1)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.3)
    tbl.columns[3].width = Inches(2.4)

    headers_13 = ["Action", "Time (s)", "Match Min", "Tactical Phase"]
    for c_i, h_t in enumerate(headers_13):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DEEP
        p = cell.text_frame.paragraphs[0]
        p.text = h_t
        p.font.name = FONT_HEAD
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    rows_13 = [
        ("Pass", "10.08", "0.17", "Ball Circulation"),
        ("Pass", "10.84", "0.18", "Ball Circulation"),
        ("Pass", "15.12", "0.25", "Ball Circulation"),
        ("Shot", "21.64", "0.36", "High Threat Attack"),
        ("Pass", "24.64", "0.41", "Ball Circulation"),
        ("Pass", "26.20", "0.44", "Ball Circulation"),
        ("Pass", "27.04", "0.45", "Ball Circulation"),
    ]
    for r_i, r_data in enumerate(rows_13):
        for c_i, val in enumerate(r_data):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_i % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = NAVY_DEEP

    # Bottom
    callout = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG
    callout.line.color.rgb = EMERALD_PITCH
    callout.line.width = Pt(1.2)

    tb = slide13.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Mathematical Analysis: The CASE expression enables dynamic branch classification of match play on the fly, while ROUND() converts raw spatiotemporal elapsed seconds into standardized match minutes."
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 14: SQL Operators (BETWEEN, IN, LIKE)
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_bg(slide14, PAGE_BG)
    add_header(slide14, "08 · QUERY OPERATORS", "Pattern Matching & Range Filtering: BETWEEN, IN & LIKE")
    add_footer(slide14, 14)

    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(5.3), Inches(4.5)
    c = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = CODE_BORDER

    tb = slide14.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.25), c_w - Inches(0.5), c_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Relational Operator Filtering Query"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    query_14 = """SELECT player_name,
       shirt_number,
       team_code,
       position
FROM players
WHERE shirt_number BETWEEN 7 AND 25
  AND team_code IN ('NEW', 'PAR', 'BAY')
  AND player_name LIKE '%a%'
ORDER BY shirt_number;"""

    p2 = tf.add_paragraph()
    p2.text = query_14
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right: Output Table
    out_lbl = slide14.shapes.add_textbox(Inches(6.4), Inches(1.6), Inches(6.0), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (Filtered squad records)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    tbl_shape = slide14.shapes.add_table(5, 4, Inches(6.4), Inches(2.0), Inches(5.9), Inches(2.6))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.1)
    tbl.columns[3].width = Inches(1.3)

    headers_14 = ["Player Name", "Shirt #", "Club", "Position"]
    for c_i, h_t in enumerate(headers_14):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DEEP
        p = cell.text_frame.paragraphs[0]
        p.text = h_t
        p.font.name = FONT_HEAD
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    rows_14 = [
        ("Serge Gnabry", "7", "BAY", "FW"),
        ("Leon Goretzka", "8", "BAY", "CM"),
        ("Sandro Tonali", "8", "NEW", "CM"),
        ("Harry Kane", "9", "BAY", "CF"),
    ]
    for r_i, r_data in enumerate(rows_14):
        for c_i, val in enumerate(r_data):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_i % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8.5)
            p.font.color.rgb = NAVY_DEEP

    # Bottom
    callout = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    callout.fill.solid()
    callout.fill.fore_color.rgb = CARD_BG
    callout.line.color.rgb = COBALT_BLUE
    callout.line.width = Pt(1.2)

    tb = slide14.shapes.add_textbox(Inches(1.0), Inches(6.32), Inches(11.3), Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Relational Set Filtering: BETWEEN tests continuous inclusive range boundaries [7..25], IN verifies membership against discrete relation sets ('NEW', 'PAR', 'BAY'), and LIKE '%a%' evaluates wildcard string patterns. Conjunctions (AND) guarantee strict intersection."
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 15: Statistical Aggregations (GROUP BY & HAVING + Chart)
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_bg(slide15, PAGE_BG)
    add_header(slide15, "08 · AGGREGATE ANALYTICS", "Statistical Aggregations & Grouping with HAVING")
    add_footer(slide15, 15)

    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(4.7), Inches(4.5)
    c = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = CODE_BORDER

    tb = slide15.shapes.add_textbox(c_x + Inches(0.2), c_y + Inches(0.25), c_w - Inches(0.4), c_h - Inches(0.5))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Aggregates with HAVING Condition"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    query_15 = """SELECT team_code,
       COUNT(*) AS total_actions,
       ROUND(AVG(event_second), 2) AS avg_sec,
       MIN(event_second) AS min_sec,
       MAX(event_second) AS max_sec,
       SUM(CASE WHEN action_type = 'Pass'
           THEN 1 ELSE 0 END) AS passes
FROM match_events
GROUP BY team_code
HAVING COUNT(*) >= 50
ORDER BY passes DESC;"""

    p2 = tf.add_paragraph()
    p2.text = query_15
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Top Right: Executed Output Table
    out_lbl = slide15.shapes.add_textbox(Inches(5.7), Inches(1.55), Inches(6.5), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "AGGREGATE QUERY OUTPUT  (Across 1,000 match events)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    tbl_shape = slide15.shapes.add_table(7, 6, Inches(5.7), Inches(1.9), Inches(6.8), Inches(2.2))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(0.8)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.3)
    tbl.columns[3].width = Inches(1.1)
    tbl.columns[4].width = Inches(1.1)
    tbl.columns[5].width = Inches(1.4)

    headers_15 = ["Club", "Actions", "Avg (s)", "Min (s)", "Max (s)", "Passes"]
    for c_i, h_t in enumerate(headers_15):
        cell = tbl.cell(0, c_i)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY_DEEP
        p = cell.text_frame.paragraphs[0]
        p.text = h_t
        p.font.name = FONT_HEAD
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

    rows_15 = [
        ("RSO", "203", "225.66", "1.72", "510.64", "102"),
        ("NEW", "172", "367.30", "10.08", "741.68", "91"),
        ("BVB", "166", "262.63", "6.72", "522.24", "83"),
        ("BAY", "150", "370.96", "6.08", "791.08", "73"),
        ("MUN", "100", "460.59", "11.68", "749.76", "46"),
        ("PAR", "78", "425.48", "15.12", "683.60", "45"),
    ]
    for r_i, r_data in enumerate(rows_15):
        for c_i, val in enumerate(r_data):
            cell = tbl.cell(r_i + 1, c_i)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_i % 2 == 1 else RGBColor(255, 255, 255)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.name = FONT_BODY
            p.font.size = Pt(8)
            p.font.color.rgb = NAVY_DEEP

    # Bottom Right: Emerald Passes Chart
    chart_img = os.path.join(ASSETS_DIR, "slide15_passes_chart_v2.png")
    if os.path.exists(chart_img):
        slide15.shapes.add_picture(chart_img, Inches(5.7), Inches(4.25), width=Inches(6.8))

    # =========================================================================
    # SLIDE 16: Review 1 Milestones & Phase 2 Technical Scope
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_bg(slide16, PAGE_BG)
    add_header(slide16, "PROJECT MILESTONES", "Review 1 Accomplishments & Phase 2 Technical Scope")
    add_footer(slide16, 16)

    # Left: Review 1 Done Checklist
    r1_items = [
        ("Normalized Relational Schema", "Designed and validated 6 core 3NF tables eliminating redundancy across clubs, fixtures, rosters, and tracking events."),
        ("Stakeholders & Domain Integrity", "Defined personas (Coach, Analyst, Engineer) and enforced multi-layer constraints (CHECK, UNIQUE, FK, DEFAULT)."),
        ("Complete 6-Entity ER Architecture", "Developed comprehensive ER diagram connecting all 6 tables with explicit 1:N referential cardinalities."),
        ("Validated DDL Schema Construction", "Implemented syntactically correct SQLite DDL with domain bounds, default parameters, and cascade specifications."),
        ("Audited DML Data Operations", "Established verified data ingestion, player position updating, and sensor noise deletion pipelines."),
        ("Analytical Query Execution", "Executed scalar transformations, dynamic CASE classifications, and statistical group aggregations on live data."),
    ]

    card_y = Inches(1.55)
    for idx, (rtitle, rdesc) in enumerate(r1_items):
        cy = card_y + idx * Inches(0.85)

        # Checkmark Icon Badge
        chk = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), cy + Inches(0.05), Inches(0.38), Inches(0.38))
        chk.fill.solid()
        chk.fill.fore_color.rgb = EMERALD_PITCH
        chk.line.fill.background()
        p = chk.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "✓"
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide16.shapes.add_textbox(Inches(1.3), cy, Inches(5.2), Inches(0.75))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = rtitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(1)

    # Right: Phase 2 Scope Card
    r_card = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.55), Inches(5.3), Inches(5.1))
    r_card.fill.solid()
    r_card.fill.fore_color.rgb = NAVY_DEEP
    r_card.line.fill.background()

    rtb = slide16.shapes.add_textbox(Inches(7.55), Inches(1.85), Inches(4.6), Inches(4.5))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_top = 0
    p = rtf.paragraphs[0]
    p.text = "PHASE 2 TECHNICAL ROADMAP"
    p.font.name = FONT_HEAD
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    p_sub = rtf.add_paragraph()
    p_sub.text = "Advanced DBMS Features & Query Optimization"
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(9.5)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_sub.space_before = Pt(3)

    r2_points = [
        ("Multi-Table Relational JOINS", "Inner, Left, and Full Outer Joins linking matches, players, events, and spatial metrics."),
        ("Complex Correlated Subqueries", "Subqueries in SELECT, WHERE, and HAVING to compute comparative player percentiles."),
        ("Indexed Materialized Views", "Pre-computed tactical summary views for real-time coach interval dashboards."),
        ("PL/SQL Procedures & Functions", "Modular server-side algorithms computing pressing intensity (PPDA) directly in the DBMS."),
        ("Event Triggers & Cursors", "Automated database triggers alerting analysts when line compression breaches critical thresholds."),
    ]
    for ptitle, pdesc in r2_points:
        p = rtf.add_paragraph()
        p.text = f"• {ptitle}: "
        p.font.name = FONT_HEAD
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        p.space_before = Pt(10)

        run = p.add_run()
        run.text = pdesc
        run.font.name = FONT_BODY
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(203, 213, 225)

    # Status callout at bottom of right card
    p_fin = rtf.add_paragraph()
    p_fin.text = "Phase 1 Review Completed · Ready for Defense & Evaluation"
    p_fin.font.name = FONT_HEAD
    p_fin.font.size = Pt(10)
    p_fin.font.bold = True
    p_fin.font.color.rgb = EMERALD_BRIGHT
    p_fin.space_before = Pt(20)

    # Save presentation
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prs.save(PPTX_PATH)
    print(f"Final presentation saved to: {PPTX_PATH}")

if __name__ == '__main__':
    build_presentation()
