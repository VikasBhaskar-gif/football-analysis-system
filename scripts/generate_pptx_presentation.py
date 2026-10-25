"""
generate_pptx_presentation.py
==============================
Generates the complete, professional 16-slide PowerPoint presentation:
'Football_Tactical_Analytics_DBMS_Review_1.pptx'
matching the exact design, formatting, and layout of FLAVRD_Review_1_Simple.pdf.
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

# Palette constants matching FLAVRD
BG_DARK = RGBColor(24, 25, 28)          # #18191C
BG_CARD_DARK = RGBColor(34, 36, 40)     # #222428
BG_LIGHT = RGBColor(248, 249, 250)      # #F8F9FA
CARD_FILL = RGBColor(241, 245, 249)     # #F1F5F9
CARD_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
CODE_BG = RGBColor(24, 26, 31)          # #181A1F
CODE_HEADER_BG = RGBColor(38, 41, 48)   # #262930

TEXT_WHITE = RGBColor(255, 255, 255)
TEXT_MUTED = RGBColor(148, 163, 184)    # #94A3B8
TEXT_DARK = RGBColor(15, 23, 42)        # #0F172A
TEXT_SUB = RGBColor(71, 85, 105)        # #475569
GOLD_ACCENT = RGBColor(197, 155, 39)    # #C59B27
GOLD_BRIGHT = RGBColor(212, 175, 55)    # #D4AF37
GOLD_MUTED = RGBColor(180, 83, 9)       # #B45309

FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"
FONT_CODE = "Consolas"

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, section_tag, title_text, dark=False):
        # Section tag
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.4))
        tf = tag_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = section_tag.upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = GOLD_BRIGHT if dark else GOLD_MUTED

        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(10), Inches(0.7))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title_text
        p2.font.name = FONT_HEADING
        p2.font.size = Pt(26)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE if dark else TEXT_DARK

        # Top Right Emblem
        emblem_path = os.path.join(ASSETS_DIR, "gold_emblem.png")
        if os.path.exists(emblem_path):
            slide.shapes.add_picture(emblem_path, Inches(12.2), Inches(0.4), width=Inches(0.65))

    def add_footer(slide, slide_num, dark=False):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(10), Inches(0.3))
        tf = footer_box.text_frame
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = "Football Tactical Analytics Database · Review 1 · Case Study Analysis & Basic SQL · DBMS"
        p.font.name = FONT_BODY
        p.font.size = Pt(8.5)
        p.font.color.rgb = TEXT_MUTED if dark else RGBColor(100, 116, 139)

        num_box = slide.shapes.add_textbox(Inches(12.0), Inches(7.05), Inches(0.7), Inches(0.3))
        tf_num = num_box.text_frame
        tf_num.margin_left = tf_num.margin_top = tf_num.margin_right = tf_num.margin_bottom = 0
        p_num = tf_num.paragraphs[0]
        p_num.alignment = PP_ALIGN.RIGHT
        p_num.text = str(slide_num)
        p_num.font.name = FONT_BODY
        p_num.font.size = Pt(8.5)
        p_num.font.color.rgb = TEXT_MUTED if dark else RGBColor(100, 116, 139)

    def set_slide_background(slide, color):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = color

    # ==========================================
    # SLIDE 1: Title Slide (Dark)
    # ==========================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1, BG_DARK)

    # Review header
    tag1 = slide1.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(8), Inches(0.4))
    tf1 = tag1.text_frame
    tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]
    p.text = "REVIEW 1 · CASE STUDY ANALYSIS & BASIC SQL"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT

    # Big Title
    tbox = slide1.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(8), Inches(1.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "FOOTBALL TACTICAL"
    p.font.name = FONT_HEADING
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p_sub = tf.add_paragraph()
    p_sub.text = "ANALYTICS DATABASE"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(40)
    p_sub.font.bold = True
    p_sub.font.color.rgb = TEXT_WHITE

    # Taglines
    tagline_box = slide1.shapes.add_textbox(Inches(0.9), Inches(3.3), Inches(7.5), Inches(0.9))
    tf_tag = tagline_box.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_left = tf_tag.margin_top = 0
    p1 = tf_tag.paragraphs[0]
    p1.text = "Query the pitch."
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(18)
    p1.font.bold = True
    p1.font.color.rgb = GOLD_ACCENT

    p2 = tf_tag.add_paragraph()
    p2.text = "Decode the tactics."
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = GOLD_ACCENT

    # Description
    desc_box = slide1.shapes.add_textbox(Inches(0.9), Inches(4.3), Inches(7.2), Inches(0.8))
    tf_desc = desc_box.text_frame
    tf_desc.word_wrap = True
    tf_desc.margin_left = tf_desc.margin_top = 0
    p = tf_desc.paragraphs[0]
    p.text = "A relational database management system organizing broadcast tracking, team structures, spatiotemporal metrics, and play-by-play tactical events from top European football matches."
    p.font.name = FONT_BODY
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(203, 213, 225)

    # Submitted By Header
    sub_tag = slide1.shapes.add_textbox(Inches(0.9), Inches(5.3), Inches(5), Inches(0.3))
    tf_sub = sub_tag.text_frame
    tf_sub.margin_left = tf_sub.margin_top = 0
    p = tf_sub.paragraphs[0]
    p.text = "SUBMITTED BY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT

    # Student 1
    s1_box = slide1.shapes.add_textbox(Inches(0.9), Inches(5.65), Inches(3.2), Inches(0.6))
    tf_s1 = s1_box.text_frame
    tf_s1.margin_left = tf_s1.margin_top = 0
    p = tf_s1.paragraphs[0]
    p.text = "Vikas Bhaskar"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p2 = tf_s1.add_paragraph()
    p2.text = "24BCT0149"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    # Student 2
    s2_box = slide1.shapes.add_textbox(Inches(4.5), Inches(5.65), Inches(3.2), Inches(0.6))
    tf_s2 = s2_box.text_frame
    tf_s2.margin_left = tf_s2.margin_top = 0
    p = tf_s2.paragraphs[0]
    p.text = "Jeevitesh Kandi"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p2 = tf_s2.add_paragraph()
    p2.text = "24BCE0350"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(148, 163, 184)

    # Academic footer
    acad_box = slide1.shapes.add_textbox(Inches(0.9), Inches(6.8), Inches(11.5), Inches(0.35))
    tf_acad = acad_box.text_frame
    tf_acad.margin_left = tf_acad.margin_top = 0
    p = tf_acad.paragraphs[0]
    p.text = "Department of Computer Science & Engineering · Database Management Systems · B.Tech · Fall 2026"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(148, 163, 184)

    # Right side large Emblem
    emblem_path = os.path.join(ASSETS_DIR, "gold_emblem.png")
    if os.path.exists(emblem_path):
        slide1.shapes.add_picture(emblem_path, Inches(9.2), Inches(1.8), width=Inches(3.3))

    # ==========================================
    # SLIDE 2: Roadmap (What We'll Cover)
    # ==========================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2, BG_LIGHT)
    add_header(slide2, "ROADMAP", "What We’ll Cover")
    add_footer(slide2, 2)

    roadmap_items = [
        ("01", "Problem & Domain", "Why raw football tracking & video silos fail"),
        ("02", "Users & Business Rules", "Coaching inquiries, roles & data integrity constraints"),
        ("03", "Entities, Keys & ER Diagram", "6 normalized tables, keys, and relational schema"),
        ("04", "DDL: CREATE · ALTER · DROP", "Building the schema and managing modifications"),
        ("05", "Constraints", "PK, FK, UNIQUE, NOT NULL, CHECK, DEFAULT"),
        ("06", "DML: INSERT · UPDATE · DELETE", "Ingesting, updating, and cleaning match event data"),
        ("07", "Single-Row Functions", "UPPER, SUBSTR, ROUND, CASE tactical expressions"),
        ("08", "Operators & Group Functions", "BETWEEN, IN, LIKE, COUNT, AVG, HAVING, ORDER BY"),
    ]

    col_w = Inches(5.6)
    row_h = Inches(1.1)
    for i, (num, title, desc) in enumerate(roadmap_items):
        col = i // 4
        row = i % 4
        x = Inches(0.8) + col * Inches(6.1)
        y = Inches(1.7) + row * Inches(1.25)

        card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_w, row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1)

        # Number
        nbox = slide2.shapes.add_textbox(x + Inches(0.25), y + Inches(0.18), Inches(0.8), Inches(0.7))
        tf_n = nbox.text_frame
        tf_n.margin_left = tf_n.margin_top = 0
        p = tf_n.paragraphs[0]
        p.text = num
        p.font.name = FONT_HEADING
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = GOLD_ACCENT

        # Text
        tbox = slide2.shapes.add_textbox(x + Inches(1.1), y + Inches(0.18), col_w - Inches(1.2), Inches(0.7))
        tf_t = tbox.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = 0
        p = tf_t.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p2 = tf_t.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10)
        p2.font.color.rgb = TEXT_SUB

    # ==========================================
    # SLIDE 3: Problem & Domain
    # ==========================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3, BG_LIGHT)
    add_header(slide3, "01 · PROBLEM & DOMAIN", "Challenges in Football Tactical Data")
    add_footer(slide3, 3)

    prob_cards = [
        ("Unstructured Video", "Broadcast video captures visual match footage but lacks queryable schema. Coaches cannot execute SQL to filter events, find pressing triggers, or track formations directly."),
        ("Massive Tracking Files", "Raw tracking datasets (1.7M+ frames in FOOTPASS H5) store coordinate streams without relational links to club rosters, official jersey numbers, or match context."),
        ("Siloed Tactical Analysis", "Matches, squad rosters, spatial states, and play-by-play events live in disconnected files, preventing multi-match queries and longitudinal tactical comparisons."),
    ]

    card_w = Inches(3.7)
    card_h = Inches(2.8)
    for i, (title, desc) in enumerate(prob_cards):
        x = Inches(0.8) + i * Inches(4.0)
        y = Inches(1.6)

        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, card_w, card_h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL
        card.line.color.rgb = CARD_BORDER

        # Header icon pill
        pill = slide3.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.3), y + Inches(0.3), Inches(0.65), Inches(0.65))
        pill.fill.solid()
        pill.fill.fore_color.rgb = GOLD_ACCENT
        pill.line.fill.background()

        tbox = slide3.shapes.add_textbox(x + Inches(0.3), y + Inches(1.1), card_w - Inches(0.6), Inches(1.5))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_SUB

    # Bottom Highlight Banner
    ban = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.7), Inches(11.7), Inches(2.0))
    ban.fill.solid()
    ban.fill.fore_color.rgb = BG_DARK
    ban.line.color.rgb = GOLD_ACCENT
    ban.line.width = Pt(1.5)

    # Screenshot inside banner on right
    web_shot = os.path.join(ASSETS_DIR, "webapp_homepage_1792511892834.png")
    if os.path.exists(web_shot):
        slide3.shapes.add_picture(web_shot, Inches(7.8), Inches(4.85), width=Inches(4.5))

    ban_text = slide3.shapes.add_textbox(Inches(1.1), Inches(4.85), Inches(6.5), Inches(1.7))
    tf_b = ban_text.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = 0
    p = tf_b.paragraphs[0]
    p.text = "Our Solution: The Football Tactical Analytics Database"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT

    p2 = tf_b.add_paragraph()
    p2.text = "A unified relational DBMS that links high-frequency tracking feeds to canonical team rosters, European fixtures, and 100K+ play-by-play events. Coaches gain sub-second SQL querying for unit compactness, space creation, and pressing traps directly from broadcast matches."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)

    # ==========================================
    # SLIDE 4: How the System Works
    # ==========================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4, BG_LIGHT)
    add_header(slide4, "01 · HOW IT WORKS", "The Tactical Pipeline in 3 Steps")
    add_footer(slide4, 4)

    steps = [
        ("1. Ingest & Track", "Broadcast video & FOOTPASS tracking data (25 fps, 14 spatiotemporal features) are sampled. Player bounding boxes and field coordinates [X, Y] are captured."),
        ("2. Relational Ingestion", "Parsed data is validated against domain constraints (CHECK, UNIQUE, FK) and normalized into 3NF tables in our relational database."),
        ("3. Query & Discover", "Tactical analysts write SQL queries to filter events, identify team shape compressions, and view live 2D tactical pitch overlays on the dashboard."),
    ]

    for i, (stitle, sdesc) in enumerate(steps):
        x = Inches(0.8) + i * Inches(4.0)
        y = Inches(1.6)

        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.7), Inches(2.9))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL if i < 2 else BG_DARK
        card.line.color.rgb = CARD_BORDER if i < 2 else GOLD_ACCENT
        card.line.width = Pt(1) if i < 2 else Pt(1.5)

        # Step indicator
        pill = slide4.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.3), y + Inches(0.3), Inches(0.65), Inches(0.65))
        pill.fill.solid()
        pill.fill.fore_color.rgb = GOLD_ACCENT if i < 2 else GOLD_BRIGHT
        pill.line.fill.background()

        tbox = slide4.shapes.add_textbox(x + Inches(0.3), y + Inches(1.15), Inches(3.1), Inches(1.5))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.name = FONT_HEADING
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK if i < 2 else TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = sdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_SUB if i < 2 else RGBColor(226, 232, 240)

    # Middle preview: show fastapi docs / backend capture
    doc_shot = os.path.join(ASSETS_DIR, "fastapi_docs_1792511905970.png")
    if os.path.exists(doc_shot):
        slide4.shapes.add_picture(doc_shot, Inches(0.8), Inches(4.7), width=Inches(11.7), height=Inches(1.8))

    # Bottom summary tag
    sum_box = slide4.shapes.add_textbox(Inches(0.8), Inches(6.6), Inches(11.7), Inches(0.35))
    tf_sum = sum_box.text_frame
    tf_sum.margin_left = tf_sum.margin_top = 0
    p = tf_sum.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "Domain: Elite Sports Analytics & Spatiotemporal DBMS  ·  Main actors: Head Coach, Tactical Analyst, Data Engineer  ·  Main data: teams, matches, rosters, tactical events, spatial snapshots"
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.italic = True
    p.font.color.rgb = TEXT_SUB

    # ==========================================
    # SLIDE 5: Requirements and Business Rules
    # ==========================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5, BG_LIGHT)
    add_header(slide5, "02 · REQUIREMENTS, USERS & BUSINESS RULES", "Users, Requirements & Rules")
    add_footer(slide5, 5)

    # Left Column: WHO USES IT & KEY REQUIREMENTS
    left_x = Inches(0.8)
    left_w = Inches(5.6)

    who_box = slide5.shapes.add_textbox(left_x, Inches(1.5), left_w, Inches(0.3))
    p = who_box.text_frame.paragraphs[0]
    p.text = "WHO USES IT"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

    actors = [
        ("Head Coach", "Analyzes opponent unit structure, backline compression, and space creation."),
        ("Tactical Analyst", "Executes ad-hoc SQL queries to evaluate pass completion, set-pieces, and pressing intensity."),
        ("Data Engineer", "Ingests tracking feeds, validates schema integrity, and optimizes query indexes."),
    ]
    for j, (role, rdesc) in enumerate(actors):
        ay = Inches(1.85) + j * Inches(0.85)
        card = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left_x, ay, left_w, Inches(0.75))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL
        card.line.color.rgb = CARD_BORDER

        tb = slide5.shapes.add_textbox(left_x + Inches(0.2), ay + Inches(0.1), left_w - Inches(0.4), Inches(0.55))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = role
        p.font.name = FONT_HEADING
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        p2 = tf.add_paragraph()
        p2.text = rdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_SUB

    req_title = slide5.shapes.add_textbox(left_x, Inches(4.6), left_w, Inches(0.3))
    p = req_title.text_frame.paragraphs[0]
    p.text = "KEY REQUIREMENTS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

    reqs = [
        "• Ingest normalized club rosters & canonical European match fixtures",
        "• Guarantee chronological sequence ordering across match halves",
        "• Support sub-second execution on 100K+ play-by-play tactical events",
        "• Automatically classify tactical macro-states (High Press, Mid Block, Low Block)",
    ]
    req_box = slide5.shapes.add_textbox(left_x, Inches(4.9), left_w, Inches(1.8))
    tf_r = req_box.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = 0
    for idx, rtext in enumerate(reqs):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.text = rtext
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_SUB
        p.space_after = Pt(4)

    # Right Column: BUSINESS RULES & BADGE RULES
    right_x = Inches(6.9)
    right_w = Inches(5.6)

    rule_title = slide5.shapes.add_textbox(right_x, Inches(1.5), right_w, Inches(0.3))
    p = rule_title.text_frame.paragraphs[0]
    p.text = "BUSINESS RULES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

    b_rules = [
        ("Valid shirt numbers", "shirt_number BETWEEN 1 AND 99"),
        ("Distinct competing clubs", "home_team <> away_team"),
        ("Single jersey per team", "UNIQUE (team_code, shirt_number)"),
        ("Valid match halves", "half IN (1, 2)"),
        ("Normalized pitch coordinates", "centroid_x BETWEEN 0.0 AND 1.0"),
    ]
    for k, (bname, bsql) in enumerate(b_rules):
        by = Inches(1.85) + k * Inches(0.6)
        rb = slide5.shapes.add_textbox(right_x, by, right_w, Inches(0.55))
        tf = rb.text_frame
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = bname + "  "
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK
        run = p.add_run()
        run.text = bsql
        run.font.name = FONT_CODE
        run.font.size = Pt(9.5)
        run.font.bold = False
        run.font.color.rgb = GOLD_MUTED

    # Tactical Classification Rules
    badge_title = slide5.shapes.add_textbox(right_x, Inches(4.9), right_w, Inches(0.3))
    p = badge_title.text_frame.paragraphs[0]
    p.text = "TACTICAL BLOCK RULES"
    p.font.name = FONT_HEADING
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

    block_rules = [
        ("High Press Block", "centroid_x >= 0.55\nlength < 35m"),
        ("Midfield Structure", "centroid_x BETWEEN\n0.35 AND 0.55"),
        ("Deep Low Block", "centroid_x < 0.35\nbackline < 20m"),
    ]
    bw = Inches(1.75)
    for m, (b_name, b_desc) in enumerate(block_rules):
        bx = right_x + m * Inches(1.9)
        by = Inches(5.25)
        bcard = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, bw, Inches(1.5))
        bcard.fill.solid()
        bcard.fill.fore_color.rgb = CARD_FILL
        bcard.line.color.rgb = CARD_BORDER

        btb = slide5.shapes.add_textbox(bx + Inches(0.1), by + Inches(0.15), bw - Inches(0.2), Inches(1.2))
        tf = btb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = b_name
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = GOLD_MUTED

        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        p2.text = b_desc
        p2.font.name = FONT_CODE
        p2.font.size = Pt(9)
        p2.font.color.rgb = TEXT_DARK
        p2.space_before = Pt(6)

    # ==========================================
    # SLIDE 6: Entities, Attributes, and Keys
    # ==========================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6, BG_LIGHT)
    add_header(slide6, "03 · ENTITIES, ATTRIBUTES & KEYS", "6 Entities, Explained Simply")
    add_footer(slide6, 6)

    entities = [
        ("teams", "European clubs with code, name, country, venue, and primary kit colors"),
        ("matches", "Scheduled fixtures with competition, season, date, frames, and duration"),
        ("players", "Squad rosters with canonical ID, team code, shirt number, position, and role ID"),
        ("match_events", "Play-by-play actions (Pass, Drive, Cross, Shot, Header, Throw-in, Tackle, Block)"),
        ("tactical_snapshots", "Macro-level spatial metrics (K=8 cluster states, team width, length, centroids)"),
        ("tactical_rules", "Coaching heuristics and threshold criteria for flagging tactical structures"),
    ]

    ew = Inches(3.7)
    eh = Inches(1.7)
    for i, (ename, edesc) in enumerate(entities):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.6) + row * Inches(1.9)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, ew, eh)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL
        card.line.color.rgb = CARD_BORDER

        pill = slide6.shapes.add_shape(MSO_SHAPE.OVAL, x + Inches(0.25), y + Inches(0.25), Inches(0.45), Inches(0.45))
        pill.fill.solid()
        pill.fill.fore_color.rgb = GOLD_ACCENT
        pill.line.fill.background()

        tb = slide6.shapes.add_textbox(x + Inches(0.85), y + Inches(0.25), ew - Inches(1.0), eh - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = ename
        p.font.name = FONT_CODE
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

        p2 = tf.add_paragraph()
        p2.text = edesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_SUB
        p2.space_before = Pt(3)

    # Bottom 4 Key Cards
    keys = [
        ("PK", "Primary Key", "Unique ID for each row — team_code, match_id, player_id"),
        ("FK", "Foreign Key", "Points to parent table — matches.home_team -> teams"),
        ("UQ", "Candidate / Unique", "Prevents duplicate entries — UNIQUE(team_code, shirt_number)"),
        ("CK", "Composite Key", "Combined unique columns — (match_id, half, frame_idx, jersey)"),
    ]
    kw = Inches(2.75)
    kh = Inches(1.4)
    for k, (kcode, ktitle, kdesc) in enumerate(keys):
        x = Inches(0.8) + k * Inches(3.0)
        y = Inches(5.45)

        card = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, kw, kh)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_DARK
        card.line.color.rgb = GOLD_ACCENT
        card.line.width = Pt(1)

        # Pill badge
        pbox = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.18), y + Inches(0.18), Inches(0.55), Inches(0.35))
        pbox.fill.solid()
        pbox.fill.fore_color.rgb = GOLD_ACCENT
        pbox.line.fill.background()
        p = pbox.text_frame.paragraphs[0]
        p.text = kcode
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_CODE
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        tb = slide6.shapes.add_textbox(x + Inches(0.82), y + Inches(0.18), kw - Inches(0.95), kh - Inches(0.3))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = ktitle
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        p2 = tf.add_paragraph()
        p2.text = kdesc
        p2.font.name = FONT_BODY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = RGBColor(203, 213, 225)
        p2.space_before = Pt(3)

    # ==========================================
    # SLIDE 7: ER Diagram
    # ==========================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7, BG_LIGHT)
    add_header(slide7, "03 · ER / EER DIAGRAM", "How the Tables Connect")
    add_footer(slide7, 7)

    er_path = os.path.join(ASSETS_DIR, "er_diagram.png")
    if os.path.exists(er_path):
        slide7.shapes.add_picture(er_path, Inches(0.8), Inches(1.5), width=Inches(11.7))

    # ==========================================
    # SLIDE 8: DDL Implementation: CREATE TABLE
    # ==========================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8, BG_LIGHT)
    add_header(slide8, "04 · DDL IMPLEMENTATION", "CREATE TABLE: Building the Schema")
    add_footer(slide8, 8)

    # Box 1
    box1_x, box1_y, box1_w, box1_h = Inches(0.8), Inches(1.55), Inches(5.7), Inches(4.3)
    c1 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box1_x, box1_y, box1_w, box1_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = CODE_BG
    c1.line.color.rgb = RGBColor(51, 65, 85)

    tb1 = slide8.shapes.add_textbox(box1_x + Inches(0.25), box1_y + Inches(0.2), box1_w - Inches(0.5), box1_h - Inches(0.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = 0
    p = tf1.paragraphs[0]
    p.text = "teams & matches  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

    ddl_1 = """CREATE TABLE teams (
    team_code     VARCHAR2(10) PRIMARY KEY,
    team_name     VARCHAR2(60) NOT NULL UNIQUE,
    country       VARCHAR2(30) NOT NULL,
    home_venue    VARCHAR2(80),
    primary_color VARCHAR2(10) DEFAULT '#FFFFFF'
);

