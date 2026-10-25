"""
generate_redesigned_presentation.py
===================================
Generates the fully redesigned, professional 16-slide PowerPoint presentation:
'Football_Tactical_Analytics_DBMS_Review_1.pptx'

Design Philosophy:
- COMPLETELY NEW THEME: Deep Navy (#0F172A), Pitch Emerald (#059669), Cobalt Blue (#2563EB), Crisp Pure White (#FFFFFF).
- NO similarity to FLAVRD colors (no gold, no bronze, no yellow-beige warning boxes).
- Minimalist, modern cover page with clear academic structure.
- Authentic football pitch pictures showing actual players on the pitch with tracking bounding boxes (test_frame_1875.jpg).
- Clean, aligned, elegant layouts with high technical rigor.
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
# MODERN SPORTS-ANALYTICS COLOR PALETTE
# ==========================================
NAVY_DEEP = RGBColor(15, 23, 42)        # #0F172A (Primary Heading / Dark Panels)
NAVY_SLATE = RGBColor(30, 41, 59)       # #1E293B (Secondary Dark)
EMERALD_PITCH = RGBColor(5, 150, 105)   # #059669 (Football Pitch Green - Primary Accent)
EMERALD_BRIGHT = RGBColor(16, 185, 129) # #10B981 (Active Green Accent)
COBALT_BLUE = RGBColor(37, 99, 235)     # #2563EB (Tech / Key Accent)
CYAN_ACCENT = RGBColor(2, 132, 199)     # #0284C7 (Secondary Blue)

WHITE_BG = RGBColor(255, 255, 255)      # Pure White Canvas
CARD_BG = RGBColor(248, 250, 252)       # Soft Cool Slate (#F8FAFC)
CARD_BORDER = RGBColor(226, 232, 240)   # Subtle Border (#E2E8F0)
CODE_BG = RGBColor(11, 19, 37)          # Sleek Deep Navy/Charcoal (#0B1325)

TEXT_HEAD = RGBColor(15, 23, 42)        # Deep Navy Headings
TEXT_BODY = RGBColor(71, 85, 105)       # Neutral Slate
TEXT_MUTED = RGBColor(100, 116, 139)    # Muted Slate
TEXT_WHITE = RGBColor(255, 255, 255)    # White
TEXT_CODE = RGBColor(241, 245, 249)     # Light Monospace Text

FONT_HEAD = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_bg(slide, color=WHITE_BG):
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
    # SLIDE 1: Title Slide (Clean, Minimalist, Academic)
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_bg(slide1, WHITE_BG)

    # Top accent bar across the slide
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
    p2.text = "This case study designs, normalizes, and implements a high-performance relational database architecture tailored for professional football analysis. Built upon the FOOTPASS spatiotemporal tracking benchmark (UEFA Champions League match footage), the system structures high-frequency player trajectories, team line compactness, and 100K+ play-by-play events into 3NF relational tables supporting real-time declarative SQL querying."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_BODY
    p2.space_before = Pt(4)

    # Student Details Cards
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
    p.text = "School of Computer Science & Engineering · Department of Computer Science · Fall 2026"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Table of Contents / Agenda
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_bg(slide2, WHITE_BG)
    add_header(slide2, "TABLE OF CONTENTS", "Presentation Agenda & Technical Coverage")
    add_footer(slide2, 2)

    agenda_items = [
        ("01", "Domain & Problem Analysis", "Technical bottlenecks in raw match video and unlinked tracking streams"),
        ("02", "System Personas & Business Rules", "Coaching inquiry workflows and core relational integrity constraints"),
        ("03", "Relational Data Model & Keys", "6 normalized entities, candidate keys, and foreign key hierarchy"),
        ("04", "DDL Schema Construction", "Building the relational tables using standard DDL with inline constraints"),
        ("05", "Data Integrity Constraints", "Implementation of PK, FK, UNIQUE, NOT NULL, CHECK, and DEFAULT"),
        ("06", "DML Data Lifecycle", "Inserting match fixtures, updating player states, and purging tracking noise"),
        ("07", "Transformation & CASE Queries", "Single-row scalar functions and dynamic tactical phase classification"),
        ("08", "Aggregates & Statistical Grouping", "Analytical queries using COUNT, AVG, MIN, MAX, SUM, and HAVING"),
    ]

    col_w = Inches(5.7)
    row_h = Inches(1.15)
    for i, (num, atitle, adesc) in enumerate(agenda_items):
        col = i // 4
        row = i % 4
        x = Inches(0.8) + col * Inches(6.05)
        y = Inches(1.7) + row * Inches(1.25)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Left color bar
        bar = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(0.12), row_h)
        bar.fill.solid()
        bar.fill.fore_color.rgb = EMERALD_PITCH if col == 0 else COBALT_BLUE
        bar.line.fill.background()

        # Number Box
        nbox = slide2.shapes.add_textbox(x + Inches(0.25), y + Inches(0.15), Inches(0.7), Inches(0.6))
        tf_n = nbox.text_frame
        tf_n.margin_left = tf_n.margin_top = 0
        p = tf_n.paragraphs[0]
        p.text = num
        p.font.name = FONT_HEAD
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        # Text
        tbox = slide2.shapes.add_textbox(x + Inches(0.95), y + Inches(0.18), col_w - Inches(1.1), Inches(0.8))
        tf_t = tbox.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = 0
        p = tf_t.paragraphs[0]
        p.text = atitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf_t.add_paragraph()
        p2.text = adesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 3: Domain & Problem Analysis (ACTUAL FOOTBALL PITCH ACTION IMAGE)
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_bg(slide3, WHITE_BG)
    add_header(slide3, "01 · DOMAIN & PROBLEM ANALYSIS", "Challenges in Spatiotemporal Football Data")
    add_footer(slide3, 3)

    # Left Column: Problem Breakdown
    left_x = Inches(0.8)
    left_w = Inches(6.0)

    prob_cards = [
        ("Unstructured Broadcast Video", "Television broadcast footage captures visual play but lacks queryable structure. Coaches cannot execute SQL to filter game phases, isolate pressing triggers, or compute unit line heights directly from pixels."),
        ("Massive Unlinked Coordinate Logs", "Raw tracking datasets (1.7M+ frames per fixture in FOOTPASS H5) store coordinate streams without relational links to canonical rosters, official jersey numbers, or match context."),
        ("File-Based Analytics Silos", "Match schedules, spatial tracking, and play-by-play event logs reside in disconnected CSV/HDF5 files, preventing multi-match querying, defensive compactness comparisons, and historical joins."),
    ]

    for p_idx, (p_title, p_desc) in enumerate(prob_cards):
        py = Inches(1.65) + p_idx * Inches(1.25)
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, py, left_w, Inches(1.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Left tag icon/pill
        tag = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x + Inches(0.2), py + Inches(0.18), Inches(0.28), Inches(0.28))
        tag.fill.solid()
        tag.fill.fore_color.rgb = EMERALD_PITCH
        tag.line.fill.background()

        tb = slide3.shapes.add_textbox(left_x + Inches(0.65), py + Inches(0.15), left_w - Inches(0.85), Inches(0.85))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = p_title
        p.font.name = FONT_HEAD
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = p_desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(2)

    # Right Column: Actual Football Pitch Broadcast Frame
    right_x = Inches(7.1)
    right_w = Inches(5.4)

    pitch_img = os.path.join(ASSETS_DIR, "football_pitch_action.png")
    if os.path.exists(pitch_img):
        # Frame container
        pic_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, right_x, Inches(1.65), right_w, Inches(3.45))
        pic_box.fill.solid()
        pic_box.fill.fore_color.rgb = CARD_BG
        pic_box.line.color.rgb = CARD_BORDER

        slide3.shapes.add_picture(pitch_img, right_x + Inches(0.08), Inches(1.73), width=right_w - Inches(0.16), height=Inches(3.29))

    cap_box = slide3.shapes.add_textbox(right_x, Inches(5.15), right_w, Inches(0.55))
    tf_cap = cap_box.text_frame
    tf_cap.word_wrap = True
    tf_cap.margin_left = tf_cap.margin_top = tf_cap.margin_right = tf_cap.margin_bottom = 0
    p = tf_cap.paragraphs[0]
    p.text = "Figure 1: Authentic match broadcast tracking footage (game_39: Newcastle vs PSG) showing outfield player distribution, team orientation, and active jersey numbers on the pitch."
    p.font.name = FONT_BODY
    p.font.size = Pt(8.5)
    p.font.color.rgb = TEXT_MUTED

    # Bottom Objective Banner
    obj_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.75), Inches(11.7), Inches(0.95))
    obj_box.fill.solid()
    obj_box.fill.fore_color.rgb = NAVY_DEEP
    obj_box.line.color.rgb = EMERALD_PITCH
    obj_box.line.width = Pt(1.5)

    otb = slide3.shapes.add_textbox(Inches(1.05), Inches(5.85), Inches(11.2), Inches(0.8))
    tf_o = otb.text_frame
    tf_o.word_wrap = True
    tf_o.margin_left = tf_o.margin_top = 0
    p = tf_o.paragraphs[0]
    p.text = "DBMS Case Study Objective"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    p2 = tf_o.add_paragraph()
    p2.text = "To transform high-frequency spatial tracking and play-by-play event streams into a 3NF relational schema, enabling coaching staff and analysts to execute sub-second declarative SQL queries for formation line heights, unit compactness, and tactical action frequency."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(2)

    # =========================================================================
    # SLIDE 4: System Workflow & Data Pipeline
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_bg(slide4, WHITE_BG)
    add_header(slide4, "01 · SYSTEM WORKFLOW", "Data Pipeline: From Raw Video to Structured SQL")
    add_footer(slide4, 4)

    steps = [
        ("Step 1: Ingest & Synchronize", "Broadcast video (25 fps) and FOOTPASS H5 coordinate logs are ingested. Player bounding boxes and field coordinate vectors [X, Y] are aligned to match timestamps."),
        ("Step 2: Relational Validation", "Extracted coordinates and events are validated against relational constraints (CHECK, UNIQUE, FK) and normalized into 3NF tables in SQLite."),
        ("Step 3: Declarative SQL Analytics", "Coaches execute structured SQL queries to analyze pressing blocks, filter match events, and render synchronized 2D pitch overlays on the tactical dashboard."),
    ]

    card_w = Inches(3.7)
    card_h = Inches(1.8)
    for s_idx, (stitle, sdesc) in enumerate(steps):
        sx = Inches(0.8) + s_idx * Inches(4.0)
        sy = Inches(1.65)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx, sy, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Top step pill
        spill = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, sx + Inches(0.2), sy + Inches(0.18), Inches(1.8), Inches(0.32))
        spill.fill.solid()
        spill.fill.fore_color.rgb = EMERALD_PITCH if s_idx == 0 else (COBALT_BLUE if s_idx == 1 else NAVY_DEEP)
        spill.line.fill.background()
        p = spill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"PHASE {s_idx+1}"
        p.font.name = FONT_HEAD
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide4.shapes.add_textbox(sx + Inches(0.2), sy + Inches(0.58), card_w - Inches(0.4), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(3)

    # Bottom Split View: Left = Swagger API Docs, Right = Architectural Specs
    doc_img = os.path.join(ASSETS_DIR, "fastapi_docs_1792511905970.png")
    if os.path.exists(doc_img):
        doc_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.7), Inches(6.5), Inches(2.9))
        doc_box.fill.solid()
        doc_box.fill.fore_color.rgb = CARD_BG
        doc_box.line.color.rgb = CARD_BORDER

        slide4.shapes.add_picture(doc_img, Inches(0.9), Inches(3.8), width=Inches(6.3), height=Inches(2.7))

    # Right Architecture Box
    arch_box = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.55), Inches(3.7), Inches(4.95), Inches(2.9))
    arch_box.fill.solid()
    arch_box.fill.fore_color.rgb = CARD_BG
    arch_box.line.color.rgb = CARD_BORDER

    atb = slide4.shapes.add_textbox(Inches(7.8), Inches(3.9), Inches(4.5), Inches(2.5))
    tf_a = atb.text_frame
    tf_a.word_wrap = True
    tf_a.margin_left = tf_a.margin_top = 0
    p = tf_a.paragraphs[0]
    p.text = "ARCHITECTURE SPECIFICATIONS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_DEEP

    specs = [
        ("Presentation Layer", "React + Vite SPA with frame-accurate timeline scrubber and 2D canvas overlay."),
        ("Application Layer", "FastAPI asynchronous service executing spatial queries and partial content video streaming."),
        ("Database Layer", "Relational SQLite/SQL engine enforcing 3NF schema, referential keys, and check constraints."),
        ("Analytical Engine", "TacticalEngine computing line heights, unit compactness, and space creation metrics."),
    ]
    for sp_title, sp_desc in specs:
        p = tf_a.add_paragraph()
        p.text = f"• {sp_title}: "
        p.font.name = FONT_HEAD
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COBALT_BLUE
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = sp_desc
        run.font.name = FONT_BODY
        run.font.size = Pt(8.5)
        run.font.bold = False
        run.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 5: System Stakeholders & Business Rules
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_bg(slide5, WHITE_BG)
    add_header(slide5, "02 · SYSTEM STAKEHOLDERS & RULES", "User Personas, Functional Needs & Data Integrity Rules")
    add_footer(slide5, 5)

    # Left Column: User Personas
    left_x = Inches(0.8)
    left_w = Inches(5.6)

    who_title = slide5.shapes.add_textbox(left_x, Inches(1.5), left_w, Inches(0.3))
    p = who_title.text_frame.paragraphs[0]
    p.text = "SYSTEM STAKEHOLDERS & NEEDS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    actors = [
        ("Head Coach", "Requires high-level tactical summaries: opponent defensive block height, team width/compactness, and flank overload patterns."),
        ("Tactical Analyst", "Executes complex declarative SQL queries to evaluate set-piece success, player pass completion, and pressing triggers."),
        ("Analytics Engineer", "Manages automated ingestion of broadcast tracking feeds, verifies schema constraints, and optimizes table indexes."),
    ]
    for j, (role, rdesc) in enumerate(actors):
        ay = Inches(1.85) + j * Inches(0.85)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, ay, left_w, Inches(0.75))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        tb = slide5.shapes.add_textbox(left_x + Inches(0.2), ay + Inches(0.1), left_w - Inches(0.4), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = role
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP
        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_BODY

    req_title = slide5.shapes.add_textbox(left_x, Inches(4.6), left_w, Inches(0.3))
    p = req_title.text_frame.paragraphs[0]
    p.text = "CORE FUNCTIONAL REQUIREMENTS"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    reqs = [
        "• Maintain canonical club rosters and official competition match fixtures.",
        "• Guarantee chronological sequence consistency across match halves.",
        "• Provide sub-second query performance on 100K+ play-by-play events.",
        "• Automatically classify tactical macro-states (High Press, Mid Block, Low Block).",
    ]
    req_box = slide5.shapes.add_textbox(left_x, Inches(4.9), left_w, Inches(1.8))
    tf_r = req_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = 0
    for idx, rtext in enumerate(reqs):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.text = rtext
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY
        p.space_after = Pt(3)

    # Right Column: Business Rules & Block Rules
    right_x = Inches(6.9)
    right_w = Inches(5.6)

    rule_title = slide5.shapes.add_textbox(right_x, Inches(1.5), right_w, Inches(0.3))
    p = rule_title.text_frame.paragraphs[0]
    p.text = "RELATIONAL DATA INTEGRITY RULES"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    b_rules = [
        ("Valid Squad Numbers", "CHECK (shirt_number BETWEEN 1 AND 99)"),
        ("Distinct Fixture Clubs", "CHECK (home_team <> away_team)"),
        ("Single Jersey per Club", "UNIQUE (team_code, shirt_number)"),
        ("Valid Match Period", "CHECK (half IN (1, 2))"),
        ("Normalized Coordinates", "CHECK (centroid_x BETWEEN 0.0 AND 1.0)"),
    ]
    for k, (bname, bsql) in enumerate(b_rules):
        by = Inches(1.85) + k * Inches(0.55)
        rb = slide5.shapes.add_textbox(right_x, by, right_w, Inches(0.5))
        tf = rb.text_frame
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = bname + "  "
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP
        run = p.add_run()
        run.text = bsql
        run.font.name = FONT_CODE
        run.font.size = Pt(9)
        run.font.color.rgb = COBALT_BLUE

    # Tactical Classification Rules
    badge_title = slide5.shapes.add_textbox(right_x, Inches(4.7), right_w, Inches(0.3))
    p = badge_title.text_frame.paragraphs[0]
    p.text = "TACTICAL BLOCK CLASSIFICATION"
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_PITCH

    block_rules = [
        ("High Press Block", "Centroid X >= 0.55\nUnit Length < 35m"),
        ("Midfield Structure", "Centroid X BETWEEN\n0.35 AND 0.55"),
        ("Deep Low Block", "Centroid X < 0.35\nBackline < 20m"),
    ]
    bw = Inches(1.75)
    for m, (b_name, b_desc) in enumerate(block_rules):
        bx = right_x + m * Inches(1.9)
        by = Inches(5.05)
        bcard = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, Inches(1.6))
        bcard.fill.solid()
        bcard.fill.fore_color.rgb = CARD_BG
        bcard.line.color.rgb = CARD_BORDER

        btb = slide5.shapes.add_textbox(bx + Inches(0.1), by + Inches(0.15), bw - Inches(0.2), Inches(1.3))
        tf = btb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = b_name
        p.font.name = FONT_HEAD
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = b_desc
        p2.font.name = FONT_CODE
        p2.font.size = Pt(9)
        p2.font.color.rgb = EMERALD_PITCH
        p2.space_before = Pt(8)

    # =========================================================================
    # SLIDE 6: Relational Data Model & Keys
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_bg(slide6, WHITE_BG)
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

    ew = Inches(3.7)
    eh = Inches(1.75)
    for i, (ename, edesc) in enumerate(entities):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.6) + row * Inches(1.95)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ew, eh)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER

        # Top entity pill
        epill = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.2), y + Inches(0.18), Inches(1.8), Inches(0.32))
        epill.fill.solid()
        epill.fill.fore_color.rgb = NAVY_DEEP
        epill.line.fill.background()
        p = epill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = ename
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.2), y + Inches(0.6), ew - Inches(0.4), eh - Inches(0.7))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = edesc
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_BODY

    # Bottom 4 Key Cards
    keys = [
        ("PK", "Primary Key", "Unique identifier for each record — team_code, match_id, player_id, event_id"),
        ("FK", "Foreign Key", "Referential link preserving integrity — matches.home_team -> teams(team_code)"),
        ("UQ", "Candidate Key", "Enforces non-duplicate attributes — UNIQUE(team_code, shirt_number)"),
        ("CK", "Composite Key", "Multi-column temporal uniqueness — (match_id, half, frame_idx, jersey)"),
    ]
    kw = Inches(2.75)
    kh = Inches(1.35)
    for k, (kcode, ktitle, kdesc) in enumerate(keys):
        x = Inches(0.8) + k * Inches(3.0)
        y = Inches(5.5)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, kw, kh)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Pill badge
        pbox = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), y + Inches(0.18), Inches(0.6), Inches(0.32))
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = EMERALD_PITCH if k % 2 == 0 else COBALT_BLUE
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
    # SLIDE 7: ER Architecture
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_bg(slide7, WHITE_BG)
    add_header(slide7, "03 · ER ARCHITECTURE", "Entity-Relationship (ER) Schema & Cardinalities")
    add_footer(slide7, 7)

    er_path = os.path.join(ASSETS_DIR, "er_diagram_v2.png")
    if os.path.exists(er_path):
        slide7.shapes.add_picture(er_path, Inches(0.8), Inches(1.5), width=Inches(11.7))

    # =========================================================================
    # SLIDE 8: DDL Implementation: Schema Construction
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_bg(slide8, WHITE_BG)
    add_header(slide8, "04 · DDL IMPLEMENTATION", "DDL Schema Construction & Table Definitions")
    add_footer(slide8, 8)

    # Box 1: teams & matches
    box1_x, box1_y, box1_w, box1_h = Inches(0.8), Inches(1.55), Inches(5.7), Inches(4.3)
    c1 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box1_x, box1_y, box1_w, box1_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CODE_BG
    c1.line.color.rgb = RGBColor(30, 41, 59)

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
    c2.line.color.rgb = RGBColor(30, 41, 59)

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
    # SLIDE 9: Schema Evolution (ALTER & DROP)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_bg(slide9, WHITE_BG)
    add_header(slide9, "04 · SCHEMA EVOLUTION", "ALTER & DROP: Managing Migrations & Table Lifecycles")
    add_footer(slide9, 9)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(6.8), Inches(4.5)
    c = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(30, 41, 59)

    tb = slide9.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Production Schema Migration Scripts"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    alter_sql = """-- 1. ADD: Expand player metrics with market valuation
