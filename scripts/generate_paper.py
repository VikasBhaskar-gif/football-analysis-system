import os
import base64
import subprocess
import pypdf

# 1. Helper to base64 encode figures
def get_b64_image(filename):
    path = os.path.abspath(os.path.join('report_assets', filename))
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing asset file: {path}")
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:image/png;base64,{data}"

print("Loading report figure assets from report_assets/ ...")
fig_map = {
    '%%FIG1_B64%%': get_b64_image('fig1_broadcast_overview.png'),
    '%%FIG2_B64%%': get_b64_image('fig2_tactical_pitch_2d.png'),
    '%%FIG3_B64%%': get_b64_image('fig3_dual_stage_side_by_side.png'),
    '%%FIG4_B64%%': get_b64_image('fig4_passing_options_pane.png'),
    '%%FIG5_B64%%': get_b64_image('fig5_shooting_options_pane_valid.png'),
    '%%FIG6_B64%%': get_b64_image('fig6_tactical_spaces_pane.png'),
    '%%FIG7_B64%%': get_b64_image('fig7_ai_coach_briefing.png'),
    '%%FIG8_B64%%': get_b64_image('fig8_ai_coach_multipitch_shotmap.png'),
    '%%FIG9_B64%%': get_b64_image('fig9_shot_decision_audit_table.png'),
}
print(f"Loaded and encoded all {len(fig_map)} figures successfully.")

# 2. Read HTML template
template_path = os.path.abspath('scripts/paper_template.html')
with open(template_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 3. Inject base64 images
for placeholder, b64_str in fig_map.items():
    if placeholder not in html_content:
        print(f"WARNING: Placeholder {placeholder} not found in template!")
    html_content = html_content.replace(placeholder, b64_str)

# 4. Save compiled HTML
output_html = os.path.abspath('football_tactical_predictor_ieee_paper.html')
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)
print(f"HTML paper written to: {output_html} ({os.path.getsize(output_html):,} bytes)")

# 5. Compile to PDF using Headless Chrome
output_pdf = os.path.abspath('football_tactical_predictor_ieee_paper.pdf')
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'

cmd = [
    chrome_path,
    '--headless',
    '--disable-gpu',
    '--no-margins',
    '--no-pdf-header-footer',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={output_pdf}',
    output_html
]

print("Rendering publication-quality PDF via Google Chrome headless engine...")
res = subprocess.run(cmd, capture_output=True, text=True)

if res.returncode == 0 and os.path.exists(output_pdf):
    reader = pypdf.PdfReader(output_pdf)
    num_pages = len(reader.pages)
    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print("=" * 60)
    print("SUCCESS: IEEE RESEARCH PAPER PDF GENERATED!")
    print(f"Path: {output_pdf}")
    print(f"Total Pages: {num_pages}")
    print(f"File Size: {size_mb:.2f} MB ({os.path.getsize(output_pdf):,} bytes)")
    print("=" * 60)
else:
    print(f"ERROR during PDF generation. Return code: {res.returncode}")
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