CREATE TABLE matches (
    match_id      VARCHAR2(20) PRIMARY KEY,
    competition   VARCHAR2(50) NOT NULL,
    season        VARCHAR2(10) DEFAULT '2023-2024',
    home_team     VARCHAR2(10) REFERENCES teams(team_code),
    away_team     VARCHAR2(10) REFERENCES teams(team_code),
    total_frames  NUMBER CHECK (total_frames > 0),
    duration_s    NUMBER(7,2) CHECK (duration_s > 0),
    fps           NUMBER(4,1) DEFAULT 25.0,
    CONSTRAINT chk_diff_teams CHECK (home_team <> away_team)
);"""
    p2 = tf1.add_paragraph()
    p2.text = ddl_1
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(4)

    # Box 2
    box2_x, box2_y, box2_w, box2_h = Inches(6.8), Inches(1.55), Inches(5.7), Inches(4.3)
    c2 = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, box2_x, box2_y, box2_w, box2_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = CODE_BG
    c2.line.color.rgb = RGBColor(51, 65, 85)

    tb2 = slide8.shapes.add_textbox(box2_x + Inches(0.25), box2_y + Inches(0.2), box2_w - Inches(0.5), box2_h - Inches(0.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = 0
    p = tf2.paragraphs[0]
    p.text = "players & match_events  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

    ddl_2 = """CREATE TABLE players (
    player_id     NUMBER PRIMARY KEY,
    team_code     VARCHAR2(10) REFERENCES teams(team_code),
    shirt_number  NUMBER CHECK (shirt_number BETWEEN 1 AND 99),
    player_name   VARCHAR2(60) NOT NULL,
    position      VARCHAR2(10) NOT NULL,
    role_id       NUMBER CHECK (role_id BETWEEN 1 AND 13),
    CONSTRAINT uq_team_shirt UNIQUE (team_code, shirt_number)
);

