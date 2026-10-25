"""
run_ball_tracking_clip.py
=========================
Command-line driver to execute ball detection and tracking on a selected clip
from existing match broadcast footage.

Outputs:
  - outputs/ball_tracking/data/<match_id>_ball_tracking_clip.csv
  - outputs/ball_tracking/data/<match_id>_ball_tracking_clip.json
"""

import os
import sys
import time
import argparse
import torch

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.tracking.ball_tracker import run_ball_tracking_on_clip


def main():
    parser = argparse.ArgumentParser(description="Run ball tracking on a match video clip.")
    parser.add_argument("--video", type=str, default="football-ai/FOOTPASS/videos/game_39.mp4",
                        help="Path to match video (Full HD 1080p).")
    parser.add_argument("--match-id", type=str, default="game_39_H1",
                        help="Match identifier corresponding to H5 data.")
    parser.add_argument("--start-frame", type=int, default=1875,
                        help="Starting frame index (e.g. 1875 = 75.0s).")
    parser.add_argument("--num-frames", type=int, default=375,
                        help="Number of frames to process (375 = 15.0s at 25fps).")
    parser.add_argument("--model", type=str, default="models/ball_tracking/yolo_football_ball_detector.pt",
                        help="Path to pretrained YOLO ball detection weights.")
    parser.add_argument("--imgsz", type=int, default=1280,
                        help="Inference image resolution.")
    parser.add_argument("--out-dir", type=str, default="outputs/ball_tracking/data",
                        help="Directory to save output CSV and JSON.")
    args = parser.parse_args()

    video_path = os.path.join(PROJECT_ROOT, args.video) if not os.path.isabs(args.video) else args.video
    model_path = os.path.join(PROJECT_ROOT, args.model) if not os.path.isabs(args.model) else args.model
    out_dir = os.path.join(PROJECT_ROOT, args.out_dir) if not os.path.isabs(args.out_dir) else args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    csv_path = os.path.join(out_dir, f"{args.match_id}_ball_tracking_clip.csv")
    json_path = os.path.join(out_dir, f"{args.match_id}_ball_tracking_clip.json")

    print(f"=== BALL TRACKING RUNNER ===")
    print(f"Video:        {video_path}")
    print(f"Match ID:     {args.match_id}")
    print(f"Frame Range:  {args.start_frame} to {args.start_frame + args.num_frames - 1} ({args.num_frames} frames)")
    print(f"Model:        {model_path}")
    print(f"Resolution:   {args.imgsz}")
    print(f"CUDA:         {torch.cuda.is_available()} ({torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A'})")
    print(f"Outputs:      {csv_path}")
    print("=" * 30)

    t0 = time.time()
    records = run_ball_tracking_on_clip(
        video_path=video_path,
        match_id=args.match_id,
        start_frame=args.start_frame,
        num_frames=args.num_frames,
        model_path=model_path,
        imgsz=args.imgsz,
        output_csv_path=csv_path,
        output_json_path=json_path,
    )
    total_time = time.time() - t0
    avg_fps = len(records) / max(0.001, total_time)

    n_det = sum(1 for r in records if r.status == "detected")
    n_unc = sum(1 for r in records if r.status == "uncertain")
    n_mis = sum(1 for r in records if r.status == "missing")
    conf_vals = [r.confidence for r in records if r.status in ("detected", "uncertain")]

    print("\n=== EXECUTION SUMMARY ===")
    print(f"Total Frames Processed: {len(records)}")
    print(f"Total Wall Time:        {total_time:.2f} s")
    print(f"Average Throughput:     {avg_fps:.2f} FPS ({1000.0 / avg_fps:.1f} ms/frame)")
    if torch.cuda.is_available():
        vram_alloc = torch.cuda.memory_allocated() / (1024**2)
        vram_res = torch.cuda.memory_reserved() / (1024**2)
        print(f"GPU VRAM Usage:         Allocated={vram_alloc:.1f} MB, Reserved={vram_res:.1f} MB")
    print(f"Detected Frames:        {n_det} ({n_det / len(records) * 100:.1f}%)")
    print(f"Uncertain Frames:       {n_unc} ({n_unc / len(records) * 100:.1f}%)")
    print(f"Missing Frames:         {n_mis} ({n_mis / len(records) * 100:.1f}%)")
    if conf_vals:
        print(f"Mean Confidence (Vis):  {sum(conf_vals) / len(conf_vals) * 100:.1f}%")
        print(f"Max Confidence:         {max(conf_vals) * 100:.1f}%")
    print(f"Saved: {csv_path}")
    print(f"Saved: {json_path}")
    print("=========================\n")


if __name__ == "__main__":
    main()
