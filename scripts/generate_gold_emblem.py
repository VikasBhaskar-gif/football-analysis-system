"""
generate_gold_emblem.py
========================
Generates a stylish gold tactical ball & pitch icon matching FLAVRD's top right gold emblem.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os

def create_gold_emblem(output_path):
    fig, ax = plt.subplots(figsize=(2, 2), dpi=300)
    fig.patch.set_facecolor('none')
    ax.set_facecolor('none')
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.axis('off')

    # Golden badge shield or circle
    gold_main = '#D4AF37'
    gold_dark = '#996515'
    gold_light = '#F3E5AB'

    # Outer hex / shield
    angles = np.linspace(0, 2*np.pi, 7)[:-1] + np.pi/6
    x = 1.05 * np.cos(angles)
    y = 1.05 * np.sin(angles)
    poly = patches.Polygon(np.column_stack([x, y]), closed=True, facecolor='#2A2518', edgecolor=gold_main, linewidth=3)
    ax.add_patch(poly)

    # Inner pitch markings / soccer hexagon
    inner_poly = patches.Polygon(np.column_stack([0.88 * x, 0.88 * y]), closed=True, facecolor='none', edgecolor=gold_dark, linewidth=1.5)
    ax.add_patch(inner_poly)

    # Ball / pitch lines
    circle = plt.Circle((0, 0), 0.55, facecolor='none', edgecolor=gold_main, linewidth=2)
    ax.add_patch(circle)

    # Pitch centerline and box
    ax.plot([-0.55, 0.55], [0, 0], color=gold_light, lw=1.8)
    rect = patches.Rectangle((-0.35, -0.2), 0.7, 0.4, facecolor='none', edgecolor=gold_main, lw=1.4)
    ax.add_patch(rect)
    ax.plot([0, 0], [-0.55, 0.55], color=gold_light, lw=1.2, linestyle=':')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.05)
    plt.close()
    print(f"Emblem saved to: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.abspath('.'), 'dbms_review_1', 'assets', 'gold_emblem.png')
    create_gold_emblem(out)