CREATE TABLE match_events (
    event_id      NUMBER PRIMARY KEY,
    match_id      VARCHAR2(20) REFERENCES matches(match_id),
    half          NUMBER CHECK (half IN (1, 2)),
    frame_idx     NUMBER CHECK (frame_idx >= 0),
    event_second  NUMBER(6,2),
    team_code     VARCHAR2(10) REFERENCES teams(team_code),
    jersey_number NUMBER,
    action_type   VARCHAR2(30) NOT NULL
    CHECK (action_type IN ('Pass','Drive','Cross','Shot','Header','Throw-in','Tackle','Block')),
    success_flag  NUMBER DEFAULT 1 CHECK (success_flag IN (0, 1))
);"""
    p2 = tf2.add_paragraph()
    p2.text = ddl_2
    p2.font.name = FONT_CODE
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(4)

    # Middle text
    sub_t = slide8.shapes.add_textbox(Inches(0.8), Inches(5.95), Inches(11.7), Inches(0.3))
    p = sub_t.text_frame.paragraphs[0]
    p.text = "Same relational pattern applied for tactical_snapshots and tactical_rules — 6 tables in total."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_SUB

    # Bottom 3 Badges
    pills = [
        "Every table gets a PRIMARY KEY",
        "Foreign keys link fixtures & rosters",
        "CHECK validates jersey numbers & halves",
    ]
    for p_idx, p_text in enumerate(pills):
        px = Inches(0.8) + p_idx * Inches(4.0)
        py = Inches(6.3)
        p_card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, px, py, Inches(3.7), Inches(0.55))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = CARD_FILL
        p_card.line.color.rgb = CARD_BORDER

        tb = slide8.shapes.add_textbox(px, py + Inches(0.1), Inches(3.7), Inches(0.4))
        p = tb.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = p_text
        p.font.name = FONT_HEADING
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = GOLD_MUTED

    # ==========================================
    # SLIDE 9: ALTER and DROP
    # ==========================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9, BG_LIGHT)
    add_header(slide9, "04 · DDL IMPLEMENTATION", "ALTER & DROP: Changing the Schema")
    add_footer(slide9, 9)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(6.8), Inches(4.5)
    c = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(51, 65, 85)

    tb = slide9.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "ALTER & DROP  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.color.rgb = GOLD_BRIGHT

    alter_sql = """-- ALTER: change an existing table structure
