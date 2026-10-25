"""
main.py
=======
FastAPI application backend for the Coach-Directed Football Tactical Analysis Platform.
Provides:
  - Video catalog & upload endpoints
  - HTTP 206 Partial Content video streaming for smooth scrubbing
  - Frame-accurate interval tactical analysis
  - Synchronized canvas overlay geometry and 2D tactical pitch state
  - Proactive AI recommendations and match tactical summaries
  - Sequence and coach manual event annotations
  - Arbitrary multi-player group analysis
  - Static frontend delivery
"""

import os
import sys
import uuid
import shutil
import subprocess
from typing import List, Optional, Dict, Any
import cv2
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel, Field

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from webapp.backend.video_streaming import stream_video_file
from webapp.backend.analysis_service import AnalysisService, UPLOADS_DIR, sanitize_for_json

app = FastAPI(
    title="Football Tactical Predictor API",
    description="Backend API for coach-directed football tactical analysis & proactive AI recommendations",
    version="2.0.0",
)

# Enable CORS for frontend development server (Vite on :5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

service = AnalysisService()


class AnalyzeRequest(BaseModel):
    video_id: str
    start_time: float = Field(..., ge=0.0, description="Interval start in seconds")
    end_time: float = Field(..., ge=0.0, description="Interval end in seconds")
    modules: List[str] = Field(
        default=["player_movement", "unit_analysis", "team_shape", "sequence_outcomes"],
        description="List of coaching analysis modules to run",
    )
    selected_players: Optional[List[int]] = Field(default=None, description="Selected player tracking IDs")
    question: Optional[str] = Field(default=None, description="Optional natural language question")
    scope: str = Field(default="interval", description="'interval', 'full_match', or 'auto'")


class AskCoachRequest(BaseModel):
    video_id: str
    question: str = Field(default="", description="Natural language tactical question for Coach AI")
    start_time: float = Field(default=0.0, ge=0.0)
    end_time: float = Field(default=15.0, ge=0.0)
    scope: str = Field(default="auto", description="'auto', 'interval', or 'full_match'")
    selected_players: Optional[List[int]] = Field(default=None)
    current_time: float = Field(default=0.0, ge=0.0)
    coach_feedback: Optional[str] = Field(default=None, description="Optional feedback or preference to teach the AI")
    coaching_team: Optional[str] = Field(default=None, description="Name or code of the team the coach manages")


class OverlayRequest(BaseModel):
    selected_players: Optional[List[int]] = Field(default=None, description="List of selected player tracking IDs")
    focus_player: Optional[int] = Field(default=None, description="Optional explicit player ID for hypothetical passing/shooting exploration")


class AnnotateRequest(BaseModel):
    timestamp_s: float = Field(..., ge=0.0)
    event_type: str = Field(default="tactical_note")
    player_name: Optional[str] = None
    description: str = Field(default="")


class CompareRequest(BaseModel):
    match_id: str
    entity_type: str = "player"
    entity_1: Dict[str, Any]
    entity_2: Dict[str, Any]


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "Coach-Directed Football Tactical Analysis Platform",
        "version": "2.0.0",
        "workspace": PROJECT_ROOT,
    }


@app.get("/api/matches")
def list_matches():
    """Return all pre-indexed matches and uploaded videos."""
    return service.get_catalog()


@app.get("/api/matches/{video_id}/summary")
def get_match_summary(video_id: str):
    """Return match profile, rosters, data coverage, and proactive recommendations."""
    return service.get_match_summary(video_id)


@app.get("/api/matches/{video_id}/recommendations")
def get_match_recommendations(video_id: str):
    """Return proactive AI tactical findings with timestamps and supporting evidence."""
    return service.get_proactive_recommendations(video_id)


@app.get("/api/matches/{video_id}/events")
def get_match_events(
    video_id: str,
    start: Optional[float] = Query(None, description="Interval start time in seconds"),
    end: Optional[float] = Query(None, description="Interval end time in seconds"),
):
    """Return extracted action events and coach manual annotations."""
    return service.get_match_events(video_id, start_time=start, end_time=end)


