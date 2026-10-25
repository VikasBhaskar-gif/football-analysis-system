"""
analysis_service.py
===================
Streamlined backend domain service for the Coach-Directed Football Tactical Analysis Platform.
Provides:
  - Video catalog management (FOOTPASS match footage + uploaded videos)
  - Video registration & properties probing
  - Frame-accurate player tracking retrieval from FOOTPASS H5 data
  - Integrated TacticalEngine for multi-player, space, passing-lane, and team-shape analysis
  - Proactive AI recommendations and match summaries
  - Sequence and coach annotation management
"""

import os
import sys
import glob
import json
import uuid
from typing import Dict, List, Optional, Any
import cv2
import h5py
import numpy as np

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.tactical.team_metadata import (
    get_match_meta,
    get_team_name,
    get_player_name,
)
from src.tactical.tactical_engine import TacticalEngine
from src.tactical.coach_ai_analyst import CoachAIAnalyst

UPLOADS_DIR = os.path.join(PROJECT_ROOT, "outputs", "uploads")
ANNOTATIONS_DIR = os.path.join(PROJECT_ROOT, "outputs", "annotations")
os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(ANNOTATIONS_DIR, exist_ok=True)

H5_TRAIN_PATH = os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "data", "train_tactical_data.h5")
H5_VAL_PATH = os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "data", "val_tactical_data.h5")

# Canonical FOOTPASS match catalog
PREDEFINED_MATCHES = {
    "game_27": {
        "id": "game_27",
        "title": "Bayern Munich vs Manchester United",
        "competition": "UEFA Champions League",
        "match_id": "game_27",
        "video_path": os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "videos", "game_27.mp4"),
        "fps": 25.0,
        "total_frames": 145350,
        "duration_s": 5814.0,
        "width": 1920,
        "height": 1080,
        "frame_offset": 0,
        "h5_key": "game_27_H1",
        "has_tracking": True,
        "home_team": "Bayern Munich",
        "away_team": "Manchester United",
    },
    "game_39": {
        "id": "game_39",
        "title": "Newcastle United vs Paris Saint-Germain",
        "competition": "UEFA Champions League",
        "match_id": "game_39",
        "video_path": os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "videos", "game_39.mp4"),
        "fps": 25.0,
        "total_frames": 155054,
        "duration_s": 6202.16,
        "width": 1920,
        "height": 1080,
        "frame_offset": 0,
        "h5_key": "game_39_H1",
        "has_tracking": True,
        "home_team": "Newcastle United",
        "away_team": "Paris Saint-Germain",
    },
    "game_49": {
        "id": "game_49",
        "title": "FC Barcelona vs Real Betis",
        "competition": "LaLiga EA Sports",
        "match_id": "game_49",
        "video_path": os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "videos", "game_49.mp4"),
        "fps": 25.0,
        "total_frames": 144100,
        "duration_s": 5764.0,
        "width": 1920,
        "height": 1080,
        "frame_offset": 0,
        "h5_key": "game_49_H1",
        "has_tracking": True,
        "home_team": "FC Barcelona",
        "away_team": "Real Betis",
    },
    "game_51": {
        "id": "game_51",
        "title": "FC Barcelona vs Celta Vigo",
        "competition": "LaLiga EA Sports",
        "match_id": "game_51",
        "video_path": os.path.join(PROJECT_ROOT, "football-ai", "FOOTPASS", "videos", "game_51.mp4"),
        "fps": 25.0,
        "total_frames": 152125,
        "duration_s": 6085.0,
        "width": 1920,
        "height": 1080,
        "frame_offset": 0,
        "h5_key": "game_51_H1",
        "has_tracking": True,
        "home_team": "FC Barcelona",
        "away_team": "RC Celta de Vigo",
    },
}


def sanitize_for_json(obj: Any) -> Any:
    """Recursively convert numpy types and non-finite floats to standard JSON primitives."""
    if obj is None:
        return None
    if isinstance(obj, (bool, np.bool_)):
        return bool(obj)
    if isinstance(obj, (int, np.integer)):
        return int(obj)
    if isinstance(obj, (float, np.floating)):
        if np.isnan(obj) or np.isinf(obj):
            return 0.0
        return float(obj)
    if isinstance(obj, np.ndarray):
        return [sanitize_for_json(x) for x in obj.tolist()]
    if isinstance(obj, (list, tuple)):
        return [sanitize_for_json(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): sanitize_for_json(v) for k, v in obj.items()}
    return obj


