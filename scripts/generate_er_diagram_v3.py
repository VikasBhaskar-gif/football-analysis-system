"""
scripts/generate_er_diagram_v3.py
=================================
Generates the comprehensive 6-entity Relational ER Diagram for Slide 7.
Entities:
  1. TEAMS (Clubs & venues)
  2. MATCHES (Fixtures & durations)
  3. PLAYERS (Squad rosters & tactical roles)
  4. TACTICAL_RULES (Domain heuristics & threshold alerts)
  5. MATCH_EVENTS (Play-by-play telemetry & actions)
  6. TACTICAL_SNAPSHOTS (Spatiotemporal tracking clusters & compactness)

Aesthetic:
- Crisp white canvas with high contrast.
- Navy headers for parent entities, emerald for core telemetry, cobalt for squads & rules.
- Clear orthogonal connectors with explicit 1 and M cardinality labels.
- Legible typography designed specifically for classroom projection.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_er_diagram(output_path):
    fig, ax = plt.subplots(figsize=(14.0, 7.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color Palette
    c_header_team = '#0F172A'      # Deep Charcoal Slate
    c_header_match = '#1E3A8A'     # Deep Cobalt Navy
    c_header_player = '#0369A1'    # Sky Navy
    c_header_rules = '#0F766E'     # Deep Teal
    c_header_event = '#047857'     # Pitch Emerald
    c_header_snap = '#334155'      # Slate
    c_bg = '#FFFFFF'
    c_border = '#CBD5E1'

    def draw_entity(x, y, w, h, title, pk_list, fk_list, attr_list, header_color):
        # Card container box
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.2,rounding_size=1.0",
            facecolor=c_bg, edgecolor=c_border, linewidth=1.5, zorder=2
        )
        ax.add_patch(box)

        # Header banner
        header_h = 4.0
        header = patches.FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=header_color, edgecolor=header_color, linewidth=1, zorder=3
        )
        ax.add_patch(header)

        # Entity Title
        ax.text(x + w / 2, y + h - header_h / 2, title,
                ha='center', va='center', color='#FFFFFF',
                fontsize=10.5, fontweight='bold', family='sans-serif', zorder=4)

        # Content attributes
        curr_y = y + h - header_h - 2.2
        line_spacing = 2.4

        for pk in pk_list:
            ax.text(x + 1.2, curr_y, 'PK', color='#059669', fontsize=8, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.8, curr_y, pk, color='#0F172A', fontsize=8.5, fontweight='bold', family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for fk in fk_list:
            ax.text(x + 1.2, curr_y, 'FK', color='#2563EB', fontsize=8, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.8, curr_y, fk, color='#1E293B', fontsize=8.5, family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for attr in attr_list:
            ax.text(x + 4.8, curr_y, attr, color='#475569', fontsize=8, family='sans-serif', zorder=4)
            curr_y -= line_spacing

    # ==========================================
    # 1. TOP ROW ENTITIES
    # ==========================================

    # 1. TEAMS (top-left)
    draw_entity(
        x=4, y=56, w=25, h=28,
        title="TEAMS",
        pk_list=["team_code"],
        fk_list=[],
        attr_list=[
            "team_name  (UQ)",
            "country",
            "home_venue",
            "primary_color  [#FFF]"
        ],
        header_color=c_header_team
    )

    # 2. MATCHES (top-center)
    draw_entity(
        x=37.5, y=52, w=27, h=33,
        title="MATCHES",
        pk_list=["match_id"],
        fk_list=["home_team", "away_team"],
        attr_list=[
            "competition",
            "season  [2023-2024]",
            "match_date",
            "total_frames  (>0)",
            "duration_s  (>0)",
            "fps  [25.0]",
            "CHK: home <> away"
        ],
        header_color=c_header_match
    )

    # 3. PLAYERS (top-right)
    draw_entity(
        x=71, y=56, w=25, h=28,
        title="PLAYERS",
        pk_list=["player_id"],
        fk_list=["team_code"],
        attr_list=[
            "shirt_number  (1..99)",
            "player_name",
            "position  (GK..FW)",
            "role_id  (1..13)",
            "UQ: (team, shirt)"
        ],
        header_color=c_header_player
    )

    # ==========================================
    # 2. BOTTOM ROW ENTITIES
    # ==========================================

    # 4. TACTICAL_RULES (bottom-left)
    draw_entity(
        x=4, y=12, w=25, h=28,
        title="TACTICAL_RULES",
        pk_list=["rule_id"],
        fk_list=[],
        attr_list=[
            "rule_name  (UQ)",
            "target_unit",
            "min_compactness",
            "trigger_action",
            "severity_level (LOW/MED/HIGH)"
        ],
        header_color=c_header_rules
    )

    # 5. MATCH_EVENTS (bottom-center)
    draw_entity(
        x=37.5, y=10, w=27, h=33,
        title="MATCH_EVENTS",
        pk_list=["event_id  (AUTO)"],
        fk_list=["match_id", "team_code"],
        attr_list=[
            "half  (1, 2)",
            "frame_idx  (>= 0)",
            "event_second",
            "jersey_number",
            "action_type  (8 types)",
            "success_flag  (0, 1)"
        ],
        header_color=c_header_event
    )

    # 6. TACTICAL_SNAPSHOTS (bottom-right)
    draw_entity(
        x=71, y=10, w=25, h=33,
        title="TACTICAL_SNAPSHOTS",
        pk_list=["snapshot_id  (AUTO)"],
        fk_list=["match_id"],
        attr_list=[
            "half  (1, 2)",
            "frame_idx",
            "team_width_m  (>= 0)",
            "team_length_m  (>= 0)",
            "centroid_x  (0.0..1.0)",
            "centroid_y  (0.0..1.0)",
            "cluster_state  (c0..c7)",
            "tactical_label"
        ],
        header_color=c_header_snap
    )

    # ==========================================
    # 3. RELATIONSHIP CONNECTORS & CARDINALITIES
    # ==========================================

    # 1. TEAMS -> MATCHES (1 to M)
    ax.annotate('', xy=(37.5, 70), xytext=(29, 70),
                arrowprops=dict(arrowstyle='-', color='#0284C7', lw=2.2), zorder=1)
    ax.text(30.0, 71.5, '1', color='#0284C7', fontsize=11, fontweight='bold')
    ax.text(35.5, 71.5, 'M', color='#0284C7', fontsize=11, fontweight='bold')

    # 2. TEAMS -> PLAYERS (1 to M) arched over the top
    ax.plot([16.5, 16.5, 83.5, 83.5], [84, 91.5, 91.5, 84], color='#0284C7', lw=2.2, zorder=1)
    ax.text(18.0, 89.0, '1', color='#0284C7', fontsize=11, fontweight='bold')
    ax.text(81.0, 89.0, 'M', color='#0284C7', fontsize=11, fontweight='bold')

    # 3. MATCHES -> MATCH_EVENTS (1 to M)
    ax.annotate('', xy=(51, 43), xytext=(51, 52),
                arrowprops=dict(arrowstyle='-', color='#059669', lw=2.2), zorder=1)
    ax.text(52.2, 49.0, '1', color='#059669', fontsize=11, fontweight='bold')
    ax.text(52.2, 44.5, 'M', color='#059669', fontsize=11, fontweight='bold')

    # 4. MATCHES -> TACTICAL_SNAPSHOTS (1 to M)
    ax.plot([64.5, 67.5, 67.5, 71], [65, 65, 30, 30], color='#059669', lw=2.2, zorder=1)
    ax.text(65.2, 66.5, '1', color='#059669', fontsize=11, fontweight='bold')
    ax.text(69.0, 31.5, 'M', color='#059669', fontsize=11, fontweight='bold')

    # 5. TEAMS -> MATCH_EVENTS (1 to M via team_code) - clean route between top-left and center
    ax.plot([29.0, 33.5, 33.5, 37.5], [60, 60, 36, 36], color='#2563EB', lw=2.0, linestyle='--', zorder=1)
    ax.text(29.8, 61.2, '1', color='#2563EB', fontsize=10, fontweight='bold')
    ax.text(35.5, 37.2, 'M', color='#2563EB', fontsize=10, fontweight='bold')

    # 6. TACTICAL_RULES -> MATCH_EVENTS (1 to M via trigger_action)
    ax.plot([29.0, 37.5], [26, 26], color='#0F766E', lw=2.0, linestyle=':', zorder=1)
    ax.text(29.8, 27.2, '1', color='#0F766E', fontsize=10, fontweight='bold')
    ax.text(35.5, 27.2, 'M', color='#0F766E', fontsize=10, fontweight='bold')

    # Top Legend Banner
    leg_box = patches.FancyBboxPatch(
        (26, 94.0), 48, 3.5,
        boxstyle="round,pad=0.1,rounding_size=0.6",
        facecolor='#F1F5F9', edgecolor='#CBD5E1', linewidth=1, zorder=2
    )
    ax.add_patch(leg_box)
    ax.text(50, 95.7,
            "PK: Primary Key   |   FK: Foreign Key   |   UQ: Unique   |   CHK: Check Constraint   |   1:M Cardinality",
            ha='center', va='center', color='#334155', fontsize=8.5, fontweight='bold', family='sans-serif', zorder=3)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"6-Entity ER diagram saved to: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.abspath('.'), 'dbms_review_1', 'assets', 'er_diagram_v3.png')
    create_er_diagram(out)
