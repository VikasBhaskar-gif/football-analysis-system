"""
ball_tracker.py
===============
Reusable, lightweight ball detection and tracking module for broadcast football footage.

Key features:
  1. Pretrained lightweight detector (YOLO11n/YOLOv8 fine-tuned on soccer ball detection)
     running efficiently on NVIDIA MX450 (2GB VRAM) or CPU.
  2. Frame resolution scaling (e.g. 1280px) with coordinates mapped back to
     Full-HD broadcast resolution (1920x1080).
  3. Dynamic physical motion gating (velocity-dependent search window, max velocity cap)
     to reject false positives (white boots, socks, ad boards, referee markings).
  4. Explicit three-tier detection status:
       - 'detected': Confirmed ball candidate with high confidence & plausible motion.
       - 'uncertain': Ambiguous or low-confidence candidate (0.15 <= conf < 0.35).
       - 'missing': Ball occluded, out of frame, or undetectable. Coordinates are None/NaN;
                    NEVER fabricated.
  5. Machine-readable exports (CSV, JSON) preserving exact temporal alignment with match frames.
  6. Integration helpers connecting ball tracking with FOOTPASS player tracking data.
"""

import os
import sys
import math
import json
import csv
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple, Dict, Any

import cv2
import numpy as np
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    torch = None
    TORCH_AVAILABLE = False

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


@dataclass
class BallDetection:
    """Raw bounding box candidate from detector."""
    x: float          # Center X in original video coordinates
    y: float          # Center Y in original video coordinates
    w: float          # Bounding box width
    h: float          # Bounding box height
    conf: float       # Detection confidence score [0..1]
    bbox_xyxy: Tuple[float, float, float, float]  # (x1, y1, x2, y2)