ALTER TABLE players ADD COLUMN market_value_eur NUMERIC(12,2);

-- 2. ALTER: Modify column precision or rename attributes
ALTER TABLE players RENAME COLUMN player_name TO full_name;

-- 3. ADD CONSTRAINT: Enforce event timestamp non-negativity
ALTER TABLE match_events ADD CONSTRAINT chk_event_sec
CHECK (event_second >= 0.0);

-- 4. DROP COLUMN: Deprecate legacy sensor features
ALTER TABLE players DROP COLUMN market_value_eur;

-- 5. DROP TABLE: Managed lifecycle removal (children first)
DROP TABLE match_events;
DROP TABLE tactical_snapshots;
DROP TABLE matches;"""

    p2 = tf.add_paragraph()
    p2.text = alter_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(6)

    # Right Action Chips
    chips = [
        ("ADD COLUMN", "Incorporates new telemetry attributes or tracking sensor parameters."),
        ("RENAME / MODIFY", "Alters attribute names or adjusts precision without data loss."),
        ("ADD CONSTRAINT", "Enforces new tactical domain rules post-table creation."),
        ("DROP COLUMN", "Purges deprecated legacy or redundant tracking fields."),
        ("DROP TABLE", "Permanently deletes a relation following dependency hierarchy."),
    ]
    for ch_idx, (cname, cdesc) in enumerate(chips):
        cy = Inches(1.55) + ch_idx * Inches(0.9)
        btn = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), cy, Inches(1.6), Inches(0.45))
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

        dtb = slide9.shapes.add_textbox(Inches(9.8), cy + Inches(0.02), Inches(2.7), Inches(0.75))
        tf_d = dtb.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]
        p.text = cdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_BODY

    # Bottom Callout Box (Clean Slate with Emerald Border)
    tip = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    tip.fill.solid()
    tip.fill.fore_color.rgb = CARD_BG
    tip.line.color.rgb = EMERALD_PITCH
    tip.line.width = Pt(1.2)

    ttb = slide9.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.5))
    tf_tip = ttb.text_frame
    tf_tip.margin_left = tf_tip.margin_top = 0
    p = tf_tip.paragraphs[0]
    p.text = "Referential Integrity Guideline: Always drop child relations (match_events, tactical_snapshots) before parent tables (matches, teams) to avoid foreign key violation locks."
    p.font.name = FONT_HEAD
    p.font.size = Pt(9.5)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 10: Relational Integrity Constraints
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_bg(slide10, WHITE_BG)
    add_header(slide10, "05 · INTEGRITY CONSTRAINTS", "Relational Constraints for Tactical Data Validation")
    add_footer(slide10, 10)

    constraints = [
        ("PK", "PRIMARY KEY", "Enforces entity identity with unique, non-null values. Used in team_code, match_id, player_id, and event_id."),
        ("FK", "FOREIGN KEY", "Preserves referential integrity across fixtures and squads. matches.home_team -> teams with ON DELETE CASCADE."),
        ("UQ", "UNIQUE KEY", "Guarantees no duplicate assignments. team_name, and composite candidate key UNIQUE(team_code, shirt_number)."),
        ("NN", "NOT NULL", "Mandates essential business values. player_name, action_type, competition must never contain missing values."),
        ("CHK", "CHECK", "Validates tactical domain bounds. shirt_number 1–99, role_id 1–13, and home_team <> away_team."),
        ("DEF", "DEFAULT", "Supplies automated defaults. season = '2023-2024', fps = 25.0, and success_flag = 1."),
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
    # SLIDE 11: DML Operations (Data Lifecycle)
    # =========================================================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_bg(slide11, WHITE_BG)
    add_header(slide11, "06 · DML OPERATIONS", "Match Event Lifecycle: INSERT, UPDATE & DELETE")
    add_footer(slide11, 11)

    dml_sections = [
        ("INSERT", "Record Ingestion", """INSERT INTO teams VALUES
