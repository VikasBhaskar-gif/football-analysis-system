"""
generate_slide15_chart.py
==========================
Generates the horizontal bar chart for Slide 15 matching the FLAVRD aesthetic.
"""

import matplotlib.pyplot as plt
import os

def create_chart(output_path):
    # Teams and their total passes from our SQL execution
    teams = ['Real Sociedad (RSO)', 'Newcastle (NEW)', 'Dortmund (BVB)', 'Bayern (BAY)', 'Man United (MUN)', 'PSG (PAR)']
    passes = [102, 91, 83, 73, 46, 45]
    
    # Reverse for top-down display
    teams = teams[::-1]
    passes = passes[::-1]

    fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    bars = ax.barh(teams, passes, color='#B45309', height=0.55, edgecolor='none')
    
    # Add data labels
    for bar in bars:
        w = bar.get_width()
        ax.text(w + 2, bar.get_y() + bar.get_height()/2, f"{int(w)}",
                va='center', ha='left', color='#0F172A', fontsize=9.5, fontweight='bold', family='sans-serif')

    ax.set_xlim(0, 125)
    ax.set_title("Total Passes Recorded by Club (HAVING COUNT >= 50)", fontsize=10.5, fontweight='bold', color='#334155', pad=12, family='sans-serif')
    
    # Remove borders
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_color('#CBD5E1')
    ax.xaxis.set_visible(False)
    ax.tick_params(axis='y', colors='#334155', labelsize=8.5)

    plt.tight_layout()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Chart saved to: {output_path}")

if __name__ == '__main__':
    out = os.path.join(os.path.abspath('.'), 'dbms_review_1', 'assets', 'slide15_passes_chart.png')
    create_chart(out)