@dataclass
class BallTrackRecord:
    """Structured tracking record for a single video frame."""
    match_id: str
    frame: int
    timestamp_s: float
    ball_x: Optional[float]
    ball_y: Optional[float]
    ball_w: Optional[float]
    ball_h: Optional[float]
    confidence: float
    status: str             # 'detected', 'uncertain', 'missing'
    velocity_x: Optional[float]
    velocity_y: Optional[float]
    speed_px_frame: Optional[float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FootballBallDetector:
    """
    Wraps lightweight pretrained YOLO ball detector.
    Handles device placement (CUDA / CPU), resolution scaling, and candidate filtering.
    """

    def __init__(
        self,
        model_path: str = "models/ball_tracking/yolo_football_ball_detector.pt",
        device: Optional[str] = None,
        imgsz: int = 1280,
        min_conf: float = 0.12,
    ):
        if not ULTRALYTICS_AVAILABLE:
            raise ImportError("ultralytics package is required. Install via pip install ultralytics.")

        if not os.path.isfile(model_path):
            raise FileNotFoundError(f"Model file not found at: {model_path}")

        if device is None:
            self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        self.model_path = model_path
        self.imgsz = imgsz
        self.min_conf = min_conf

        print(f"[FootballBallDetector] Loading model '{os.path.basename(model_path)}' on {self.device}...")
        self.model = YOLO(model_path)
        self.model.to(self.device)
        print(f"[FootballBallDetector] Model loaded successfully. Default imgsz={imgsz}, min_conf={min_conf}")

    def detect_frame(self, frame_bgr: np.ndarray) -> List[BallDetection]:
        """
        Run inference on a single BGR frame.
        Returns a list of candidate BallDetection objects in original frame coordinates.
        """
        results = self.model(
            frame_bgr,
            imgsz=self.imgsz,
            conf=self.min_conf,
            verbose=False,
            device=self.device,
        )

        candidates: List[BallDetection] = []
        if not results or len(results) == 0:
            return candidates

        res = results[0]
        if res.boxes is None or len(res.boxes) == 0:
            return candidates

        for box in res.boxes:
            conf = float(box.conf[0].item())
            xyxy = box.xyxy[0].tolist()
            x1, y1, x2, y2 = xyxy
            w = x2 - x1
            h = y2 - y1
            cx = x1 + w / 2.0
            cy = y1 + h / 2.0

            # Basic spatial sanity filter for broadcast 1920x1080 soccer:
            # A soccer ball in broadcast camera cannot be > 80px or < 3px.
            if w > 80 or h > 80 or w < 3 or h < 3:
                continue

            candidates.append(
                BallDetection(
                    x=float(cx),
                    y=float(cy),
                    w=float(w),
                    h=float(h),
                    conf=float(conf),
                    bbox_xyxy=(float(x1), float(y1), float(x2), float(y2)),
                )
            )

        # Sort candidates descending by confidence
        candidates.sort(key=lambda c: c.conf, reverse=True)
        return candidates


class FootballBallTracker:
    """
    Temporal ball tracker enforcing physical motion constraints and explicit certainty tagging.
    """

    def __init__(
        self,
        high_conf_thresh: float = 0.35,
        low_conf_thresh: float = 0.15,
        max_speed_px_frame: float = 120.0,    # Max plausible displacement per frame (~130 km/h)
        base_search_radius: float = 55.0,     # Base search radius in pixels
        velocity_radius_factor: float = 2.2,  # Search radius expansion factor based on speed
        max_lost_frames: int = 5,             # Frames before track reset
        history_window: int = 16,
    ):
        self.high_conf_thresh = high_conf_thresh
        self.low_conf_thresh = low_conf_thresh
        self.max_speed = max_speed_px_frame
        self.base_search_radius = base_search_radius
        self.velocity_radius_factor = velocity_radius_factor
        self.max_lost_frames = max_lost_frames
        self.history_window = history_window

        # Tracker state
        self.current_pos: Optional[Tuple[float, float]] = None
        self.current_vel: Tuple[float, float] = (0.0, 0.0)
        self.current_bbox: Optional[Tuple[float, float]] = None  # (w, h)
        self.lost_count: int = 999
        self.recent_positions: List[Tuple[float, float]] = []

    def reset(self):
        """Reset tracking state."""
        self.current_pos = None
        self.current_vel = (0.0, 0.0)
        self.current_bbox = None
        self.lost_count = 999
        self.recent_positions.clear()

    def update(
        self,
        candidates: List[BallDetection],
        match_id: str,
        frame_idx: int,
        fps: float = 25.0,
    ) -> BallTrackRecord:
        """
        Associate detections, update motion state, and return a BallTrackRecord.
        """
        timestamp_s = round(frame_idx / fps, 4)

        # Case 1: Active track exists and is not lost
        if self.current_pos is not None and self.lost_count < self.max_lost_frames:
            pred_x = self.current_pos[0] + self.current_vel[0]
            pred_y = self.current_pos[1] + self.current_vel[1]
            speed = math.hypot(self.current_vel[0], self.current_vel[1])
            search_radius = min(
                self.max_speed,
                max(self.base_search_radius, self.base_search_radius + self.velocity_radius_factor * speed)
            )

            # Find matching candidate within search gate
            best_cand: Optional[BallDetection] = None
            best_score = -float("inf")

            for cand in candidates:
                dist = math.hypot(cand.x - pred_x, cand.y - pred_y)
                if dist > search_radius:
                    continue

                # Scoring function: balance confidence with proximity to predicted motion
                # Score = conf * 1.5 - (dist / search_radius)
                score = cand.conf * 1.5 - (dist / max(1.0, search_radius))
                if score > best_score:
                    best_score = score
                    best_cand = cand

            if best_cand is not None:
                # Associate candidate
                new_vx = best_cand.x - self.current_pos[0]
                new_vy = best_cand.y - self.current_pos[1]
                # Smooth velocity
                self.current_vel = (
                    0.65 * new_vx + 0.35 * self.current_vel[0],
                    0.65 * new_vy + 0.35 * self.current_vel[1],
                )
                self.current_pos = (best_cand.x, best_cand.y)
                self.current_bbox = (best_cand.w, best_cand.h)
                self.lost_count = 0
                self.recent_positions.append(self.current_pos)
                if len(self.recent_positions) > self.history_window:
                    self.recent_positions.pop(0)

                status = "detected" if best_cand.conf >= self.high_conf_thresh else "uncertain"
                speed_px = math.hypot(self.current_vel[0], self.current_vel[1])

                return BallTrackRecord(
                    match_id=match_id,
                    frame=frame_idx,
                    timestamp_s=timestamp_s,
                    ball_x=round(best_cand.x, 2),
                    ball_y=round(best_cand.y, 2),
                    ball_w=round(best_cand.w, 2),
                    ball_h=round(best_cand.h, 2),
                    confidence=round(best_cand.conf, 4),
                    status=status,
                    velocity_x=round(self.current_vel[0], 2),
                    velocity_y=round(self.current_vel[1], 2),
                    speed_px_frame=round(speed_px, 2),
                )
            else:
                # No candidate matched within motion gate -> missing
                self.lost_count += 1
                # Velocity decays
                self.current_vel = (self.current_vel[0] * 0.7, self.current_vel[1] * 0.7)

                # Do NOT invent coordinates. Explicitly return None.
                return BallTrackRecord(
                    match_id=match_id,
                    frame=frame_idx,
                    timestamp_s=timestamp_s,
                    ball_x=None,
                    ball_y=None,
                    ball_w=None,
                    ball_h=None,
                    confidence=0.0,
                    status="missing",
                    velocity_x=None,
                    velocity_y=None,
                    speed_px_frame=None,
                )

        # Case 2: No active track or track lost -> try to initialize / reacquire
        if candidates:
            # Look for strong candidate
            top_cand = candidates[0]
            if top_cand.conf >= self.high_conf_thresh:
                self.current_pos = (top_cand.x, top_cand.y)
                self.current_bbox = (top_cand.w, top_cand.h)
                self.current_vel = (0.0, 0.0)
                self.lost_count = 0
                self.recent_positions.append(self.current_pos)

                return BallTrackRecord(
                    match_id=match_id,
                    frame=frame_idx,
                    timestamp_s=timestamp_s,
                    ball_x=round(top_cand.x, 2),
                    ball_y=round(top_cand.y, 2),
                    ball_w=round(top_cand.w, 2),
                    ball_h=round(top_cand.h, 2),
                    confidence=round(top_cand.conf, 4),
                    status="detected",
                    velocity_x=0.0,
                    velocity_y=0.0,
                    speed_px_frame=0.0,
                )
            elif top_cand.conf >= self.low_conf_thresh:
                # Candidate exists but low confidence -> tag as uncertain without committing full track
                return BallTrackRecord(
                    match_id=match_id,
                    frame=frame_idx,
                    timestamp_s=timestamp_s,
                    ball_x=round(top_cand.x, 2),
                    ball_y=round(top_cand.y, 2),
                    ball_w=round(top_cand.w, 2),
                    ball_h=round(top_cand.h, 2),
                    confidence=round(top_cand.conf, 4),
                    status="uncertain",
                    velocity_x=None,
                    velocity_y=None,
                    speed_px_frame=None,
                )

        # Case 3: Completely missing
        self.lost_count += 1
        return BallTrackRecord(
            match_id=match_id,
            frame=frame_idx,
            timestamp_s=timestamp_s,
            ball_x=None,
            ball_y=None,
            ball_w=None,
            ball_h=None,
            confidence=0.0,
            status="missing",
            velocity_x=None,
            velocity_y=None,
            speed_px_frame=None,
        )


def run_ball_tracking_on_clip(
    video_path: str,
    match_id: str,
    start_frame: int,
    num_frames: int,
    model_path: str = "models/ball_tracking/yolo_football_ball_detector.pt",
    device: Optional[str] = None,
    imgsz: int = 1280,
    output_csv_path: Optional[str] = None,
    output_json_path: Optional[str] = None,
) -> List[BallTrackRecord]:
    """
    Run the complete ball detection and tracking pipeline on a video clip.
    Returns list of BallTrackRecord objects and optionally saves to CSV/JSON.
    """
    detector = FootballBallDetector(model_path=model_path, device=device, imgsz=imgsz)
    tracker = FootballBallTracker()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError(f"Failed to open video file: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    records: List[BallTrackRecord] = []
    end_frame = start_frame + num_frames

    print(f"[run_ball_tracking_on_clip] Processing {num_frames} frames ({start_frame}..{end_frame-1}) from {video_path}...")

    for f_idx in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            print(f"[run_ball_tracking_on_clip] Video ended early at frame {f_idx}")
            break

        candidates = detector.detect_frame(frame)
        rec = tracker.update(candidates, match_id=match_id, frame_idx=f_idx, fps=fps)
        records.append(rec)

        if (f_idx - start_frame + 1) % 50 == 0 or (f_idx - start_frame + 1) == num_frames:
            n_done = f_idx - start_frame + 1
            n_det = sum(1 for r in records if r.status == "detected")
            n_unc = sum(1 for r in records if r.status == "uncertain")
            n_mis = sum(1 for r in records if r.status == "missing")
            pct_vis = (n_det + n_unc) / n_done * 100.0
            print(
                f"  Frame {f_idx} ({n_done}/{num_frames}) -> "
                f"detected: {n_det}, uncertain: {n_unc}, missing: {n_mis} ({pct_vis:.1f}% visible)"
            )

    cap.release()

    # Save to CSV if requested
    if output_csv_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_csv_path)), exist_ok=True)
        fieldnames = [
            "match_id", "frame", "timestamp_s", "ball_x", "ball_y", "ball_w", "ball_h",
            "confidence", "status", "velocity_x", "velocity_y", "speed_px_frame"
        ]
        with open(output_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for r in records:
                writer.writerow(r.to_dict())
        print(f"[run_ball_tracking_on_clip] Saved CSV output to: {output_csv_path}")

    # Save to JSON if requested
    if output_json_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_json_path)), exist_ok=True)
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump([r.to_dict() for r in records], f, indent=2)
        print(f"[run_ball_tracking_on_clip] Saved JSON output to: {output_json_path}")

    return records