('NEW', 'Newcastle United',
 'ENG', 'St. James'' Park', '#F8FAFC');

INSERT INTO matches VALUES
('game_39', 'UEFA Champions League',
 '2023-2024', DATE '2023-10-04',
 'NEW', 'PAR', 155054, 6202.16, 25.0);

INSERT INTO match_events
(event_id, match_id, half,
 frame_idx, event_second, team_code,
 jersey_number, action_type, success_flag)
VALUES (101, 'game_39', 1, 252,
        10.08, 'NEW', 9, 'Pass', 1);"""),

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

        ("DELETE", "Data Sanitization", """-- 1. Purge corrupted tracking sensor noise
DELETE FROM match_events
WHERE frame_idx < 0
   OR event_second > 7200.0;

-- 2. Remove cancelled friendly fixture
DELETE FROM matches
WHERE competition = 'Exhibition Friendly'
  AND season = '2023-2024';

-- 3. Clean obsolete coaching annotations
DELETE FROM tactical_rules
WHERE rule_id = 'RULE_DEPRECATED';"""),
    ]

    col_w = Inches(3.7)
    for i, (action, tag, sql_code) in enumerate(dml_sections):
        x = Inches(0.8) + i * Inches(4.0)

        # Header pill
        hpill = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(1.3), Inches(0.35))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = EMERALD_PITCH if i == 0 else (COBALT_BLUE if i == 1 else NAVY_DEEP)
        hpill.line.fill.background()
        p = hpill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = action
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        sub_t = slide11.shapes.add_textbox(x + Inches(1.4), Inches(1.52), Inches(2.2), Inches(0.35))
        p = sub_t.text_frame.paragraphs[0]
        p.text = tag
        p.font.name = FONT_HEAD
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_BODY

        # Code box
        c = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.95), col_w, Inches(4.75))
        c.fill.solid()
        c.fill.fore_color.rgb = CODE_BG
        c.line.color.rgb = RGBColor(30, 41, 59)

        tb = slide11.shapes.add_textbox(x + Inches(0.2), Inches(2.1), col_w - Inches(0.4), Inches(4.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = f"-- {action.lower()}_operations.sql"
        p.font.name = FONT_CODE
        p.font.size = Pt(9)
        p.font.color.rgb = EMERALD_BRIGHT

        p2 = tf.add_paragraph()
        p2.text = sql_code
        p2.font.name = FONT_CODE
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = TEXT_CODE
        p2.space_before = Pt(6)

    # =========================================================================
    # SLIDE 12: Data Transformation (Single-Row Functions)
    # =========================================================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_bg(slide12, WHITE_BG)
    add_header(slide12, "07 · DATA TRANSFORMATION", "Single-Row Functions for Tactical Formatting")
    add_footer(slide12, 12)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(3.8)
    c = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(30, 41, 59)

    tb = slide12.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Single-Row Scalar Transformation Query"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = EMERALD_BRIGHT

    q12_sql = """SELECT player_id,
       UPPER(player_name) AS name_caps,
       LOWER(team_code)   AS team_lower,
       SUBSTR(position, 1, 2) AS pos_code,
       'ROLE-' || substr('00' || role_id, -2) AS tier