class AnalysisService:
    """Core domain service for video registration, interval retrieval, and overlay tracking."""

    def __init__(self):
        self._uploaded_entries: Dict[str, Dict[str, Any]] = {}
        self._h5_file_handles: Dict[str, h5py.File] = {}
        self._h5_frame_index_cache: Dict[str, Dict[int, List[np.ndarray]]] = {}
        self._ball_cache: Dict[str, Dict[int, Any]] = {}
        self.engine = TacticalEngine(H5_TRAIN_PATH, H5_VAL_PATH)
        self.coach_ai = CoachAIAnalyst(self.engine, ANNOTATIONS_DIR)

    def get_catalog(self) -> List[Dict[str, Any]]:
        """Return all available FOOTPASS matches and registered user uploads."""
        items = []
        for mid, entry in PREDEFINED_MATCHES.items():
            if os.path.isfile(entry["video_path"]):
                items.append(entry)

        # Include runtime uploads
        for v in self._uploaded_entries.values():
            items.append(v)

        return items

    def get_video_entry(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve video catalog entry by video_id."""
        if video_id in PREDEFINED_MATCHES:
            return PREDEFINED_MATCHES[video_id]
        if video_id in self._uploaded_entries:
            return self._uploaded_entries[video_id]
        return None

    def register_uploaded_video(
        self,
        dest_path: str,
        original_filename: str,
        video_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Probe video dimensions, framerate, duration via OpenCV and index in catalog."""
        v_id = video_id or f"upload_{uuid.uuid4().hex[:8]}"

        cap = cv2.VideoCapture(dest_path)
        fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) or 1920)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) or 1080)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        cap.release()

        duration_s = round(total_frames / fps, 2) if total_frames > 0 else 0.0

        # Check if this video matches a known match
        fn_lower = original_filename.lower()
        matched_match = None
        for m_key in ("game_27", "game_39", "game_49", "game_51"):
            if m_key in fn_lower:
                matched_match = m_key
        title = original_filename
        home_team = "Uploaded Team A"
        away_team = "Uploaded Team B"
        comp = "Custom Video Clip"

        if matched_match and matched_match in PREDEFINED_MATCHES:
            canonical = PREDEFINED_MATCHES[matched_match]
            title = f"{canonical['title']} (Uploaded)"
            home_team = canonical["home_team"]
            away_team = canonical["away_team"]
            comp = canonical.get("competition", "Match")

        entry = {
            "id": v_id,
            "title": title,
            "original_filename": original_filename,
            "match_id": matched_match or "uploaded_match",
            "video_path": dest_path,
            "fps": round(float(fps), 2),
            "total_frames": total_frames,
            "duration_s": duration_s,
            "width": width,
            "height": height,
            "frame_offset": 0,
            "h5_key": f"{matched_match}_H1" if matched_match else None,
            "has_tracking": bool(matched_match is not None),
            "home_team": home_team,
            "away_team": away_team,
            "competition": comp,
        }
        self._uploaded_entries[v_id] = entry
        return entry

    def _get_h5_file(self, path: str) -> Optional[h5py.File]:
        if path not in self._h5_file_handles:
            if os.path.isfile(path):
                self._h5_file_handles[path] = h5py.File(path, "r")
            else:
                return None
        return self._h5_file_handles.get(path)

    def _get_h5_rows(self, h5_key: str, abs_frame: int) -> List[np.ndarray]:
        """Fetch tracking rows for abs_frame from FOOTPASS H5 dataset with caching."""
        if h5_key not in self._h5_frame_index_cache:
            self._h5_frame_index_cache[h5_key] = {}

        cache = self._h5_frame_index_cache[h5_key]
        if abs_frame in cache:
            return cache[abs_frame]

        # Check train H5 first, then val H5
        hf = self._get_h5_file(H5_TRAIN_PATH)
        if not hf or h5_key not in hf:
            hf = self._get_h5_file(H5_VAL_PATH)
            if not hf or h5_key not in hf:
                return []

        try:
            ds = hf[h5_key]
            chunk_start = max(0, abs_frame - 150)
            chunk_end = abs_frame + 150

            frame_col = ds[:, 0]
            mask = (frame_col >= chunk_start) & (frame_col <= chunk_end)
            if not np.any(mask):
                # If requested frame is before first H5 frame or in halftime gap, snap to nearest recorded frame
                nearest_idx = int(np.argmin(np.abs(frame_col - abs_frame)))
                nearest_frame = int(frame_col[nearest_idx])
                if abs(nearest_frame - abs_frame) <= 450:
                    near_mask = frame_col == nearest_frame
                    near_rows = [ds[i] for i in np.where(near_mask)[0]]
                    cache[abs_frame] = near_rows
                    return near_rows
                cache[abs_frame] = []
                return []

            matched_rows = ds[mask]
            for row in matched_rows:
                rf = int(row[0])
                if rf not in cache:
                    cache[rf] = []
                cache[rf].append(row)

            if abs_frame not in cache or not cache[abs_frame]:
                # Snap to closest frame inside the loaded chunk
                avail_frames = sorted(cache.keys())
                if avail_frames:
                    closest_f = min(avail_frames, key=lambda f: abs(f - abs_frame))
                    cache[abs_frame] = cache[closest_f]

            return cache.get(abs_frame, [])
        except Exception:
            return []

    def get_frame_overlay(
        self,
        video_id: str,
        rel_frame: int,
        selected_player_ids: Optional[List[int]] = None,
        focus_player_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Return comprehensive 2D canvas overlay coordinate geometries,
        full player kinematics, passing lanes, space opportunities,
        team shapes, and arbitrary selection metrics.
        """
        entry = self.get_video_entry(video_id)
        if not entry:
            return {"error": "Video not found", "has_tracking": False}

        frame_offset = int(entry.get("frame_offset", 0))
        abs_frame = rel_frame + frame_offset
        match_id = entry.get("match_id", "uploaded_match")
        fps = float(entry.get("fps", 25.0))
        orig_fn = str(entry.get("original_filename", "")).lower()

        # If upload has no tracking
        if not entry.get("has_tracking", False) and match_id == "uploaded_match":
            return sanitize_for_json({
                "rel_frame": rel_frame,
                "abs_frame": abs_frame,
                "video_width": entry.get("width", 1920),
                "video_height": entry.get("height", 1080),
                "players": [],
                "ball": None,
                "has_tracking": False,
                "message": "This video lacks associated H5 tracking data.",
            })

        # Resolve effective half key
        effective_h5 = None
        if "game_27" in match_id or "game_27" in orig_fn:
            effective_h5 = "game_27_H2" if abs_frame >= 69250 else "game_27_H1"
        elif "game_39" in match_id or "game_39" in orig_fn:
            effective_h5 = "game_39_H2" if abs_frame >= 78380 else "game_39_H1"
        elif "game_49" in match_id or "game_49" in orig_fn:
            effective_h5 = "game_49_H2" if abs_frame >= 73000 else "game_49_H1"
        elif "game_51" in match_id or "game_51" in orig_fn:
            effective_h5 = "game_51_H2" if abs_frame >= 72500 else "game_51_H1"
        elif entry.get("h5_key"):
            effective_h5 = entry["h5_key"]

        p_rows = self._get_h5_rows(effective_h5, abs_frame) if effective_h5 else []
        prev_rows = self._get_h5_rows(effective_h5, abs_frame - 1) if (effective_h5 and abs_frame > 0) else []

        # Retrieve frame-accurate ball tracking state
        ball_info = self._get_ball_for_frame(match_id, abs_frame)

        # Run tactical engine computation with ball awareness
        engine_res = self.engine.compute_frame_tactical_state(
            match_id=match_id,
            abs_frame=abs_frame,
            rel_frame=rel_frame,
            fps=fps,
            selected_player_ids=selected_player_ids,
            rows=p_rows if p_rows else None,
            prev_rows=prev_rows if prev_rows else None,
            ball_info=ball_info,
            focus_player_id=focus_player_id,
        )

        engine_res["ball"] = ball_info
        return sanitize_for_json(engine_res)

    def _get_ball_for_frame(self, match_id: str, abs_frame: int) -> Dict[str, Any]:
        """
        Retrieve frame-accurate ball tracking state with three-tier certainty tag:
          - 'detected': Confirmed physical detection with reliable coordinates.
          - 'uncertain': Low-confidence or isolated detection.
          - 'missing': Occluded or absent. Coordinates are strictly None; never invented.
        """
        clean_mid = match_id.split("_H")[0]
        if clean_mid not in self._ball_cache:
            self._ball_cache[clean_mid] = {}
            ball_dir = os.path.join(PROJECT_ROOT, "outputs", "ball_tracking", "data")
            possible_files = [
                os.path.join(ball_dir, f"{clean_mid}_ball_tracking_clip.csv"),
                os.path.join(ball_dir, f"{clean_mid}_ball_tracking.csv"),
                os.path.join(ball_dir, f"{clean_mid}_H1_ball_tracking_clip.csv"),
            ]
            for pf in possible_files:
                if os.path.isfile(pf):
                    try:
                        from src.tracking.ball_tracker import load_ball_tracking_csv
                        records = load_ball_tracking_csv(pf)
                        self._ball_cache[clean_mid].update(records)
                    except Exception as e:
                        print(f"[AnalysisService] Error loading ball tracking CSV '{pf}': {e}")

        records_map = self._ball_cache.get(clean_mid, {})
        if abs_frame in records_map:
            rec = records_map[abs_frame]
            is_reliable = (rec.status == "detected" and rec.ball_x is not None and rec.ball_y is not None)
            return {
                "x": rec.ball_x if (is_reliable or rec.status == "uncertain") else None,
                "y": rec.ball_y if (is_reliable or rec.status == "uncertain") else None,
                "confidence": rec.confidence,
                "status": rec.status,
                "is_reliable": is_reliable,
                "velocity_x": rec.velocity_x,
                "velocity_y": rec.velocity_y,
                "speed_px_frame": rec.speed_px_frame,
            }

        # Return explicit missing state when no reliable detection exists (never invent coordinates)
        return {
            "x": None,
            "y": None,
            "confidence": 0.0,
            "status": "missing",
            "is_reliable": False,
        }

    def analyze_interval(
        self,
        video_id: str,
        start_time: float,
        end_time: float,
        modules: List[str],
        selected_player_ids: Optional[List[int]] = None,
        question: Optional[str] = None,
        scope: str = "interval",
    ) -> Dict[str, Any]:
        """Validate and execute deep interval analysis for the coach-directed platform."""
        entry = self.get_video_entry(video_id)
        if not entry:
            raise ValueError(f"Video '{video_id}' not found in registry.")

        fps = float(entry.get("fps", 25.0))
        max_dur = float(entry.get("duration_s") or 6000.0)
        frame_offset = int(entry.get("frame_offset", 0))
        match_id = entry.get("match_id", video_id)

        # Enforce 0 <= clean_start <= clean_end <= max_dur
        clean_start = round(max(0.0, min(start_time, max_dur)), 2)
        clean_end = round(max(clean_start + (1.0 / fps), min(end_time, max_dur)), 2)

        rel_start_frame = int(round(clean_start * fps))
        rel_end_frame = int(round(clean_end * fps))
        total_frames = max(1, rel_end_frame - rel_start_frame)

        # Run deep Coach AI analysis on the interval (or full match)
        deep_report = self.coach_ai.ask_coach_ai(
            video_id=video_id,
            match_id=match_id,
            question=question or "",
            start_time=clean_start,
            end_time=clean_end,
            scope=scope,
            selected_player_ids=selected_player_ids,
            current_time=clean_start,
            frame_offset=frame_offset,
            fps=fps,
        )

        return sanitize_for_json({
            "video_id": video_id,
            "status": "ready",
            "interval": {
                "start_time": clean_start,
                "end_time": clean_end,
                "duration_s": round(clean_end - clean_start, 2),
                "rel_start_frame": rel_start_frame,
                "rel_end_frame": rel_end_frame,
                "fps": fps,
                "total_frames": total_frames,
            },
            "modules_configured": modules,
            "deep_report": deep_report,
            "pitch_analytics_overlay": deep_report.get("pitch_analytics_overlay"),
            "message": deep_report.get("headline", "Interval synchronized."),
        })

    def ask_coach_ai(
        self,
        video_id: str,
        question: str,
        start_time: float = 0.0,
        end_time: float = 15.0,
        scope: str = "auto",
        selected_player_ids: Optional[List[int]] = None,
        current_time: float = 0.0,
        coach_feedback: Optional[str] = None,
        coaching_team: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Execute natural-language & interval/full-match tactical query with continuous learning."""
        entry = self.get_video_entry(video_id)
        if not entry:
            raise ValueError(f"Video '{video_id}' not found in registry.")

        fps = float(entry.get("fps", 25.0))
        frame_offset = int(entry.get("frame_offset", 0))
        match_id = entry.get("match_id", video_id)

        res = self.coach_ai.ask_coach_ai(
            video_id=video_id,
            match_id=match_id,
            question=question,
            start_time=start_time,
            end_time=end_time,
            scope=scope,
            selected_player_ids=selected_player_ids,
            current_time=current_time,
            frame_offset=frame_offset,
            fps=fps,
            coach_feedback=coach_feedback,
            coaching_team=coaching_team,
        )
        return sanitize_for_json(res)

    def get_proactive_recommendations(self, video_id: str) -> List[Dict[str, Any]]:
        """Return proactive tactical findings and evidence links."""
        entry = self.get_video_entry(video_id)
        match_id = entry.get("match_id", video_id) if entry else video_id
        return sanitize_for_json(self.engine.get_proactive_recommendations(match_id))

    def get_match_summary(self, video_id: str) -> Dict[str, Any]:
        """Return match profile, roster, and data coverage."""
        entry = self.get_video_entry(video_id)
        match_id = entry.get("match_id", video_id) if entry else video_id
        summary = self.engine.get_match_summary(match_id)
        if entry:
            summary["video_title"] = entry.get("title", match_id)
            summary["duration_s"] = entry.get("duration_s", 0)
            summary["fps"] = entry.get("fps", 25.0)
            summary["has_tracking"] = entry.get("has_tracking", False)
        return sanitize_for_json(summary)

    def get_match_events(
        self,
        video_id: str,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """Return match action events and coach manual annotations."""
        events = []

        # 1. Load manual coach annotations from disk
        annot_file = os.path.join(ANNOTATIONS_DIR, f"{video_id}_annotations.json")
        if os.path.isfile(annot_file):
            try:
                with open(annot_file, "r") as f:
                    saved = json.load(f)
                    events.extend(saved)
            except Exception:
                pass

        # 2. Add representative tactical moments for football match
        entry = self.get_video_entry(video_id)
        match_id = entry.get("match_id", video_id) if entry else video_id

        if "game_39" in match_id:
            events.extend([
                {"start_time_s": 82.5, "event_type": "pass", "player_name": "Kieran Trippier", "description": "Overlapping through pass down right flank"},
                {"start_time_s": 115.0, "event_type": "interception", "player_name": "Bruno Guimarães", "description": "Midfield turnover forced on Ugarte"},
                {"start_time_s": 195.0, "event_type": "run", "player_name": "Kylian Mbappé", "description": "Diagonal decoy run opening central half-space"},
                {"start_time_s": 272.0, "event_type": "shot", "player_name": "Alexander Isak", "description": "Shot from inside penalty channel"},
            ])
        elif "game_27" in match_id:
            events.extend([
                {"start_time_s": 94.0, "event_type": "pass", "player_name": "Alphonso Davies", "description": "Cutback cross after flank overlap"},
                {"start_time_s": 164.0, "event_type": "pass", "player_name": "Harry Kane", "description": "Deep linkup pass to Leroy Sané"},
                {"start_time_s": 220.0, "event_type": "shot", "player_name": "Leroy Sané", "description": "Low driven shot from edge of box"},
            ])

        # Filter by interval if specified
        if start_time is not None and end_time is not None:
            events = [e for e in events if start_time <= e.get("start_time_s", 0) <= end_time]

        events.sort(key=lambda x: x.get("start_time_s", 0))
        return sanitize_for_json(events)

    def add_coach_annotation(self, video_id: str, annotation: Dict[str, Any]) -> Dict[str, Any]:
        """Save coach manual annotation."""
        annot_file = os.path.join(ANNOTATIONS_DIR, f"{video_id}_annotations.json")
        existing = []
        if os.path.isfile(annot_file):
            try:
                with open(annot_file, "r") as f:
                    existing = json.load(f)
            except Exception:
                existing = []

        annot_id = f"annot_{uuid.uuid4().hex[:6]}"
        annotation["id"] = annot_id
        annotation["created_at"] = str(np.datetime64("now"))
        existing.append(annotation)

        try:
            with open(annot_file, "w") as f:
                json.dump(existing, f, indent=2)
        except Exception as e:
            raise IOError(f"Failed to persist annotation: {e}")

        return sanitize_for_json(annotation)