ALTER TABLE players ADD (market_value_eur NUMBER(12,2));

ALTER TABLE players MODIFY (player_name VARCHAR2(80));

ALTER TABLE match_events ADD CONSTRAINT chk_event_sec
CHECK (event_second >= 0);

ALTER TABLE players DROP COLUMN market_value_eur;

-- DROP: remove a table completely (children first!)
DROP TABLE match_events;
DROP TABLE tactical_snapshots;
DROP TABLE matches;"""

    p2 = tf.add_paragraph()
    p2.text = alter_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(8)

    # Right Action Chips
    chips = [
        ("ADD", "Adds a new column (e.g. market valuation or sensor metric)"),
        ("MODIFY", "Changes a column's width, precision, or nullability"),
        ("ADD CONSTRAINT", "Enforces tactical business rules post-table creation"),
        ("DROP COLUMN", "Removes deprecated or legacy tracking attributes"),
        ("DROP TABLE", "Permanently deletes an entire table and all its data"),
    ]
    for ch_idx, (cname, cdesc) in enumerate(chips):
        cy = Inches(1.55) + ch_idx * Inches(0.9)
        # Button badge
        btn = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), cy, Inches(1.5), Inches(0.5))
        btn.fill.solid()
        btn.fill.fore_color.rgb = BG_DARK
        btn.line.color.rgb = GOLD_ACCENT
        btn.line.width = Pt(1)
        p = btn.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = cname
        p.font.name = FONT_CODE
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Description
        dtb = slide9.shapes.add_textbox(Inches(9.7), cy + Inches(0.05), Inches(2.8), Inches(0.7))
        tf_d = dtb.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]
        p.text = cdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_DARK

    # Bottom Tip Box
    tip = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.25), Inches(11.7), Inches(0.65))
    tip.fill.solid()
    tip.fill.fore_color.rgb = RGBColor(254, 243, 199)
    tip.line.color.rgb = RGBColor(245, 158, 11)

    ttb = slide9.shapes.add_textbox(Inches(1.0), Inches(6.35), Inches(11.3), Inches(0.5))
    tf_tip = ttb.text_frame
    tf_tip.margin_left = tf_tip.margin_top = 0
    p = tf_tip.paragraphs[0]
    p.text = "Tip: Always drop child tables (match_events, tactical_snapshots) before parent tables (matches, teams), or foreign key referential integrity will block deletion."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(146, 64, 14)

    # ==========================================
    # SLIDE 10: Database Constraints
    # ==========================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10, BG_LIGHT)
    add_header(slide10, "05 · CONSTRAINTS", "The 6 Constraints We Use")
    add_footer(slide10, 10)

    constraints = [
        ("PK", "PRIMARY KEY", "Unique + not null entity identifier. team_code, match_id, player_id, event_id"),
        ("FK", "FOREIGN KEY", "Enforces relational integrity. matches.home_team -> teams, ON DELETE CASCADE"),
        ("UQ", "UNIQUE", "No duplicates. team_name, and (team_code, shirt_number) = one jersey per club"),
        ("NN", "NOT NULL", "Mandatory attributes. player_name, action_type, competition must have values"),
        ("CHK", "CHECK", "Domain rules. shirt_number 1–99, role_id 1–13, home_team <> away_team"),
        ("DEF", "DEFAULT", "Auto fallback value. season = '2023-2024', fps = 25.0, success_flag = 1"),
    ]

    cw = Inches(3.7)
    ch = Inches(2.3)
    for i, (code, title, desc) in enumerate(constraints):
        col = i % 3
        row = i // 3
        x = Inches(0.8) + col * Inches(4.0)
        y = Inches(1.6) + row * Inches(2.55)

        card = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, cw, ch)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_FILL
        card.line.color.rgb = CARD_BORDER

        # Badge pill
        bpill = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x + Inches(0.25), y + Inches(0.25), Inches(0.7), Inches(0.5))
        bpill.fill.solid()
        bpill.fill.fore_color.rgb = GOLD_ACCENT
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
        tb = slide10.shapes.add_textbox(x + Inches(1.1), y + Inches(0.25), cw - Inches(1.3), Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_DARK

        # Desc
        dtb = slide10.shapes.add_textbox(x + Inches(0.3), y + Inches(1.05), cw - Inches(0.6), Inches(1.1))
        tf_d = dtb.text_frame
        tf_d.word_wrap = True
        tf_d.margin_left = tf_d.margin_top = 0
        p = tf_d.paragraphs[0]
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_SUB

    # ==========================================
    # SLIDE 11: DML Operations
    # ==========================================
    slide11 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide11, BG_LIGHT)
    add_header(slide11, "06 · DML OPERATIONS", "INSERT · UPDATE · DELETE")
    add_footer(slide11, 11)

    dml_sections = [
        ("INSERT", "Add new rows", """INSERT INTO teams VALUES
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

        ("UPDATE", "Change existing rows", """-- Match extra time duration update
UPDATE matches
SET duration_s = 6280.50,
    total_frames = 157012
WHERE match_id = 'game_39';

-- Coach adjusts player tactical role
UPDATE players
SET role_id = 10,
    position = 'LW'
WHERE player_id = 5;

-- Verified tackle success attribution
UPDATE match_events
SET success_flag = 1
WHERE event_id = 101;"""),

        ("DELETE", "Remove rows", """-- Remove corrupted tracking noise
DELETE FROM match_events
WHERE frame_idx < 0
   OR event_second > 7200;

-- Remove cancelled friendly fixture
DELETE FROM matches
WHERE competition = 'Friendly'
  AND season = '2023-2024';

-- Clean obsolete coaching annotations
DELETE FROM tactical_rules
WHERE rule_id = 'RULE_OLD';"""),
    ]

    col_w = Inches(3.7)
    for i, (action, tag, sql_code) in enumerate(dml_sections):
        x = Inches(0.8) + i * Inches(4.0)

        # Header pill
        hpill = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.5), Inches(1.3), Inches(0.4))
        hpill.fill.solid()
        hpill.fill.fore_color.rgb = GOLD_ACCENT
        hpill.line.fill.background()
        p = hpill.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = action
        p.font.name = FONT_CODE
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        sub_t = slide11.shapes.add_textbox(x + Inches(1.4), Inches(1.55), Inches(2.2), Inches(0.35))
        p = sub_t.text_frame.paragraphs[0]
        p.text = tag
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_SUB

        # Code box
        c = slide11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(2.0), col_w, Inches(4.7))
        c.fill.solid()
        c.fill.fore_color.rgb = CODE_BG
        c.line.color.rgb = RGBColor(51, 65, 85)

        tb = slide11.shapes.add_textbox(x + Inches(0.2), Inches(2.15), col_w - Inches(0.4), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = f"{action.lower()}.sql  Oracle SQL"
        p.font.name = FONT_CODE
        p.font.size = Pt(9)
        p.font.color.rgb = GOLD_BRIGHT

        p2 = tf.add_paragraph()
        p2.text = sql_code
        p2.font.name = FONT_CODE
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = RGBColor(241, 245, 249)
        p2.space_before = Pt(6)

    # ==========================================
    # SLIDE 12: Single-Row Functions
    # ==========================================
    slide12 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide12, BG_LIGHT)
    add_header(slide12, "07 · SINGLE-ROW FUNCTIONS", "String Functions")
    add_footer(slide12, 12)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(3.8)
    c = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(51, 65, 85)

    tb = slide12.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Single-row functions  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

    q12_sql = """SELECT player_id,
       UPPER(player_name) AS name_caps,
       LOWER(team_code)   AS team_lower,
       SUBSTR(position, 1, 2) AS pos_code,
       'ROLE-' || LPAD(role_id, 2, '0') AS tier
FROM players
WHERE team_code = 'NEW'
ORDER BY shirt_number;"""

    p2 = tf.add_paragraph()
    p2.text = q12_sql
    p2.font.name = FONT_CODE
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide12.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "OUTPUT  5 rows (Executed against project SQLite DB)"
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

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
            p.font.name = FONT_HEADING if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_DARK
            else:
                p.font.color.rgb = TEXT_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom In simple words callout
    card_sw = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1))
    card_sw.fill.solid()
    card_sw.fill.fore_color.rgb = RGBColor(254, 243, 199)
    card_sw.line.color.rgb = RGBColor(245, 158, 11)

    tb_sw = slide12.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(0.9))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_top = 0
    p = tf_sw.paragraphs[0]
    p.text = "In simple words: single-row functions operate on one record at a time and return one formatted output per row — generating standardized player rosters, position codes, and tactical tiers."
    p.font.name = FONT_BODY
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(146, 64, 14)

    # ==========================================
    # SLIDE 13: Numeric Functions and CASE
    # ==========================================
    slide13 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide13, BG_LIGHT)
    add_header(slide13, "07 · SINGLE-ROW FUNCTIONS", "ROUND & CASE: Tactical Classification")
    add_footer(slide13, 13)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(4.7)
    c = slide13.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(51, 65, 85)

    tb = slide13.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Numeric + CASE  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

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
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide13.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "OUTPUT  7 rows (Executed against match game_39)"
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

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
            p.font.name = FONT_HEADING if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_DARK
            else:
                p.font.color.rgb = TEXT_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom summary tag
    sum_b = slide13.shapes.add_textbox(Inches(0.8), Inches(6.45), Inches(11.7), Inches(0.4))
    p = sum_b.text_frame.paragraphs[0]
    p.text = "In simple words: CASE assigns tactical threat levels dynamically based on action classes, while ROUND converts raw elapsed tracking seconds into match minutes."
    p.font.name = FONT_BODY
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_SUB

    # ==========================================
    # SLIDE 14: SQL Operators
    # ==========================================
    slide14 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide14, BG_LIGHT)
    add_header(slide14, "08 · OPERATORS", "BETWEEN, IN & LIKE")
    add_footer(slide14, 14)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.6), Inches(5.4), Inches(3.8)
    c = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(51, 65, 85)

    tb = slide14.shapes.add_textbox(c_x + Inches(0.25), c_y + Inches(0.2), c_w - Inches(0.5), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Relational operators  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

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
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(8)

    # Right Output Table
    out_lbl = slide14.shapes.add_textbox(Inches(6.6), Inches(1.6), Inches(5.9), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "OUTPUT  4 rows (Executed against canonical rosters)"
    p.font.name = FONT_CODE
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

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
            p.font.name = FONT_HEADING if r_idx == 0 else FONT_CODE
            p.font.size = Pt(9)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_DARK
            else:
                p.font.color.rgb = TEXT_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Bottom In simple words callout
    card_sw = slide14.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.65), Inches(11.7), Inches(1.1))
    card_sw.fill.solid()
    card_sw.fill.fore_color.rgb = RGBColor(254, 243, 199)
    card_sw.line.color.rgb = RGBColor(245, 158, 11)

    tb_sw = slide14.shapes.add_textbox(Inches(1.0), Inches(5.75), Inches(11.3), Inches(0.9))
    tf_sw = tb_sw.text_frame
    tf_sw.word_wrap = True
    tf_sw.margin_left = tf_sw.margin_top = 0
    p = tf_sw.paragraphs[0]
    p.text = "In simple words: BETWEEN filters a numeric range of shirt numbers [7..25], IN restricts results to specific European squads ('NEW', 'PAR', 'BAY'), and LIKE '%a%' finds names containing 'a'. All 3 conditions are combined via AND."
    p.font.name = FONT_BODY
    p.font.size = Pt(10)
    p.font.color.rgb = RGBColor(146, 64, 14)

    # ==========================================
    # SLIDE 15: Group Functions with HAVING
    # ==========================================
    slide15 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide15, BG_LIGHT)
    add_header(slide15, "08 · GROUP FUNCTIONS", "Group Functions with HAVING")
    add_footer(slide15, 15)

    # Left Dark Code Panel
    c_x, c_y, c_w, c_h = Inches(0.8), Inches(1.55), Inches(4.8), Inches(5.0)
    c = slide15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, c_x, c_y, c_w, c_h)
    c.fill.solid()
    c.fill.fore_color.rgb = CODE_BG
    c.line.color.rgb = RGBColor(51, 65, 85)

    tb = slide15.shapes.add_textbox(c_x + Inches(0.2), c_y + Inches(0.2), c_w - Inches(0.4), c_h - Inches(0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = 0
    p = tf.paragraphs[0]
    p.text = "Aggregates  Oracle SQL"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.color.rgb = GOLD_BRIGHT

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
    p2.font.color.rgb = RGBColor(241, 245, 249)
    p2.space_before = Pt(6)

    # Right Output Table
    out_lbl = slide15.shapes.add_textbox(Inches(5.9), Inches(1.55), Inches(6.6), Inches(0.3))
    p = out_lbl.text_frame.paragraphs[0]
    p.text = "OUTPUT  6 rows (Executed across 1,000 match actions)"
    p.font.name = FONT_CODE
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = GOLD_MUTED

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
            p.font.name = FONT_HEADING if r_idx == 0 else FONT_CODE
            p.font.size = Pt(8.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = BG_DARK
            else:
                p.font.color.rgb = TEXT_DARK
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor(248, 250, 252) if r_idx % 2 == 1 else RGBColor(255, 255, 255)

    # Right Chart below table
    chart_path = os.path.join(ASSETS_DIR, "slide15_passes_chart.png")
    if os.path.exists(chart_path):
        slide15.shapes.add_picture(chart_path, Inches(6.1), Inches(4.25), width=Inches(6.2))

    # ==========================================
    # SLIDE 16: Summary and Next Review (Dark)
    # ==========================================
    slide16 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide16, BG_DARK)
    add_header(slide16, "SUMMARY", "What We Built", dark=True)
    add_footer(slide16, 16, dark=True)

    summary_points = [
        "Problem & domain: Structured football tracking vs raw video silos",
        "3 user roles, 5 business rules, and 3 tactical block tiers",
        "6 normalized entities, relational keys, and complete ER diagram",
        "CREATE, ALTER, DROP DDL + all 6 integrity constraints",
        "DML operations: Validated INSERT, UPDATE, and DELETE workflows",
        "Single-row functions, operators, and group aggregates with HAVING",
    ]

    sy_start = Inches(1.6)
    for s_idx, sp in enumerate(summary_points):
        sy = sy_start + s_idx * Inches(0.8)

        # Checkmark badge
        chk = slide16.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.8), sy, Inches(0.55), Inches(0.55))
        chk.fill.solid()
        chk.fill.fore_color.rgb = GOLD_ACCENT
        chk.line.fill.background()
        p = chk.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = "✓"
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE

        # Text
        stb = slide16.shapes.add_textbox(Inches(1.5), sy + Inches(0.08), Inches(5.8), Inches(0.6))
        tf = stb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = 0
        p = tf.paragraphs[0]
        p.text = sp
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(241, 245, 249)

    # Right Card: NEXT · REVIEW 2
    rc_x, rc_y, rc_w, rc_h = Inches(7.7), Inches(1.6), Inches(4.8), Inches(4.9)
    rc = slide16.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, rc_x, rc_y, rc_w, rc_h)
    rc.fill.solid()
    rc.fill.fore_color.rgb = BG_CARD_DARK
    rc.line.color.rgb = GOLD_ACCENT
    rc.line.width = Pt(1.5)

    # Gold Emblem inside Next Box
    if os.path.exists(emblem_path):
        slide16.shapes.add_picture(emblem_path, rc_x + Inches(1.65), rc_y + Inches(0.4), width=Inches(1.5))

    nxt_box = slide16.shapes.add_textbox(rc_x + Inches(0.4), rc_y + Inches(2.1), rc_w - Inches(0.8), Inches(2.5))
    tf_nxt = nxt_box.text_frame
    tf_nxt.word_wrap = True
    tf_nxt.margin_left = tf_nxt.margin_top = 0
    p = tf_nxt.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = "NEXT · REVIEW 2"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = GOLD_BRIGHT

    p2 = tf_nxt.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.text = "Subqueries, multi-table JOINs, tactical views, stored procedures, PL/SQL functions, cursors, and triggers that turn this relational schema into a live tactical intelligence engine."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(12)

    p3 = tf_nxt.add_paragraph()
    p3.alignment = PP_ALIGN.CENTER
    p3.text = "Thank you · Questions?"
    p3.font.name = FONT_HEADING
    p3.font.size = Pt(13)
    p3.font.bold = True
    p3.font.color.rgb = GOLD_ACCENT
    p3.space_before = Pt(20)

    # Save presentation
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    prs.save(PPTX_PATH)
    print(f"Presentation saved successfully to: {PPTX_PATH}")

if __name__ == '__main__':
    create_presentation()