FROM players
WHERE team_code = 'NEW'
ORDER BY shirt_number;"""

    p2 = tf.add_paragraph()
    p2.text = q12_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide12.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (5 sample records)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    rows12 = [
        ("ID", "Name (UPPER)", "Team", "Pos", "Tactical Tier"),
        ("1", "KIERAN TRIPPIER", "new", "RB", "ROLE-13"),
        ("2", "FABIAN SCHÄR", "new", "CB", "ROLE-03"),
        ("3", "JAMAAL LASCELLES", "new", "CB", "ROLE-05"),
        ("4", "SANDRO TONALI", "new", "CM", "ROLE-06"),
        ("5", "ANTHONY GORDON", "new", "LW", "ROLE-10"),
    ]

    t_shape = slide12.shapes.add_table(6, 5, Inches(6.6), Inches(2.0), Inches(5.9), Inches(2.8))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(0.6)
    tbl.columns[1].width = Inches(2.2)
    tbl.columns[2].width = Inches(0.9)
    tbl.columns[3].width = Inches(0.8)
    tbl.columns[4].width = Inches(1.4)

    for r_idx, r_data in enumerate(rows12):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_HEAD if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DEEP
            else:
                p.font.color.rgb = TEXT_HEAD
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom Callout Box (Clean Slate with Emerald Accent)
    card_sw = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1))
    card_sw.fill.solid()
    card_sw.fill.fore_color.rgb = CARD_BG
    card_sw.line.color.rgb = EMERALD_PITCH
    card_sw.line.width = Pt(1.2)

    tb_sw = slide12.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(0.9))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_top = 0
    p = tf_sw.paragraphs[0]
    p.text = "Mathematical & Scalar Principle: Single-row functions operate deterministically on individual record attributes to return exactly one scalar value per row — formatting player rosters, generating normalized lookup codes, and padding hierarchical role keys."
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 13: Conditional Computation & CASE
    # =========================================================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_bg(slide13, WHITE_BG)
    add_header(slide13, "07 · CONDITIONAL COMPUTATION", "Numeric Computations & Dynamic CASE Classifications")
    add_footer(slide13, 13)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(4.7)
    c = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(30, 41, 59)

    tb = slide13.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Numeric Rounding & CASE Categorization"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = EMERALD_BRIGHT

    q13_sql = """SELECT action_type,
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
    p2.text = q13_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide13.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (Match game_39 events)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    rows13 = [
        ("Action", "Time (s)", "Match Min", "Tactical Phase"),
        ("Pass", "10.08", "0.17", "Ball Circulation"),
        ("Pass", "10.84", "0.18", "Ball Circulation"),
        ("Pass", "15.12", "0.25", "Ball Circulation"),
        ("Shot", "21.64", "0.36", "High Threat Attack"),
        ("Pass", "24.64", "0.41", "Ball Circulation"),
        ("Pass", "26.20", "0.44", "Ball Circulation"),
        ("Pass", "27.04", "0.45", "Ball Circulation"),
    ]

    t_shape = slide13.shapes.add_table(8, 4, Inches(6.6), Inches(2.0), Inches(5.9), Inches(4.3))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(1.1)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.3)
    tbl.columns[3].width = Inches(2.4)

    for r_idx, r_data in enumerate(rows13):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_HEAD if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DEEP
            else:
                p.font.color.rgb = TEXT_HEAD
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom summary tag
    sum_b = slide13.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.4))
    p = sum_b.text_frame.paragraphs[0]
    p.text = "Mathematical Analysis: The CASE expression enables dynamic branch classification of match play on the fly, while ROUND() converts raw spatiotemporal elapsed seconds into standardized match minutes."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_BODY

    # =========================================================================
    # SLIDE 14: Relational Query Operators
    # =========================================================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_bg(slide14, WHITE_BG)
    add_header(slide14, "08 · QUERY OPERATORS", "Pattern Matching & Range Filtering: BETWEEN, IN & LIKE")
    add_footer(slide14, 14)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(3.8)
    c = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(30, 41, 59)

    tb = slide14.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Relational Operator Filtering Query"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = EMERALD_BRIGHT

    q14_sql = """SELECT player_name,
       shirt_number,
       team_code,
       position
FROM players
WHERE shirt_number BETWEEN 7 AND 25
  AND team_code IN ('NEW', 'PAR', 'BAY')
  AND player_name LIKE '%a%'
ORDER BY shirt_number;"""

    p2 = tf.add_paragraph()
    p2.text = q14_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide14.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "EXECUTED QUERY OUTPUT  (Filtered squad records)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    rows14 = [
        ("Player Name", "Shirt #", "Club", "Position"),
        ("Serge Gnabry", "7", "BAY", "FW"),
        ("Leon Goretzka", "8", "BAY", "CM"),
        ("Sandro Tonali", "8", "NEW", "CM"),
        ("Harry Kane", "9", "BAY", "CF"),
    ]

    t_shape = slide14.shapes.add_table(5, 4, Inches(6.6), Inches(2.0), Inches(5.9), Inches(2.6))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(2.5)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.1)
    tbl.columns[3].width = Inches(1.3)

    for r_idx, r_data in enumerate(rows14):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_HEAD if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DEEP
            else:
                p.font.color.rgb = TEXT_HEAD
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom Callout Box (Clean Slate with Cobalt Border)
    card_sw = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1))
    card_sw.fill.solid()
    card_sw.fill.fore_color.rgb = CARD_BG
    card_sw.line.color.rgb = COBALT_BLUE
    card_sw.line.width = Pt(1.2)

    tb_sw = slide14.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(0.9))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_top = 0
    p = tf_sw.paragraphs[0]
    p.text = "Relational Set Filtering: BETWEEN tests continuous inclusive range boundaries [7..25], IN verifies membership against discrete relation sets ('NEW', 'PAR', 'BAY'), and LIKE '%a%' evaluates wildcard string patterns. Conjunctions (AND) guarantee strict intersection."
    p.font.name = FONT_HEAD
    p.font.size = Pt(10)
    p.font.color.rgb = NAVY_DEEP

    # =========================================================================
    # SLIDE 15: Aggregate Analytics & Grouping
    # =========================================================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_bg(slide15, WHITE_BG)
    add_header(slide15, "08 · AGGREGATE ANALYTICS", "Statistical Aggregations & Grouping with HAVING")
    add_footer(slide15, 15)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(4.8), Inches(5.0)
    c = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(30, 41, 59)

    tb = slide15.shapes.add_textbox(c_x + Inches(0.2), c_y + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "-- Aggregates with HAVING Condition"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = EMERALD_BRIGHT

    q15_sql = """SELECT team_code,
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
    p2.text = q15_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9)
    p2.font.color.rgb = TEXT_CODE
    p2.space_before = Pt(6)

    # Right Output Table
    out_lbl = slide15.shapes.add_textbox(Inches(5.9), Inches(1.55), Inches(6.6), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "AGGREGATE QUERY OUTPUT  (Across 1,000 match events)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COBALT_BLUE

    rows15 = [
        ("Club", "Actions", "Avg (s)", "Min (s)", "Max (s)", "Passes"),
        ("RSO", "203", "225.66", "1.72", "510.64", "102"),
        ("NEW", "172", "367.30", "10.08", "741.68", "91"),
        ("BVB", "166", "262.63", "6.72", "522.24", "83"),
        ("BAY", "150", "370.96", "6.08", "791.08", "73"),
        ("MUN", "100", "460.59", "11.68", "749.76", "46"),
        ("PAR", "78", "425.48", "15.12", "683.60", "45"),
    ]

    t_shape = slide15.shapes.add_table(7, 6, Inches(5.9), Inches(1.9), Inches(6.6), Inches(2.2))
    tbl = t_shape.table
    tbl.columns[0].width = Inches(0.9)
    tbl.columns[1].width = Inches(1.1)
    tbl.columns[2].width = Inches(1.2)
    tbl.columns[3].width = Inches(1.1)
    tbl.columns[4].width = Inches(1.1)
    tbl.columns[5].width = Inches(1.2)

    for r_idx, r_data in enumerate(rows15):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_HEAD if r_idx == 0 else FONT_CODE
            p.font.size = Pt(8.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_DEEP
            else:
                p.font.color.rgb = TEXT_HEAD
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Right Chart below table (Emerald Green Theme)
    chart_path = os.path.join(ASSETS_DIR, "slide15_passes_chart_v2.png")
    if os.path.exists(chart_path):
        slide15.shapes.add_picture(chart_path, Inches(6.1), Inches(4.25), width=Inches(6.2))

    # =========================================================================
    # SLIDE 16: Project Milestones & Review 2 Scope
    # =========================================================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_bg(slide16, WHITE_BG)
    add_header(slide16, "PROJECT MILESTONES", "Review 1 Accomplishments & Phase 2 Technical Scope")
    add_footer(slide16, 16)

    summary_points = [
        ("Normalized Relational Schema", "Designed 6 core 3NF tables eliminating redundancy across clubs, fixtures, rosters, and tracking events."),
        ("Stakeholders & Domain Integrity", "Defined personas (Coach, Analyst, Engineer) and enforced multi-layer constraints (CHECK, UNIQUE, FK)."),
        ("Comprehensive ER Architecture", "Developed robust ER schema with strict primary/foreign key hierarchies and explicit 1:N / M:N cardinalities."),
        ("Validated DDL Schema Construction", "Implemented syntactically correct DDL with domain bounds, default parameters, and cascade specifications."),
        ("Audited DML Data Operations", "Established verified data ingestion, player position updating, and sensor noise deletion pipelines."),
        ("Analytical Query Execution", "Executed scalar transformations, dynamic CASE classifications, and statistical group aggregations on live data."),
    ]

    sy_start = Inches(1.6)
    for s_idx, (stitle, sdesc) in enumerate(summary_points):
        sy = sy_start + s_idx * Inches(0.85)

        # Checkmark badge
        chk = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), sy, Inches(0.38), Inches(0.38))
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

        # Text
        stb = slide16.shapes.add_textbox(Inches(1.3), sy, Inches(5.9), Inches(0.75))
        tf = stb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.name = FONT_HEAD
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY_DEEP

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_BODY
        p2.space_before = Pt(1)

    # Right Card: PHASE 2 TECHNICAL ROADMAP
    rc_x, rc_y, rc_w, rc_h = Inches(7.6), Inches(1.6), Inches(4.9), Inches(5.0)
    rc = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_x, rc_y, rc_w, rc_h)
    rc.fill.solid()
    rc.fill.fore_color.rgb = NAVY_DEEP
    rc.line.color.rgb = EMERALD_PITCH
    rc.line.width = Pt(1.5)

    nxt_box = slide16.shapes.add_textbox(rc_x + Inches(0.4), rc_y + Inches(0.35), rc_w - Inches(0.8), Inches(4.3))
    tf_nxt = nxt_box.text_frame
    tf_nxt.word_wrap = True
    tf_nxt.margin_left = tf_nxt.margin_top = 0
    p = tf_nxt.paragraphs[0]
    p.text = "PHASE 2 TECHNICAL ROADMAP"
    p.font.name = FONT_HEAD
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD_BRIGHT

    p_sub = tf_nxt.add_paragraph()
    p_sub.text = "Advanced DBMS Features & Query Optimization"
    p_sub.font.name = FONT_HEAD
    p_sub.font.size = Pt(10)
    p_sub.font.color.rgb = RGBColor(148, 163, 184)
    p_sub.space_before = Pt(2)

    r2_topics = [
        ("Multi-Table Relational JOINs", "Inner, Left, and Full Outer Joins linking matches, players, events, and spatial metrics."),
        ("Complex Correlated Subqueries", "Subqueries in SELECT, WHERE, and HAVING to compute comparative player percentiles."),
        ("Indexed Materialized Views", "Pre-computed tactical summary views for real-time coach interval dashboards."),
        ("PL/SQL Procedures & Functions", "Modular server-side algorithms computing pressing intensity (PPDA) directly in the DBMS."),
        ("Event Triggers & Cursors", "Automated database triggers alerting analysts when line compression breaches critical thresholds."),
    ]
    for r_title, r_desc in r2_topics:
        p = tf_nxt.add_paragraph()
        p.text = f"• {r_title}: "
        p.font.name = FONT_HEAD
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_before = Pt(8)
        run = p.add_run()
        run.text = r_desc
        run.font.name = FONT_BODY
        run.font.size = Pt(8.5)
        run.font.bold = False
        run.font.color.rgb = RGBColor(203, 213, 225)

    p_end = tf_nxt.add_paragraph()
    p_end.text = "Phase 1 Review Completed  ·  Ready for Defense & Evaluation"
    p_end.font.name = FONT_HEAD
    p_end.font.size = Pt(9.5)
    p_end.font.bold = True
    p_end.font.color.rgb = EMERALD_BRIGHT
    p_end.space_before = Pt(14)

    # Save presentation
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prs.save(PPTX_PATH)
    print(f"Redesigned presentation saved successfully to: {PPTX_PATH}")

if __name__ == '__main__':
    build_presentation()