def load_ball_tracking_csv(csv_path: str) -> Dict[int, BallTrackRecord]:
    """Load ball tracking records from CSV into a frame -> BallTrackRecord dictionary."""
    records_by_frame = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            f_idx = int(row["frame"])
            rec = BallTrackRecord(
                match_id=row["match_id"],
                frame=f_idx,
                timestamp_s=float(row["timestamp_s"]),
                ball_x=float(row["ball_x"]) if row["ball_x"] else None,
                ball_y=float(row["ball_y"]) if row["ball_y"] else None,
                ball_w=float(row["ball_w"]) if row["ball_w"] else None,
                ball_h=float(row["ball_h"]) if row["ball_h"] else None,
                confidence=float(row["confidence"]),
                status=row["status"],
                velocity_x=float(row["velocity_x"]) if row["velocity_x"] else None,
                velocity_y=float(row["velocity_y"]) if row["velocity_y"] else None,
                speed_px_frame=float(row["speed_px_frame"]) if row["speed_px_frame"] else None,
            )
            records_by_frame[f_idx] = rec
    return records_by_frame


def get_aligned_match_frame_data(
    h5_file_path: str,
    ball_records: Dict[int, BallTrackRecord],
    match_id: str,
    frame_idx: int,
) -> Dict[str, Any]:
    """
    Integration helper: retrieves aligned player tracking and ball tracking for a single frame.
    Keyed cleanly by (match_id, frame_idx).
    """
    import h5py

    aligned_data = {
        "match_id": match_id,
        "frame": frame_idx,
        "ball": ball_records.get(frame_idx),
        "players": [],
    }

    with h5py.File(h5_file_path, "r") as f:
        if match_id in f:
            d = f[match_id]
            frames_col = d[:, 0]
            mask = frames_col == frame_idx
            rows = d[mask]
            for r in rows:
                aligned_data["players"].append({
                    "player_id": int(r[1]),
                    "team": int(r[2]),
                    "shirt": int(r[3]),
                    "role": int(r[4]),
                    "x_pos": float(r[5]),
                    "y_pos": float(r[6]),
                    "vx": float(r[7]),
                    "vy": float(r[8]),
                    "roi_x": float(r[9]) if not np.isnan(r[9]) else None,
                    "roi_y": float(r[10]) if not np.isnan(r[10]) else None,
                    "roi_w": float(r[11]) if not np.isnan(r[11]) else None,
                    "roi_h": float(r[12]) if not np.isnan(r[12]) else None,
                })

    return aligned_data