@app.post("/api/matches/{video_id}/annotate")
def add_coach_annotation(video_id: str, req: AnnotateRequest):
    """Add a coach manual tactical event annotation."""
    try:
        return service.add_coach_annotation(video_id, req.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record annotation: {e}")


@app.post("/api/upload")
async def upload_video(file: UploadFile = File(...)):
    """Upload a match video (MP4/WebM), probe resolution/fps/duration, and register in catalog."""
    filename = file.filename or "uploaded_video.mp4"
    ext = os.path.splitext(filename)[1].lower()
    if ext not in (".mp4", ".webm", ".mov", ".mkv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '{ext}'. Please upload an MP4, WebM, or MOV video.",
        )

    v_id = f"upload_{uuid.uuid4().hex[:8]}"
    clean_basename = "".join(c for c in os.path.splitext(filename)[0] if c.isalnum() or c in ("-", "_")) or "video"
    dest_path = os.path.join(UPLOADS_DIR, f"{v_id}_{clean_basename}{ext}")

    try:
        with open(dest_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save video to storage: {e}")

    try:
        import imageio_ffmpeg
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cap_probe = cv2.VideoCapture(dest_path)
        fourcc = int(cap_probe.get(cv2.CAP_PROP_FOURCC))
        fourcc_str = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)]).lower()
        cap_probe.release()

        if fourcc_str not in ("h264", "avc1", "vp80", "vp90", "av01"):
            h264_path = os.path.splitext(dest_path)[0] + "_h264.mp4"
            cmd = [
                ffmpeg_exe, "-y", "-i", dest_path,
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
                "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                h264_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
            if res.returncode == 0 and os.path.isfile(h264_path):
                dest_path = h264_path
    except Exception:
        pass

    try:
        entry = service.register_uploaded_video(dest_path, filename, video_id=v_id)
        return {
            "status": "success",
            "message": f"Successfully uploaded and indexed '{filename}'",
            "video": entry,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to probe video properties: {e}")


@app.get("/api/videos/{video_id}/stream")
async def stream_video(video_id: str, request: Request):
    """Stream video with HTTP 206 Partial Content range requests for smooth scrubbing."""
    if not video_id or video_id.startswith("local_"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid video ID.")

    entry = service.get_video_entry(video_id)
    if not entry or not os.path.isfile(entry.get("video_path", "")):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Video '{video_id}' not found in registry.")

    video_path = entry["video_path"]
    ext = os.path.splitext(video_path)[1].lower()
    content_type = "video/webm" if ext == ".webm" else "video/mp4"

    return stream_video_file(request, video_path, content_type=content_type)


@app.post("/api/analyze")
def run_interval_analysis(req: AnalyzeRequest):
    """Initialize tactical interval analysis on selected video interval."""
    if not req.video_id or not isinstance(req.video_id, str) or req.video_id.strip() == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A registered video_id is required for tactical interval analysis.",
        )
    if req.video_id.startswith("local_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Temporary client ID '{req.video_id}' cannot be analyzed. Please wait for video registration to complete.",
        )
    if req.start_time < 0 or req.end_time <= req.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid time interval: start ({req.start_time}s) must be >= 0 and < end ({req.end_time}s).",
        )
    try:
        res = service.analyze_interval(
            video_id=req.video_id,
            start_time=req.start_time,
            end_time=req.end_time,
            modules=req.modules,
            selected_player_ids=req.selected_players,
            question=req.question,
            scope=req.scope,
        )
        return JSONResponse(content=sanitize_for_json(res))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Analysis pipeline error: {e}")


@app.post("/api/ask")
@app.post("/api/coach/ask")
def ask_coach_ai_endpoint(req: AskCoachRequest):
    """Run deep spatiotemporal Coach AI query on interval or full 90-minute match and learn from query."""
    if not req.video_id or req.video_id.startswith("local_"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Valid registered video_id is required.")
    try:
        res = service.ask_coach_ai(
            video_id=req.video_id,
            question=req.question,
            start_time=req.start_time,
            end_time=req.end_time,
            scope=req.scope,
            selected_player_ids=req.selected_players,
            current_time=req.current_time,
            coach_feedback=req.coach_feedback,
            coaching_team=req.coaching_team,
        )
        return JSONResponse(content=sanitize_for_json(res))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Coach AI error: {e}")


@app.get("/api/overlay/{video_id}/{rel_frame}")
def get_frame_overlay(
    video_id: str,
    rel_frame: int,
    selected_players: Optional[str] = Query(None, description="Comma-separated player IDs"),
    focus_player: Optional[int] = Query(None, description="Optional explicit player ID for hypothetical passing/shooting exploration"),
):
    """Fetch 2D overlay and tactical pitch state for frame, with optional selected players."""
    if not video_id or video_id.startswith("local_"):
        return JSONResponse(content={"error": "Invalid video ID", "has_tracking": False})

    selected_ids = None
    if selected_players:
        try:
            selected_ids = [int(x.strip()) for x in selected_players.split(",") if x.strip().isdigit()]
        except Exception:
            selected_ids = None

    return JSONResponse(content=sanitize_for_json(service.get_frame_overlay(video_id, rel_frame, selected_ids, focus_player)))


@app.post("/api/overlay/{video_id}/{rel_frame}")
def post_frame_overlay(video_id: str, rel_frame: int, req: OverlayRequest):
    """Fetch frame overlay with arbitrary player selection via POST."""
    if not video_id or video_id.startswith("local_"):
        return JSONResponse(content={"error": "Invalid video ID", "has_tracking": False})

    return JSONResponse(content=sanitize_for_json(service.get_frame_overlay(video_id, rel_frame, req.selected_players, req.focus_player)))


@app.post("/api/compare")
def compare_entities(req: CompareRequest):
    """Compare two players, units, or periods."""
    try:
        res = service.engine.compare_players(req.match_id, req.entity_1, req.entity_2)
        return JSONResponse(content=sanitize_for_json(res))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison calculation failed: {e}")


# Mount built frontend if available
FRONTEND_DIST = os.path.join(PROJECT_ROOT, "webapp", "frontend", "dist")
if os.path.isdir(FRONTEND_DIST):
    app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="frontend")
