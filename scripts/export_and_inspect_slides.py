"""
export_and_inspect_slides.py
============================
Uses PowerPoint COM automation to:
1. Export Football_Tactical_Analytics_DBMS_Review_1.pptx -> PDF
2. Export all 16 slides as high-res PNG images for visual inspection
"""

import os
import sys
import win32com.client

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "dbms_review_1")
PPTX_PATH = os.path.join(OUTPUT_DIR, "Football_Tactical_Analytics_DBMS_Review_1.pptx")
PDF_PATH = os.path.join(OUTPUT_DIR, "Football_Tactical_Analytics_DBMS_Review_1.pdf")
SLIDES_IMG_DIR = os.path.join(OUTPUT_DIR, "slide_previews")

def export():
    os.makedirs(SLIDES_IMG_DIR, exist_ok=True)

    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    # Open presentation in read-only / hidden mode
    presentation = powerpoint.Presentations.Open(PPTX_PATH, WithWindow=False)

    try:
        # 1. Export as PDF (Format type 32 is ppSaveAsPDF)
        print("Exporting PDF...")
        presentation.SaveAs(PDF_PATH, 32)
        print(f"PDF exported successfully to: {PDF_PATH}")

        # 2. Export each slide as PNG
        print("Exporting slide images for inspection...")
        for i, slide in enumerate(presentation.Slides):
            slide_img_path = os.path.join(SLIDES_IMG_DIR, f"slide_{i+1:02d}.png")
            # 1920x1080 resolution
            slide.Export(slide_img_path, "PNG", 1920, 1080)
            print(f"  Slide {i+1} exported: {slide_img_path}")

    finally:
        presentation.Close()
        powerpoint.Quit()

if __name__ == '__main__':
    export()
