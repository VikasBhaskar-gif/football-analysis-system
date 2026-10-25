"""
generate_er_diagram.py
=======================
Generates a crisp, academic ER diagram for Slide 7 matching FLAVRD's style.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def create_er_diagram(output_path):
    fig, ax = plt.subplots(figsize=(13.333, 7.5), dpi=300)
    fig.patch.set_facecolor('#F8F9FA')
    ax.set_facecolor('#F8F9FA')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Color palette matching FLAVRD
    c_header_team = '#9A3412'      # Burnt Orange / Brick
    c_header_match = '#B45309'     # Amber / Gold
    c_header_player = '#1E3A8A'    # Navy Blue
    c_header_event = '#047857'     # Emerald Green
    c_header_snap = '#475569'      # Slate
    c_bg = '#FFFFFF'
    c_border = '#CBD5E1'

    def draw_entity(x, y, w, h, title, pk_list, fk_list, attr_list, header_color):
        # Card container
        box = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.2,rounding_size=1.2",
            facecolor=c_bg, edgecolor=c_border, linewidth=1.5, zorder=2
        )
        ax.add_patch(box)

        # Header box
        header_h = 3.8
        header = patches.FancyBboxPatch(
            (x, y + h - header_h), w, header_h,
            boxstyle="round,pad=0.2,rounding_size=1.0",
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
            ax.text(x + 1.2, curr_y, 'PK', color='#B45309', fontsize=7.5, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.5, curr_y, pk, color='#0F172A', fontsize=8, fontweight='bold', family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for fk in fk_list:
            ax.text(x + 1.2, curr_y, 'FK', color='#2563EB', fontsize=7.5, fontweight='bold', family='monospace', zorder=4)
            ax.text(x + 4.5, curr_y, fk, color='#334155', fontsize=8, family='sans-serif', zorder=4)
            curr_y -= line_spacing

        for attr in attr_list:
            ax.text(x + 4.5, curr_y, attr, color='#475569', fontsize=7.5, family='sans-serif', zorder=4)
            curr_y -= line_spacing

    # Layout:
    # Top row: TEAMS (left), MATCHES (middle), PLAYERS (right)
    # Bottom row: IN SIMPLE WORDS (left), MATCH_EVENTS (middle), TACTICAL_SNAPSHOTS (right)

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

    # Connectors:
    # 1. TEAMS -> MATCHES (1 to M)
    ax.annotate('', xy=(36, 75), xytext=(28, 75),
                arrowprops=dict(arrowstyle='-', color='#64748B', lw=1.8), zorder=1)
    ax.text(29, 76.2, '1', color='#0F172A', fontsize=9.5, fontweight='bold')
    ax.text(34, 76.2, 'M', color='#0F172A', fontsize=9.5, fontweight='bold')

    # 2. TEAMS -> PLAYERS (1 to M) cleanly over the top of the canvas
    ax.plot([16, 16, 83.5, 83.5], [92, 96, 96, 92], color='#64748B', lw=1.8, zorder=1)
    ax.text(17.5, 93.5, '1', color='#0F172A', fontsize=9.5, fontweight='bold')
    ax.text(81.5, 93.5, 'M', color='#0F172A', fontsize=9.5, fontweight='bold')

    # 3. MATCHES -> MATCH_EVENTS (1 to M)
    ax.annotate('', xy=(50, 48), xytext=(50, 56),
                arrowprops=dict(arrowstyle='-', color='#64748B', lw=1.8), zorder=1)
    ax.text(51, 53.5, '1', color='#0F172A', fontsize=9.5, fontweight='bold')
    ax.text(51, 49.5, 'M', color='#0F172A', fontsize=9.5, fontweight='bold')

    # 4. MATCHES -> TACTICAL_SNAPSHOTS (1 to M)
    ax.plot([64, 67.5, 67.5, 71], [70, 70, 30, 30], color='#64748B', lw=1.8, zorder=1)
    ax.text(64.5, 71.2, '1', color='#0F172A', fontsize=9.5, fontweight='bold')
    ax.text(69, 31.2, 'M', color='#0F172A', fontsize=9.5, fontweight='bold')

    # In Simple Words Card (bottom-left)
    card_x, card_y, card_w, card_h = 4, 10, 26, 38
    card = patches.FancyBboxPatch(
        (card_x, card_y), card_w, card_h,
        boxstyle="round,pad=0.2,rounding_size=1.2",
        facecolor='#F1F5F9', edgecolor='#E2E8F0', linewidth=1.2, zorder=2
    )
    ax.add_patch(card)

    ax.text(card_x + 1.8, card_y + card_h - 3.5, "IN SIMPLE WORDS",
            color='#94A3B8', fontsize=8.5, fontweight='bold', family='sans-serif')

    explanations = [
        ("1 : M", "A team hosts or visits many matches"),
        ("1 : M", "A team has many squad players"),
        ("1 : M", "A match records many tactical events"),
        ("1 : M", "A match records many spatial snapshots"),
        ("M : N", "Teams compete against teams in fixtures"),
    ]

    ey = card_y + card_h - 8.0
    for card_type, text in explanations:
        ax.text(card_x + 1.8, ey, card_type, color='#B45309', fontsize=8.5, fontweight='bold', family='monospace')
        ax.text(card_x + 7.5, ey, text, color='#334155', fontsize=8, family='sans-serif')
        ey -= 6.0

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Refined ER diagram saved to: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.abspath('.'), 'dbms_review_1', 'assets', 'er_diagram.png')
    create_er_diagram(out)
