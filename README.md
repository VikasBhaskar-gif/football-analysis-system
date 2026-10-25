# Football Tactical Predictor
### Coach-Directed Tactical Analysis Platform

An interactive computer vision and spatial analytics platform designed for professional football coaches and tactical analysts. The platform enables coaches to analyze individual player dynamics, unit structures, team shape, space creation, and sequence outcomes from match broadcast footage and player-tracking data.

---

## 1. Product Direction & Coaching Capabilities

The platform is built to support core coaching inquiry workflows:

- **Individual Player Movement & Positioning**: Detailed player trajectories, pressing lines, support runs, deceleration, and off-the-ball movement.
- **Defensive & Midfield Unit Analysis**: Line height, unit vertical/lateral compactness, and inter-line spacing between defensive and midfield blocks.
- **Whole-Team Shape & Space Creation**: Team width, depth, compression, flank overload identification, and open channel creation.
- **Sequences & Post-Action Outcomes**: Tracking territorial progression and defensive reorganization immediately following a pass, reception, or shot.
- **Situational Comparison**: Discovering recurring tactical patterns and comparing similar tactical situations and their outcomes.

---

## 2. Project Architecture & Structure

```text
football-tactical-predictor/
├── football-ai/
│   ├── FOOTPASS/               # Original source dataset (H5 tracking data & match videos)
│   ├── models/                 # Model weights
│   │   ├── ball_tracking/      # YOLO football ball detector weights
│   │   └── yolov8n.pt          # Base detection model weights
│   ├── src/                    # Minimal AI & spatial analytics source modules
│   │   ├── tactical/           # H5 dataset loader, spatial state, and team metadata
│   │   └── tracking/           # Ball detection and tracking engine
│   ├── scripts/                # Essential operational scripts
│   │   ├── launch_web_app.py   # Web application launcher
│   │   └── run_ball_tracking_clip.py # CLI ball tracking driver
│   └── venv/                   # Python virtual environment (PyTorch, OpenCV, Ultralytics)
├── webapp/
│   ├── backend/                # FastAPI application backend
│   │   ├── main.py             # API endpoints, streaming, and static delivery
│   │   ├── analysis_service.py # Match catalog, video indexing, and frame overlay service
│   │   └── video_streaming.py  # HTTP 206 Partial Content video streaming
│   └── frontend/               # React + Vite application shell
│       ├── src/                # Reusable UI infrastructure (VideoPlayer, timeline, coaching panel)
│       └── dist/               # Compiled production web bundle
├── outputs/
│   ├── k8_reference/           # Retained K=8 macro tactical state baseline reference asset
│   └── uploads/                # Directory for user-uploaded match videos
├── scripts/                    # Top-level operational shortcuts
│   ├── launch_web_app.py       # Primary web app launcher
│   └── run_ball_tracking_clip.py
├── src/                        # Core source modules (mirrored for top-level path resolution)
│   ├── tactical/
│   └── tracking/
└── README.md
```

---

## 3. Environment Setup & Launch

### Prerequisites
- Python 3.10+ (configured in `football-ai/venv`)
- Node.js 18+ (for frontend development/builds)

### Launching the Web Application
Run the single-command launcher using the workspace virtual environment:

```powershell
& "football-ai\venv\Scripts\python.exe" scripts/launch_web_app.py
```

The application will be accessible at:
- **Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Building the Frontend
To compile changes in the frontend:

```powershell
cd webapp/frontend
npm run build
```

---

## 4. Key Components Retained

1. **Original Dataset**: Preserved the complete FOOTPASS dataset (`train_tactical_data.h5`, `val_tactical_data.h5`) and Full-HD match videos (`game_27.mp4`, `game_39.mp4`, `game_49.mp4`, `game_51.mp4`).
2. **Ball Tracking**: Retained the specialized YOLO ball detector (`models/ball_tracking/yolo_football_ball_detector.pt`) and inference tracker (`src/tracking/ball_tracker.py`).
3. **K=8 Tactical Reference**: Preserved the historical $K=8$ macro state discovery configuration and metrics in `outputs/k8_reference/` as a comparative baseline.
4. **Application Shell**: Modern, dark-themed video workstation with HTML5 playback, frame-stepping, custom timeline scrubber, broadcast ground-contact foot rings, team color attribution, and video upload capabilities.
