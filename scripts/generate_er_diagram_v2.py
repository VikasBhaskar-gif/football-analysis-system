"""
generate_er_diagram_v2.py
==========================
Generates a redesigned, clean, technical ER diagram for Slide 7.
Theme: Deep Navy, Cobalt Blue, Pitch Emerald, and Crisp Slate.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_er_diagram(output_path):
    fig, ax = plt.subplots(figsize=(13.333, 7.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color palette - Modern Tech & Football Analytics (Navy / Cobalt / Emerald / Slate)
    c_header_team = '#0F172A'      # Deep Navy Slate
    c_header_match = '#1E3A8A'     # Deep Cobalt Navy
    c_header_player = '#0369A1'    # Sky / Blue
    c_header_event = '#047857'     # Pitch Emerald
    c_header_snap = '#334155'      # Slate
    c_bg = '#FFFFFF'
    c_border = '#CBD5E1'

    def draw_entity(x, y, w, h, title, pk_list, fk_list, attr_list, header_color):
        # Card container
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.2,rounding_size=1.0",
            facecolor=c_bg, edgecolor=c_border, linewidth=1.4, zorder=2
        )
        ax.add_patch(box)

        # Header box
        header_h = 3.8
        header = patches.FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle="round,pad=0.2,rounding_size=0.8",
            facecolor=header_color, edgecolor=header_color, linewidth=1, zorder=3
        )
        ax.add_patch(header)

        # Title text
        ax.text(x + w / 2, y + h - header_h / 2, title,
                ha='center', va='center', color='#FFFFFF',
                fontsize=9.5, fontweight='bold', family='sans-serif', zorder=4)

        # Content text
        curr_y = y + h - header_h - 2.0
        line_spacing = 2.2

        for pk in pk_list:
            ax.text(x + 1.2, curr_y, 'PK', color='#059669', fontsize=7.5, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.5, curr_y, pk, color='#0F172A', fontsize=8, fontweight='bold', family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for fk in fk_list:
            ax.text(x + 1.2, curr_y, 'FK', color='#2563EB', fontsize=7.5, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.5, curr_y, fk, color='#334155', fontsize=8, family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for attr in attr_list:
            ax.text(x + 4.5, curr_y, attr, color='#475569', fontsize=7.5, family='sans-serif', zorder=4)
            curr_y -= line_spacing

    # 1. TEAMS (top-left)
    draw_entity(
        x=4, y=58, w=24, h=34,
        title="TEAMS",
        pk_list=["team_code"],
        fk_list=[],
        attr_list=["team_name (UQ)", "country", "home_venue", "primary_color"],
        header_color=c_header_team
    )

    # 2. MATCHES (top-center)
    draw_entity(
        x=36, y=56, w=28, h=37,
        title="MATCHES",
        pk_list=["match_id"],
        fk_list=["home_team", "away_team"],
        attr_list=["competition", "season", "match_date", "total_frames", "duration_s", "fps"],
        header_color=c_header_match
    )

    # 3. PLAYERS (top-right)
    draw_entity(
        x=71, y=58, w=25, h=34,
        title="PLAYERS",
        pk_list=["player_id"],
        fk_list=["team_code"],
        attr_list=["shirt_number (UQ)", "player_name", "position", "role_id (1..13)"],
        header_color=c_header_player
    )

    # 4. MATCH_EVENTS (bottom-center)
    draw_entity(
        x=36, y=10, w=28, h=38,
        title="MATCH_EVENTS",
        pk_list=["event_id"],
        fk_list=["match_id", "team_code"],
        attr_list=["half (1, 2)", "frame_idx", "event_second", "jersey_number", "action_type", "success_flag"],
        header_color=c_header_event
    )

    # 5. TACTICAL_SNAPSHOTS (bottom-right)
    draw_entity(
        x=71, y=12, w=25, h=36,
        title="TACTICAL_SNAPSHOTS",
        pk_list=["snapshot_id"],
        fk_list=["match_id"],
        attr_list=["half", "frame_idx", "team_width_m", "team_length_m", "centroid_x", "centroid_y", "cluster_state (c0..c7)", "tactical_label"],
        header_color=c_header_snap
    )

    # Connectors
    # 1. TEAMS -> MATCHES (1 to M)
    ax.annotate('', xy=(36, 75), xytext=(28, 75),
                arrowprops=dict(arrowstyle='-', color='#0284C7', lw=2.0), zorder=1)
    ax.text(29, 76.5, '1', color='#0284C7', fontsize=10, fontweight='bold')
    ax.text(34, 76.5, 'M', color='#0284C7', fontsize=10, fontweight='bold')

    # 2. TEAMS -> PLAYERS (1 to M) cleanly over the top of the canvas
    ax.plot([16, 16, 83.5, 83.5], [92, 96, 96, 92], color='#0284C7', lw=2.0, zorder=1)
    ax.text(17.5, 93.5, '1', color='#0284C7', fontsize=10, fontweight='bold')
    ax.text(81.5, 93.5, 'M', color='#0284C7', fontsize=10, fontweight='bold')

    # 3. MATCHES -> MATCH_EVENTS (1 to M)
    ax.annotate('', xy=(50, 48), xytext=(50, 56),
                arrowprops=dict(arrowstyle='-', color='#059669', lw=2.0), zorder=1)
    ax.text(51, 53.5, '1', color='#059669', fontsize=10, fontweight='bold')
    ax.text(51, 49.5, 'M', color='#059669', fontsize=10, fontweight='bold')

    # 4. MATCHES -> TACTICAL_SNAPSHOTS (1 to M)
    ax.plot([64, 67.5, 67.5, 71], [70, 70, 30, 30], color='#059669', lw=2.0, zorder=1)
    ax.text(64.5, 71.5, '1', color='#059669', fontsize=10, fontweight='bold')
    ax.text(69, 31.5, 'M', color='#059669', fontsize=10, fontweight='bold')

    # Relational Cardinality Summary Card (bottom-left)
    card_x, card_y, card_w, card_h = 4, 10, 26, 38
    card = patches.FancyBboxPatch(
        (card_x, card_y), card_w, card_h,
        boxstyle="round,pad=0.2,rounding_size=1.0",
        facecolor='#F8FAFC', edgecolor='#E2E8F0', linewidth=1.2, zorder=2
    )
    ax.add_patch(card)

    ax.text(card_x + 1.8, card_y + card_h - 3.5, "RELATIONAL CARDINALITIES",
            color='#0369A1', fontsize=8.5, fontweight='bold', family='sans-serif')

    explanations = [
        ("1 : N", "A team participates in multiple match fixtures"),
        ("1 : N", "A team registers multiple squad players"),
        ("1 : N", "A match records multiple tactical events"),
        ("1 : N", "A match produces multiple spatial snapshots"),
        ("M : N", "Competing teams associate through fixtures"),
    ]

    ey = card_y + card_h - 8.0
    for card_type, text in explanations:
        ax.text(card_x + 1.8, ey, card_type, color='#0F172A', fontsize=8.5, fontweight='bold', family='monospace')
        ax.text(card_x + 7.5, ey, text, color='#334155', fontsize=8, family='sans-serif')
        ey -= 6.0

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Refined ER diagram saved to: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.abspath('.'), 'dbms_review_1', 'assets', 'er_diagram_v2.png')
    create_er_diagram(out)
