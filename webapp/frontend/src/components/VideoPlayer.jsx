import React, { useRef, useState, useEffect, useCallback } from 'react';
import { 
  Play, 
  Pause, 
  SkipBack, 
  SkipForward, 
  Cpu, 
  RefreshCw,
  Repeat,
  Target,
  Shield,
  Calendar,
  Layers,
  AlertTriangle,
  UploadCloud,
  Clock,
  BookmarkPlus
} from 'lucide-react';

// Safe Canvas RoundRect Helper with Quadratic Curve Fallback
function safeRoundRect(ctx, x, y, w, h, r = 4) {
  if (typeof ctx.roundRect === 'function') {
    ctx.roundRect(x, y, w, h, r);
  } else {
    const rad = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
    ctx.moveTo(x + rad, y);
    ctx.lineTo(x + w - rad, y);
    ctx.quadraticCurveTo(x + w, y, x + w, y + rad);
    ctx.lineTo(x + w, y + h - rad);
    ctx.quadraticCurveTo(x + w, y + h, x + w - rad, y + h);
    ctx.lineTo(x + rad, y + h);
    ctx.quadraticCurveTo(x, y + h, x, y + h - rad);
    ctx.lineTo(x, y + rad);
    ctx.quadraticCurveTo(x, y, x + rad, y);
  }
}

// 2D Convex Hull (Monotone Chain) for guaranteed screen-space team shape
function compute2DConvexHull(points) {
  if (!points || points.length < 3) return points || [];
  const pts = points.slice().sort((a, b) => (a[0] === b[0] ? a[1] - b[1] : a[0] - b[0]));
  const cross = (o, a, b) => (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0]);
  
  const lower = [];
  for (let p of pts) {
    while (lower.length >= 2 && cross(lower[lower.length - 2], lower[lower.length - 1], p) <= 0) {
      lower.pop();
    }
    lower.push(p);
  }
  
  const upper = [];
  for (let i = pts.length - 1; i >= 0; i--) {
    const p = pts[i];
    while (upper.length >= 2 && cross(upper[upper.length - 2], upper[upper.length - 1], p) <= 0) {
      upper.pop();
    }
    upper.push(p);
  }
  
  lower.pop();
  upper.pop();
  return lower.concat(upper);
}

export default function VideoPlayer({
  activeMatch,
  intervalStart,
  setIntervalStart,
  intervalEnd,
  setIntervalEnd,
  currentTime,
  setCurrentTime,
  onDurationDiscovered,
  onRunAnalysis,
  isAnalyzing,
  overlayData,
  analysisResult,
  seekTargetTime,
  setSeekTargetTime,
  activeAnalysisMode,
  setActiveAnalysisMode,
  overlayToggles,
  setOverlayToggles,
  onUploadAnotherVideo,
  isUploading,
  selectedPlayerIds = [],
  onTogglePlayerSelection,
  highlightedReceiverId = null,
}) {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const trackRef = useRef(null);
  const isDraggingScrubberRef = useRef(false);
  const isDraggingInHandleRef = useRef(false);
  const isDraggingOutHandleRef = useRef(false);
  const isDraggingRangeRef = useRef(false);
  const dragRangeStartMouseX = useRef(0);
  const dragRangeInitialStart = useRef(0);
  const dragRangeInitialEnd = useRef(0);
  const smoothedPlayersRef = useRef(new Map());
  const smoothedBallRef = useRef({ x: null, y: null, lastSeen: 0 });

  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoopingInterval, setIsLoopingInterval] = useState(false);
  const [videoError, setVideoError] = useState(null);
  const [nativeDuration, setNativeDuration] = useState(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showAllLanes, setShowAllLanes] = useState(false);

  const [selectedModules, setSelectedModules] = useState({
    tactical_states: true,
    possession: true,
    tactical_options: true,
  });

  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [hoverTimeline, setHoverTimeline] = useState(null);

  const handleToggleSpeed = () => {
    const speeds = [1.0, 1.5, 2.0, 0.5];
    const nextIdx = (speeds.indexOf(playbackSpeed) + 1) % speeds.length;
    const nextSpeed = speeds[nextIdx];
    setPlaybackSpeed(nextSpeed);
    if (videoRef.current) {
      videoRef.current.playbackRate = nextSpeed;
    }
  };

  const fps = activeMatch?.fps || 25.0;
  const effectiveDuration = Math.max(
    0.1,
    nativeDuration || activeMatch?.duration_s || (videoRef.current?.duration && isFinite(videoRef.current.duration) ? videoRef.current.duration : 15.0)
  );

  // Sync external seek requests (e.g. clicking an event in the timeline)
  useEffect(() => {
    if (seekTargetTime !== null && videoRef.current) {
      videoRef.current.currentTime = seekTargetTime;
      setCurrentTime(seekTargetTime);
      setSeekTargetTime(null);
    }
  }, [seekTargetTime, setCurrentTime, setSeekTargetTime]);

  // Handle Play/Pause
  const togglePlay = () => {
    if (!videoRef.current) return;
    if (isPlaying) {
      videoRef.current.pause();
      setIsPlaying(false);
    } else {
      videoRef.current.play().then(() => setIsPlaying(true)).catch((err) => {
        console.warn('Playback error:', err);
      });
    }
  };

  // Step Frame (-1 or +1)
  const stepFrame = (delta) => {
    if (!videoRef.current) return;
    videoRef.current.pause();
    setIsPlaying(false);
    const newTime = Math.max(0, Math.min(effectiveDuration, videoRef.current.currentTime + delta * (1.0 / fps)));
    videoRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  // Video TimeUpdate handler
  const handleTimeUpdate = () => {
    if (!videoRef.current || isDraggingScrubberRef.current) return;
    const t = videoRef.current.currentTime;
    setCurrentTime(t);

    // Loop interval if enabled
    if (isLoopingInterval && t >= intervalEnd) {
      videoRef.current.currentTime = intervalStart;
      setCurrentTime(intervalStart);
    }
  };

  // Metadata loaded handler
  const handleLoadedMetadata = (e) => {
    setVideoError(null);
    const dur = e.target.duration;
    if (dur && isFinite(dur) && dur > 0) {
      setNativeDuration(dur);
      if (onDurationDiscovered) {
        onDurationDiscovered(dur);
      }
    }
  };

  // Error handler
  const handleVideoError = (e) => {
    console.error('HTML5 Video decoding error:', e);
    setVideoError('Video playback could not be decoded by the browser. Please ensure the file is a standard H.264 MP4 or WebM video.');
  };

  // Helper: compute time in seconds from mouse position on track
  const getTimeFromMouseEvent = useCallback((e) => {
    if (!trackRef.current) return 0;
    const rect = trackRef.current.getBoundingClientRect();
    const pos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
    return pos * effectiveDuration;
  }, [effectiveDuration]);

  // Playhead Scrubber Logic
  const handleTrackMouseDown = (e) => {
    if (e.target.closest('.timeline-handle') || e.target.closest('.timeline-range-body')) {
      return;
    }
    e.preventDefault();
    isDraggingScrubberRef.current = true;
    const targetT = getTimeFromMouseEvent(e);
    if (videoRef.current) {
      videoRef.current.currentTime = targetT;
    }
    setCurrentTime(targetT);

    const handleMouseMove = (moveEvent) => {
      if (isDraggingScrubberRef.current) {
        const t = getTimeFromMouseEvent(moveEvent);
        if (videoRef.current) {
          videoRef.current.currentTime = t;
        }
        setCurrentTime(t);
      }
    };

    const handleMouseUp = () => {
      isDraggingScrubberRef.current = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Drag IN Handle Logic
  const handleInHandleMouseDown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    isDraggingInHandleRef.current = true;

    const handleMouseMove = (moveEvent) => {
      if (isDraggingInHandleRef.current) {
        const t = getTimeFromMouseEvent(moveEvent);
        const clamped = Math.max(0, Math.min(intervalEnd - (1.0 / fps), t));
        setIntervalStart(Math.round(clamped * 100) / 100);
      }
    };

    const handleMouseUp = () => {
      isDraggingInHandleRef.current = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Drag OUT Handle Logic
  const handleOutHandleMouseDown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    isDraggingOutHandleRef.current = true;

    const handleMouseMove = (moveEvent) => {
      if (isDraggingOutHandleRef.current) {
        const t = getTimeFromMouseEvent(moveEvent);
        const clamped = Math.min(effectiveDuration, Math.max(intervalStart + (1.0 / fps), t));
        setIntervalEnd(Math.round(clamped * 100) / 100);
      }
    };

    const handleMouseUp = () => {
      isDraggingOutHandleRef.current = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Drag Range Window Body (sliding the window across the video)
  const handleRangeBodyMouseDown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    isDraggingRangeRef.current = true;
    dragRangeStartMouseX.current = e.clientX;
    dragRangeInitialStart.current = intervalStart;
    dragRangeInitialEnd.current = intervalEnd;

    const trackWidth = trackRef.current?.getBoundingClientRect().width || 1000;
    const dur = intervalEnd - intervalStart;

    const handleMouseMove = (moveEvent) => {
      if (isDraggingRangeRef.current) {
        const deltaPx = moveEvent.clientX - dragRangeStartMouseX.current;
        const deltaSeconds = (deltaPx / trackWidth) * effectiveDuration;
        let newStart = dragRangeInitialStart.current + deltaSeconds;
        let newEnd = dragRangeInitialEnd.current + deltaSeconds;

        if (newStart < 0) {
          newStart = 0;
          newEnd = dur;
        } else if (newEnd > effectiveDuration) {
          newEnd = effectiveDuration;
          newStart = Math.max(0, effectiveDuration - dur);
        }

        setIntervalStart(Math.round(newStart * 100) / 100);
        setIntervalEnd(Math.round(newEnd * 100) / 100);
      }
    };

    const handleMouseUp = () => {
      isDraggingRangeRef.current = false;
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
  };

  // Frame Steppers & Reset Helpers
  const stepIntervalStart = (deltaFrames) => {
    const newT = Math.max(0, Math.min(intervalEnd - (1.0 / fps), intervalStart + deltaFrames * (1.0 / fps)));
    setIntervalStart(Math.round(newT * 100) / 100);
  };

  const stepIntervalEnd = (deltaFrames) => {
    const newT = Math.min(effectiveDuration, Math.max(intervalStart + (1.0 / fps), intervalEnd + deltaFrames * (1.0 / fps)));
    setIntervalEnd(Math.round(newT * 100) / 100);
  };

  const handleSetInToPlayhead = () => {
    const roundedTime = Math.round(currentTime * 100) / 100;
    const clampedIn = Math.max(0, Math.min(effectiveDuration - (1.0 / fps), roundedTime));
    let newEnd = intervalEnd;
    if (clampedIn >= newEnd) {
      newEnd = Math.min(effectiveDuration, Math.round((clampedIn + 15.0) * 100) / 100);
    }
    setIntervalStart(clampedIn);
    setIntervalEnd(newEnd);
  };

  const handleSetOutToPlayhead = () => {
    const roundedTime = Math.round(currentTime * 100) / 100;
    const clampedOut = Math.min(effectiveDuration, Math.max(1.0 / fps, roundedTime));
    let newStart = intervalStart;
    if (clampedOut <= newStart) {
      newStart = Math.max(0, Math.round((clampedOut - 15.0) * 100) / 100);
    }
    setIntervalStart(newStart);
    setIntervalEnd(clampedOut);
  };

  const resetInterval = () => {
    setIntervalStart(0.0);
    setIntervalEnd(Math.min(effectiveDuration, 15.0));
  };

  // Handle Drag & Drop to replace video directly on stage
  const handleDropOnStage = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0 && onUploadAnotherVideo) {
      onUploadAnotherVideo(e.dataTransfer.files[0]);
    }
  };

  // Synchronize canvas bounding rect with actual rendered video pixels (eliminating letterbox/pillarbox offset)
  const updateCanvasTransform = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const vw = video.videoWidth || (overlayData?.video_width || 1920);
    const vh = video.videoHeight || (overlayData?.video_height || 1080);
    const cw = video.clientWidth;
    const ch = video.clientHeight;

    if (!cw || !ch || !vw || !vh) return;

    const videoRatio = vw / vh;
    const containerRatio = cw / ch;

    let renderWidth, renderHeight, offsetX, offsetY;
    if (containerRatio > videoRatio) {
      renderHeight = ch;
      renderWidth = ch * videoRatio;
      offsetX = (cw - renderWidth) / 2;
      offsetY = 0;
    } else {
      renderWidth = cw;
      renderHeight = cw / videoRatio;
      offsetX = 0;
      offsetY = (ch - renderHeight) / 2;
    }

    if (canvas.width !== vw) canvas.width = vw;
    if (canvas.height !== vh) canvas.height = vh;

    canvas.style.position = 'absolute';
    canvas.style.left = `${Math.round(offsetX)}px`;
    canvas.style.top = `${Math.round(offsetY)}px`;
    canvas.style.width = `${Math.round(renderWidth)}px`;
    canvas.style.height = `${Math.round(renderHeight)}px`;
    canvas.style.pointerEvents = 'auto';
    canvas.style.cursor = 'pointer';
  }, [overlayData?.video_width, overlayData?.video_height]);

  const handleCanvasClick = useCallback((e) => {
    const canvas = canvasRef.current;
    if (!canvas || !overlayData?.players || !onTogglePlayerSelection) return;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    const clickX = (e.clientX - rect.left) * scaleX;
    const clickY = (e.clientY - rect.top) * scaleY;

    let closest = null;
    let minDist = 50;
    for (const p of overlayData.players) {
      let fx = p.foot_x;
      let fy = p.foot_y;
      if (fx === undefined || fx === null || fy === undefined || fy === null) {
        if (p.bbox) {
          fx = p.bbox[0] + p.bbox[2] / 2;
          fy = p.bbox[1] + p.bbox[3];
        }
      }
      if (fx !== undefined && fx !== null && fy !== undefined && fy !== null) {
        const d = Math.hypot(clickX - fx, clickY - fy);
        if (d < minDist) {
          minDist = d;
          closest = p;
        }
      }
    }
    if (closest) {
      onTogglePlayerSelection(closest.player_id);
    }
  }, [overlayData?.players, onTogglePlayerSelection]);

  useEffect(() => {
    updateCanvasTransform();
    window.addEventListener('resize', updateCanvasTransform);

    let observer = null;
    if (videoRef.current && window.ResizeObserver) {
      observer = new ResizeObserver(() => {
        updateCanvasTransform();
      });
      observer.observe(videoRef.current);
    }

    return () => {
      window.removeEventListener('resize', updateCanvasTransform);
      if (observer) observer.disconnect();
    };
  }, [updateCanvasTransform]);

  // Broadcast-style Canvas Overlay Drawing (strictly transparent and aligned to video)
  const drawOverlay = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // If active video has no tracking or overlay data is empty, keep canvas 100% transparent
    if (!activeMatch?.has_tracking || !overlayData) return;

    try {
      const scaleX = canvas.width / (overlayData.video_width || 1920);
      const scaleY = canvas.height / (overlayData.video_height || 1080);

      // 1. Draw Space Opportunities (Restrained Tactical Spaces)
      if (overlayToggles?.spaces && overlayData?.space_opportunities && overlayData.space_opportunities.length > 0) {
        overlayData.space_opportunities.forEach((sp) => {
          if (sp.img_polygon && sp.img_polygon.length >= 3) {
            // Check if coordinates fall within reasonable broadcast window
            const validPoints = sp.img_polygon.filter(
              ([x, y]) => !isNaN(x) && !isNaN(y) && x >= -80 && x <= 2000 && y >= -80 && y <= 1160
            );
            if (validPoints.length >= 3) {
              // Screen area check: restrain huge arbitrary whole-screen polygons (> 32% canvas area)
              const xs = validPoints.map((p) => p[0]);
              const ys = validPoints.map((p) => p[1]);
              const minX = Math.min(...xs), maxX = Math.max(...xs);
              const minY = Math.min(...ys), maxY = Math.max(...ys);
              const w = maxX - minX;
              const h = maxY - minY;
              if (w * h > 1920 * 1080 * 0.32) return; // Discard oversized flood-fills

              ctx.save();
              ctx.beginPath();
              ctx.moveTo(validPoints[0][0] * scaleX, validPoints[0][1] * scaleY);
              for (let i = 1; i < validPoints.length; i++) {
                ctx.lineTo(validPoints[i][0] * scaleX, validPoints[i][1] * scaleY);
              }
              ctx.closePath();
              ctx.fillStyle = 'rgba(56, 189, 248, 0.10)';
              ctx.fill();
              ctx.strokeStyle = 'rgba(56, 189, 248, 0.65)';
              ctx.lineWidth = 1.4;
              ctx.setLineDash([4, 4]);
              ctx.stroke();

              // Space Centroid Label (restrained, unobtrusive)
              const polyMidX = (validPoints.reduce((acc, p) => acc + p[0], 0) / validPoints.length) * scaleX;
              const polyMidY = (validPoints.reduce((acc, p) => acc + p[1], 0) / validPoints.length) * scaleY;
              if (polyMidX >= 50 && polyMidX <= canvas.width - 50 && polyMidY >= 30 && polyMidY <= canvas.height - 30) {
                const lbl = sp.label || sp.area_name || 'SPACE';
                ctx.font = '600 9px system-ui, sans-serif';
                const textW = ctx.measureText(lbl).width + 8;
                ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
                ctx.beginPath();
                safeRoundRect(ctx, polyMidX - textW / 2, polyMidY - 7, textW, 14, 3);
                ctx.fill();
                ctx.fillStyle = '#7dd3fc';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(lbl, polyMidX, polyMidY);
              }
              ctx.restore();
            }
          }
        });
      }

      // 2. Team Shape & Defensive Backline Overlays
      if (overlayToggles?.teamShape && overlayData?.players) {
        ctx.save();
        const ts = overlayData.team_shape || {};
        const teams = [0, 1];

        teams.forEach((tId) => {
          const tData = ts[`team_${tId}`];
          const teamPlayers = overlayData.players.filter(
            (p) => p.team === tId && !p.is_goalkeeper && p.role !== 1
          );
          if (teamPlayers.length < 3) return;

          const isT0 = tId === 0;
          const baseColor = isT0 ? '#00e5ff' : '#ef4444';
          const teamName = teamPlayers[0]?.team_name || (isT0 ? 'Home' : 'Away');

          // Convex hull screen points
          let hullPoints = null;
          if (tData?.convex_hull_img && tData.convex_hull_img.length >= 3) {
            hullPoints = tData.convex_hull_img.map(([x, y]) => [x * scaleX, y * scaleY]);
          } else {
            // Robust fallback: compute convex hull directly from screen positions
            const screenPts = teamPlayers
              .filter((p) => p.foot_x !== undefined && p.foot_y !== undefined && !isNaN(p.foot_x) && !isNaN(p.foot_y))
              .map((p) => [p.foot_x * scaleX, p.foot_y * scaleY]);
            if (screenPts.length >= 3) {
              hullPoints = compute2DConvexHull(screenPts);
            }
          }

          if (hullPoints && hullPoints.length >= 3) {
            ctx.beginPath();
            ctx.moveTo(hullPoints[0][0], hullPoints[0][1]);
            for (let i = 1; i < hullPoints.length; i++) {
              ctx.lineTo(hullPoints[i][0], hullPoints[i][1]);
            }
            ctx.closePath();
            ctx.fillStyle = isT0 ? 'rgba(0, 229, 255, 0.08)' : 'rgba(239, 68, 68, 0.08)';
            ctx.fill();
            ctx.strokeStyle = isT0 ? 'rgba(0, 229, 255, 0.50)' : 'rgba(239, 68, 68, 0.50)';
            ctx.lineWidth = 1.6;
            ctx.setLineDash([5, 4]);
            ctx.stroke();

            // Centroid Label for Team Formation
            const midX = hullPoints.reduce((sum, pt) => sum + pt[0], 0) / hullPoints.length;
            const midY = hullPoints.reduce((sum, pt) => sum + pt[1], 0) / hullPoints.length;
            if (midX >= 50 && midX <= canvas.width - 50 && midY >= 40 && midY <= canvas.height - 40) {
              const widthStr = tData?.width_m ? ` • ${tData.width_m}m width` : '';
              const lbl = `${teamName.toUpperCase()} SHAPE${widthStr}`;
              ctx.font = 'bold 9px system-ui, sans-serif';
              const tw = ctx.measureText(lbl).width + 12;
              ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
              ctx.beginPath();
              safeRoundRect(ctx, midX - tw / 2, midY - 9, tw, 18, 4);
              ctx.fill();
              ctx.strokeStyle = isT0 ? 'rgba(0, 229, 255, 0.5)' : 'rgba(239, 68, 68, 0.5)';
              ctx.lineWidth = 1;
              ctx.stroke();

              ctx.fillStyle = isT0 ? '#67e8f9' : '#fca5a5';
              ctx.textAlign = 'center';
              ctx.textBaseline = 'middle';
              ctx.fillText(lbl, midX, midY);
            }
          }

          // Defensive Backline Unit Connecting Defenders
          const defRoles = [2, 3, 4, 5, 13];
          const defenders = teamPlayers.filter((p) => defRoles.includes(p.role));
          let backlinePts = null;
          if (tData?.backline?.defensive_line_img && tData.backline.defensive_line_img.length >= 2) {
            backlinePts = tData.backline.defensive_line_img.map(([x, y]) => [x * scaleX, y * scaleY]);
          } else if (defenders.length >= 2) {
            // Sort defenders laterally across image
            const sortedDefs = defenders
              .filter((d) => d.foot_x !== undefined && d.foot_y !== undefined && !isNaN(d.foot_x))
              .sort((a, b) => a.foot_y - b.foot_y);
            if (sortedDefs.length >= 2) {
              backlinePts = sortedDefs.map((d) => [d.foot_x * scaleX, d.foot_y * scaleY]);
            }
          }

          if (backlinePts && backlinePts.length >= 2) {
            ctx.beginPath();
            ctx.moveTo(backlinePts[0][0], backlinePts[0][1]);
            for (let i = 1; i < backlinePts.length; i++) {
              ctx.lineTo(backlinePts[i][0], backlinePts[i][1]);
            }
            ctx.strokeStyle = isT0 ? 'rgba(0, 229, 255, 0.95)' : 'rgba(239, 68, 68, 0.95)';
            ctx.lineWidth = 2.2;
            ctx.setLineDash([]);
            ctx.shadowColor = isT0 ? '#00e5ff' : '#ef4444';
            ctx.shadowBlur = 6;
            ctx.stroke();

            // Connect dots on defenders
            backlinePts.forEach(([bx, by]) => {
              ctx.beginPath();
              ctx.arc(bx, by, 3.5, 0, 2 * Math.PI);
              ctx.fillStyle = '#ffffff';
              ctx.fill();
              ctx.strokeStyle = baseColor;
              ctx.lineWidth = 1.5;
              ctx.stroke();
            });

            const dMidX = (backlinePts[0][0] + backlinePts[backlinePts.length - 1][0]) / 2;
            const dMidY = (backlinePts[0][1] + backlinePts[backlinePts.length - 1][1]) / 2;
            const heightText = tData?.backline?.line_height_m ? ` (${tData.backline.line_height_m}m)` : '';
            const bLabel = `${teamName.toUpperCase()} BACKLINE${heightText}`;
            ctx.font = 'bold 9px system-ui, sans-serif';
            const bw = ctx.measureText(bLabel).width + 10;
            ctx.fillStyle = 'rgba(15, 23, 42, 0.90)';
            ctx.beginPath();
            safeRoundRect(ctx, dMidX - bw / 2, dMidY - 18, bw, 16, 3);
            ctx.fill();
            ctx.strokeStyle = baseColor;
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.fillStyle = isT0 ? '#67e8f9' : '#fca5a5';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(bLabel, dMidX, dMidY - 10);
          }
        });
        ctx.restore();
      }

    // 3. Draw Multi-Player Selection Connections
    if (overlayToggles?.multiPlayer && selectedPlayerIds && selectedPlayerIds.length >= 2 && overlayData?.players) {
      const selPlayers = overlayData.players.filter((p) => selectedPlayerIds.includes(p.player_id));
      if (selPlayers.length === 2 && selPlayers[0].foot_x !== undefined && selPlayers[1].foot_x !== undefined) {
        const p1x = selPlayers[0].foot_x * scaleX;
        const p1y = selPlayers[0].foot_y * scaleY;
        const p2x = selPlayers[1].foot_x * scaleX;
        const p2y = selPlayers[1].foot_y * scaleY;

        ctx.save();
        ctx.beginPath();
        ctx.moveTo(p1x, p1y);
        ctx.lineTo(p2x, p2y);
        ctx.strokeStyle = '#fde047';
        ctx.lineWidth = 2.0;
        ctx.shadowColor = '#fde047';
        ctx.shadowBlur = 6;
        ctx.stroke();

        // Distance label at center
        const mx = (p1x + p2x) / 2;
        const my = (p1y + p2y) / 2;
        const distVal = overlayData.selection_analysis?.pairwise_distance_m ?? overlayData.selection_analysis?.pair_distance_m;
        const distText = distVal != null ? `${Number(distVal).toFixed(1)}m` : '';
        if (distText) {
          ctx.font = 'bold 9px system-ui, sans-serif';
          const w = ctx.measureText(distText).width + 8;
          ctx.fillStyle = 'rgba(15, 23, 42, 0.9)';
          ctx.fillRect(mx - w / 2, my - 7, w, 14);
          ctx.fillStyle = '#fde047';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          ctx.fillText(distText, mx, my);
        }
        ctx.restore();
      } else if (selPlayers.length >= 3 && (overlayData.selection_analysis?.group_hull_img || overlayData.selection_analysis?.hull_img)) {
        const hull = overlayData.selection_analysis?.group_hull_img || overlayData.selection_analysis?.hull_img;
        if (hull && hull.length >= 3) {
          ctx.save();
          ctx.beginPath();
          ctx.moveTo(hull[0][0] * scaleX, hull[0][1] * scaleY);
          for (let i = 1; i < hull.length; i++) {
            ctx.lineTo(hull[i][0] * scaleX, hull[i][1] * scaleY);
          }
          ctx.closePath();
          ctx.fillStyle = 'rgba(253, 224, 71, 0.12)';
          ctx.fill();
          ctx.strokeStyle = '#fde047';
          ctx.lineWidth = 1.6;
          ctx.setLineDash([5, 4]);
          ctx.stroke();
          ctx.restore();
        }
      }
    }

    // 4. Draw Passing Lanes & Candidate Receivers (Restrained, Visual-First, Interactive)
    if (overlayToggles?.lanes && overlayData?.passing_lanes && overlayData.passing_lanes.length > 0) {
      const lanesToDraw = overlayData.passing_lanes.filter((l) =>
        showAllLanes || l.is_top_option || l.receiver_id === highlightedReceiverId || (l.rank && l.rank <= 3)
      );

      lanesToDraw.forEach((lane) => {
        let fx = lane.from_img_x;
        let fy = lane.from_img_y;
        let tx = lane.to_img_x;
        let ty = lane.to_img_y;

        if (fx === undefined || tx === undefined) {
          const passer = overlayData.players?.find((p) => p.player_id === lane.passer_id);
          const receiver = overlayData.players?.find((p) => p.player_id === (lane.receiver_id || lane.target_player_id));
          if (passer?.foot_x !== undefined && receiver?.foot_x !== undefined) {
            fx = passer.foot_x;
            fy = passer.foot_y;
            tx = receiver.foot_x;
            ty = receiver.foot_y;
          }
        }

        if (fx !== undefined && tx !== undefined && fx !== null && tx !== null) {
          const cfx = fx * scaleX;
          const cfy = fy * scaleY;
          const ctx_ = tx * scaleX;
          const cty = ty * scaleY;

          const isHighlighted = lane.receiver_id === highlightedReceiverId;
          const isClear = lane.lane_status === 'open' || lane.risk_level === 'low';
          const isBlocked = lane.lane_status === 'blocked' || lane.risk_level === 'high';
          const color = isClear ? '#00e5ff' : isBlocked ? '#ef4444' : '#f59e0b';
          const isHypothetical = Boolean(lane.is_hypothetical);

          const isBoxRun = Boolean(lane.is_box_run || (lane.run_annotation && lane.run_annotation.includes('dangerous')));
          const isAerial = Boolean(lane.is_aerial_threat || lane.aerial_type);

          ctx.save();
          ctx.beginPath();
          if (isBlocked) {
            ctx.setLineDash([4, 4]);
          } else if (isAerial) {
            ctx.setLineDash([6, 3]);
          } else if (isHypothetical) {
            ctx.setLineDash([6, 3]);
          } else {
            ctx.setLineDash([]);
          }

          const laneColor = isAerial ? '#38bdf8' : (isBoxRun ? '#f87171' : color);
          ctx.strokeStyle = laneColor;
          ctx.lineWidth = isHighlighted ? 3.6 : (isClear || isAerial ? 2.6 : 1.7);
          ctx.shadowColor = laneColor;
          ctx.shadowBlur = isHighlighted ? 14 : (isClear || isAerial ? 7 : 2);

          if (isAerial) {
            // Draw parabolic trajectory arc representing aerial lofted pass
            const midX = (cfx + ctx_) / 2;
            const dist = Math.hypot(ctx_ - cfx, cty - cfy);
            const arcH = Math.min(65, Math.max(25, dist * 0.20));
            const midY = Math.min(cfy, cty) - arcH;
            ctx.moveTo(cfx, cfy);
            ctx.quadraticCurveTo(midX, midY, ctx_, cty);
            ctx.stroke();

            // Flight tag at peak of arc
            const flightTag = `✈ ${lane.aerial_type || 'AERIAL CROSS'}`;
            ctx.font = 'bold 8.5px system-ui, sans-serif';
            const ftw = ctx.measureText(flightTag).width + 10;
            ctx.fillStyle = 'rgba(15, 23, 42, 0.90)';
            ctx.beginPath();
            safeRoundRect(ctx, midX - ftw / 2, midY - 8, ftw, 15, 3);
            ctx.fill();
            ctx.strokeStyle = '#38bdf8';
            ctx.lineWidth = 1;
            ctx.stroke();
            ctx.fillStyle = '#38bdf8';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(flightTag, midX, midY);
          } else {
            ctx.moveTo(cfx, cfy);
            ctx.lineTo(ctx_, cty);
            ctx.stroke();
          }

          // Arrow head
          const angle = Math.atan2(cty - cfy, ctx_ - cfx);
          const headLen = isHighlighted ? 12 : (isClear ? 10 : 8);
          ctx.beginPath();
          ctx.moveTo(ctx_, cty);
          ctx.lineTo(ctx_ - headLen * Math.cos(angle - Math.PI / 7), cty - headLen * Math.sin(angle - Math.PI / 7));
          ctx.lineTo(ctx_ - headLen * Math.cos(angle + Math.PI / 7), cty - headLen * Math.sin(angle + Math.PI / 7));
          ctx.closePath();
          ctx.fillStyle = laneColor;
          ctx.fill();

          // Render high-speed penetration run badge above receiver if making run into dangerous area
          if (isBoxRun) {
            const runnerSpeed = lane.runner_speed_kmh || lane.speed_kmh;
            const runText = `⚡ MAKING RUN INTO DANGEROUS AREA${runnerSpeed ? ` • ${Number(runnerSpeed).toFixed(1)} km/h` : ''}`;
            ctx.font = 'bold 9px system-ui, sans-serif';
            const rtw = ctx.measureText(runText).width + 14;
            const rx = ctx_ - rtw / 2;
            const ry = cty - 42;

            ctx.fillStyle = 'rgba(239, 68, 68, 0.94)';
            ctx.shadowColor = '#ef4444';
            ctx.shadowBlur = 10;
            ctx.beginPath();
            safeRoundRect(ctx, rx, ry, rtw, 18, 4);
            ctx.fill();
            ctx.strokeStyle = '#fca5a5';
            ctx.lineWidth = 1.2;
            ctx.stroke();

            ctx.fillStyle = '#ffffff';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(runText, ctx_, ry + 9);

            // Pointer arrow to runner
            ctx.beginPath();
            ctx.moveTo(ctx_ - 4, ry + 18);
            ctx.lineTo(ctx_ + 4, ry + 18);
            ctx.lineTo(ctx_, ry + 24);
            ctx.closePath();
            ctx.fillStyle = '#ef4444';
            ctx.fill();
          }

          // Highlight target receiver with luminous halo if hovered/selected
          if (isHighlighted) {
            ctx.beginPath();
            ctx.arc(ctx_, cty, 16, 0, 2 * Math.PI);
            ctx.strokeStyle = laneColor;
            ctx.lineWidth = 2.0;
            ctx.shadowBlur = 10;
            ctx.stroke();
          }

          // Subtle indicator on intercepting defender when blocked
          if (isBlocked && lane.interceptor_shirt && overlayData.players) {
            const intDef = overlayData.players.find((p) => p.shirt === lane.interceptor_shirt);
            if (intDef && intDef.foot_x !== undefined) {
              const ix = intDef.foot_x * scaleX;
              const iy = intDef.foot_y * scaleY;
              ctx.beginPath();
              ctx.ellipse(ix, iy, 12, 5, 0, 0, 2 * Math.PI);
              ctx.strokeStyle = 'rgba(239, 68, 68, 0.85)';
              ctx.lineWidth = 1.5;
              ctx.stroke();
            }
          }
          ctx.restore();
        }
      });
    }

    // 4b. On-Video Status Tag (Visual Feedback on Possession & Active Ball Carrier)
    if (overlayData) {
      ctx.save();
      const firstLane = overlayData.passing_lanes?.[0];
      const isHypothetical = Boolean(firstLane && firstLane.is_hypothetical);

      if (isHypothetical && firstLane) {
        // Explicit hypothetical exploration mode
        const expLabel = `• Hypothetical: #${firstLane.passer_shirt || ''} ${firstLane.passer_name?.split(' ').pop() || ''}`;
        ctx.font = '600 11px system-ui, -apple-system, sans-serif';
        const boxW = Math.max(210, ctx.measureText(expLabel).width + 24);
        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = 'rgba(253, 224, 71, 0.5)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        safeRoundRect(ctx, 16, 16, boxW, 26, 6);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#fde047';
        ctx.fillText(expLabel, 26, 33);
      } else if (overlayData.ball_carrier) {
        // Confirmed carrier
        const cName = overlayData.carrier_name?.split(' ').pop() || 'Carrier';
        const cShirt = overlayData.carrier_shirt ? `#${overlayData.carrier_shirt} ` : '';
        const possLabel = `• On Ball: ${cShirt}${cName}`;
        ctx.font = '600 11px system-ui, -apple-system, sans-serif';
        const boxW = Math.max(195, ctx.measureText(possLabel).width + 24);
        ctx.fillStyle = 'rgba(15, 23, 42, 0.85)';
        ctx.strokeStyle = 'rgba(16, 185, 129, 0.5)';
        ctx.lineWidth = 1;
        ctx.beginPath();
        safeRoundRect(ctx, 16, 16, boxW, 26, 6);
        ctx.fill();
        ctx.stroke();
        ctx.fillStyle = '#10b981';
        ctx.fillText(possLabel, 26, 33);
      }
      ctx.restore();
    }

    // 5. Draw Shooting Options & Goal Corridors (Visual Direction, Off-Screen Target Ray & Defenders)
    if (overlayToggles?.shooting && overlayData?.shooting_options) {
      const shoot = overlayData.shooting_options;
      const isViable = Boolean(shoot.is_viable || shoot.viable);
      const corridors = shoot.target_corridors || shoot.corridors || [];

      if (isViable && corridors.length > 0) {
        let fromX = shoot.from_img_x !== undefined ? shoot.from_img_x * scaleX : null;
        let fromY = shoot.from_img_y !== undefined ? shoot.from_img_y * scaleY : null;

        if ((fromX === null || fromY === null) && (shoot.shooter_id || shoot.shirt) && overlayData.players) {
          const sh = overlayData.players.find((p) => p.player_id === shoot.shooter_id || p.shirt === shoot.shirt);
          if (sh && sh.foot_x !== undefined) {
            fromX = sh.foot_x * scaleX;
            fromY = sh.foot_y * scaleY;
          }
        }

        if (fromX !== null && fromY !== null) {
          // Highlight shooter position with subtle targeting reticle
          ctx.save();
          ctx.beginPath();
          ctx.ellipse(fromX, fromY, 18, 8, 0, 0, 2 * Math.PI);
          ctx.strokeStyle = 'rgba(239, 68, 68, 0.85)';
          ctx.lineWidth = 2.0;
          ctx.shadowColor = '#ef4444';
          ctx.shadowBlur = 8;
          ctx.stroke();
          ctx.restore();

          // Draw shooting corridors to goal
          corridors.forEach((corr) => {
            let toX = corr.img_x !== undefined ? corr.img_x : corr.to_img_x;
            let toY = corr.img_y !== undefined ? corr.img_y : corr.to_img_y;

            if (toX !== undefined && toY !== undefined && toX !== null && toY !== null) {
              toX = toX * scaleX;
              toY = toY * scaleY;

              // Check if goal point is off-screen. If so, clip ray to screen boundary
              let endX = toX;
              let endY = toY;
              const isOffScreen = toX < 20 || toX > canvas.width - 20 || toY < 20 || toY > canvas.height - 20;
              if (isOffScreen) {
                const dx = toX - fromX;
                const dy = toY - fromY;
                const length = Math.hypot(dx, dy);
                if (length > 0) {
                  const maxT = Math.min(
                    dx > 0 ? (canvas.width - 30 - fromX) / dx : (30 - fromX) / dx,
                    dy > 0 ? (canvas.height - 30 - fromY) / dy : (30 - fromY) / dy
                  );
                  if (maxT > 0 && maxT < 1.0) {
                    endX = fromX + dx * maxT;
                    endY = fromY + dy * maxT;
                  }
                }
              }

              const isClear = corr.obstruction === 'clear' || corr.status === 'Clear Lane';
              const isBlocked = corr.obstruction === 'blocked' || corr.status === 'Blocked by Defender';
              const strokeColor = isClear ? 'rgba(16, 185, 129, 0.9)' : isBlocked ? 'rgba(239, 68, 68, 0.85)' : 'rgba(245, 158, 11, 0.85)';

              ctx.save();
              ctx.beginPath();
              if (isBlocked) ctx.setLineDash([5, 4]);
              ctx.strokeStyle = strokeColor;
              ctx.lineWidth = isClear ? 2.5 : 1.8;
              ctx.shadowColor = strokeColor;
              ctx.shadowBlur = 6;
              ctx.moveTo(fromX, fromY);
              ctx.lineTo(endX, endY);
              ctx.stroke();

              // Goal target cap / arrow
              const angle = Math.atan2(endY - fromY, endX - fromX);
              const headLen = 10;
              ctx.beginPath();
              ctx.moveTo(endX, endY);
              ctx.lineTo(endX - headLen * Math.cos(angle - Math.PI / 7), endY - headLen * Math.sin(angle - Math.PI / 7));
              ctx.lineTo(endX - headLen * Math.cos(angle + Math.PI / 7), endY - headLen * Math.sin(angle + Math.PI / 7));
              ctx.closePath();
              ctx.fillStyle = strokeColor;
              ctx.fill();

              // Target label tag
              ctx.fillStyle = '#ffffff';
              ctx.font = 'bold 9px system-ui, sans-serif';
              ctx.textAlign = 'center';
              ctx.shadowColor = 'rgba(0,0,0,0.9)';
              ctx.shadowBlur = 4;
              ctx.fillText(corr.target_name || corr.target_label || 'Goal Target', endX, endY - 8);
              ctx.restore();
            }
          });

          // Highlight blocking defenders
          if (shoot.blocked_by_defenders && shoot.blocked_by_defenders.length > 0 && overlayData.players) {
            shoot.blocked_by_defenders.forEach((b) => {
              let defX = b.foot_x !== undefined ? b.foot_x * scaleX : null;
              let defY = b.foot_y !== undefined ? b.foot_y * scaleY : null;
              if (defX === null) {
                const defPlayer = overlayData.players.find((p) => p.shirt === b.shirt || p.name === b.name);
                if (defPlayer && defPlayer.foot_x !== undefined) {
                  defX = defPlayer.foot_x * scaleX;
                  defY = defPlayer.foot_y * scaleY;
                }
              }
              if (defX !== null && defY !== null) {
                ctx.save();
                ctx.beginPath();
                ctx.ellipse(defX, defY, 14, 6, 0, 0, 2 * Math.PI);
                ctx.strokeStyle = 'rgba(239, 68, 68, 0.9)';
                ctx.lineWidth = 1.8;
                ctx.setLineDash([4, 3]);
                ctx.stroke();
                ctx.fillStyle = 'rgba(239, 68, 68, 0.18)';
                ctx.fill();

                ctx.font = 'bold 8px system-ui, sans-serif';
                ctx.fillStyle = '#ef4444';
                ctx.textAlign = 'center';
                ctx.fillText('BLOCKER', defX, defY + 12);
                ctx.restore();
              }
            });
          }

          // Compact Shot HUD near shooter
          ctx.save();
          ctx.fillStyle = 'rgba(15, 23, 42, 0.92)';
          ctx.strokeStyle = 'rgba(239, 68, 68, 0.75)';
          ctx.lineWidth = 1;
          const hudLine1 = `SHOT: ${shoot.distance_m || shoot.distance_to_goal_m}m • ${shoot.angle_deg || shoot.shooting_angle_deg}° angle`;
          const hudLine2 = `xG: Unavailable (Validated model pending)`;
          ctx.font = 'bold 10px system-ui, sans-serif';
          const w1 = ctx.measureText(hudLine1).width;
          ctx.font = '600 9px system-ui, sans-serif';
          const w2 = ctx.measureText(hudLine2).width;
          const hudW = Math.max(w1, w2) + 16;
          const hudH = 32;
          const hX = fromX - hudW / 2;
          const hY = fromY + 18;

          ctx.beginPath();
          safeRoundRect(ctx, hX, hY, hudW, hudH, 4);
          ctx.fill();
          ctx.stroke();

          ctx.font = 'bold 10px system-ui, sans-serif';
          ctx.fillStyle = '#f87171';
          ctx.textAlign = 'center';
          ctx.fillText(hudLine1, fromX, hY + 13);

          ctx.font = '600 8.5px system-ui, sans-serif';
          ctx.fillStyle = '#94a3b8';
          ctx.fillText(hudLine2, fromX, hY + 26);
          ctx.restore();
        }
      }
    }

    // 6. Draw Players as Broadcast-Style Clean Foot Rings
    if (overlayToggles?.players && overlayData.players) {
      const situation = overlayData.situation || {};
      const carrierShirt = situation.controlling_shirt;
      const carrierTeam = situation.possessing_team;
      const sitPhase = situation.possession_state || situation.situation_phase || '';
      const isContestedSituation = sitPhase === 'contested' || situation.evidence_type === 'opposing_duel_50_50';

      overlayData.players.forEach((p) => {
        let rawFootX = p.foot_x;
        let rawFootY = p.foot_y;

        if ((rawFootX === undefined || rawFootX === null || rawFootY === undefined || rawFootY === null) && p.bbox) {
          const [rx, ry, rw, rh] = p.bbox;
          rawFootX = rx + rw / 2.0;
          rawFootY = ry + rh;
        }

        if (rawFootX === null || rawFootY === null || isNaN(rawFootX) || isNaN(rawFootY)) return;

        // Ground ellipse perspective radius: kept small and aligned with feet
        const pHeight = (p.bbox && p.bbox[3]) ? p.bbox[3] * scaleY : 55 * scaleY;
        const rawHeadY = (p.bbox && p.bbox[1] !== undefined) ? p.bbox[1] * scaleY : (rawFootY * scaleY - pHeight);

        // Temporal EMA smoothing to eliminate frame-to-frame tracking glitching / jumping
        const pKey = p.player_id !== undefined ? p.player_id : `s_${p.team}_${p.shirt}`;
        const prev = smoothedPlayersRef.current.get(pKey);
        let sFootX = rawFootX;
        let sFootY = rawFootY;
        let sHeadY = rawHeadY;
        const now = performance.now();

        if (prev && prev.rawFootX !== undefined) {
          const jumpDist = Math.hypot(rawFootX - prev.rawFootX, rawFootY - prev.rawFootY);
          if (jumpDist < 120) {
            // Smoothly glide with player (0.35 factor ensures fluid sticking without lag)
            const alpha = 0.35;
            sFootX = prev.sFootX + (rawFootX - prev.sFootX) * alpha;
            sFootY = prev.sFootY + (rawFootY - prev.sFootY) * alpha;
            sHeadY = prev.sHeadY + (rawHeadY - prev.sHeadY) * alpha;
          }
        }
        smoothedPlayersRef.current.set(pKey, {
          sFootX,
          sFootY,
          sHeadY,
          rawFootX,
          rawFootY,
          lastSeen: now,
        });

        const canvasFootX = sFootX * scaleX;
        const canvasFootY = sFootY * scaleY;
        const radiusX = Math.max(10, Math.min(18, pHeight * 0.22));
        const radiusY = radiusX * 0.40; // Pitch perspective foreshortening

        const isTeam0 = p.team === 0;
        const teamColor = p.accent_color || (isTeam0 ? '#00e5ff' : '#ef4444');
        const teamGlow = p.accent_color ? `${p.accent_color}88` : (isTeam0 ? 'rgba(0, 229, 255, 0.45)' : 'rgba(239, 68, 68, 0.45)');
        const teamFill = p.kit_color ? `${p.kit_color}25` : (isTeam0 ? 'rgba(0, 229, 255, 0.12)' : 'rgba(239, 68, 68, 0.12)');

        // Carrier determination
        const isCarrier = Boolean(
          p.is_carrier || 
          (carrierShirt !== null && carrierShirt !== undefined && p.shirt === carrierShirt && p.team === carrierTeam)
        );

        // Selected player flag
        const isSelected = selectedPlayerIds.includes(p.player_id);

        ctx.save();

        if (isSelected) {
          // === COACH SELECTED PLAYER HIGHLIGHT (Distinct Gold Double Ring) ===
          const pulse = 0.85 + 0.15 * Math.sin(Date.now() / 200);
          ctx.beginPath();
          ctx.ellipse(canvasFootX, canvasFootY, radiusX * 1.35, radiusY * 1.35, 0, 0, 2 * Math.PI);
          ctx.strokeStyle = `rgba(253, 224, 71, ${0.9 * pulse})`;
          ctx.lineWidth = 1.8;
          ctx.stroke();

          ctx.beginPath();
          ctx.ellipse(canvasFootX, canvasFootY, radiusX, radiusY, 0, 0, 2 * Math.PI);
          ctx.fillStyle = 'rgba(253, 224, 71, 0.28)';
          ctx.fill();
          ctx.strokeStyle = '#fde047';
          ctx.lineWidth = 2.4;
          ctx.shadowColor = '#fde047';
          ctx.shadowBlur = 12;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(canvasFootX, canvasFootY, 3, 0, 2 * Math.PI);
          ctx.fillStyle = '#ffffff';
          ctx.fill();
        } else if (isCarrier) {
          // === CONTROLLED BALL CARRIER ===
          const pulse = 0.85 + 0.15 * Math.sin(Date.now() / 240);
          ctx.beginPath();
          ctx.ellipse(canvasFootX, canvasFootY, radiusX * 1.25, radiusY * 1.25, 0, 0, 2 * Math.PI);
          ctx.strokeStyle = `rgba(245, 158, 11, ${0.8 * pulse})`;
          ctx.lineWidth = 1.6;
          ctx.stroke();

          ctx.beginPath();
          ctx.ellipse(canvasFootX, canvasFootY, radiusX, radiusY, 0, 0, 2 * Math.PI);
          ctx.fillStyle = 'rgba(245, 158, 11, 0.20)';
          ctx.fill();
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 2.2;
          ctx.shadowColor = '#f59e0b';
          ctx.shadowBlur = 10;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(canvasFootX, canvasFootY, 2.5, 0, 2 * Math.PI);
          ctx.fillStyle = '#ffffff';
          ctx.fill();
        } else {
          // === STANDARD TEAM PLAYER FOOT RING ===
          ctx.beginPath();
          ctx.ellipse(canvasFootX, canvasFootY, radiusX, radiusY, 0, 0, 2 * Math.PI);
          ctx.fillStyle = teamFill;
          ctx.fill();
          ctx.strokeStyle = teamColor;
          ctx.lineWidth = 1.5;
          ctx.shadowColor = teamGlow;
          ctx.shadowBlur = 6;
          ctx.stroke();

          ctx.beginPath();
          ctx.arc(canvasFootX, canvasFootY, 1.8, 0, 2 * Math.PI);
          ctx.fillStyle = teamColor;
          ctx.fill();
        }

        ctx.restore();

        // === PLAYER IDENTITY BADGE (Priority 5: unobtrusive for unselected, rich HUD for selected) ===
        const headY = sHeadY !== undefined ? sHeadY : ((p.bbox && p.bbox[1] !== undefined) ? p.bbox[1] * scaleY : (canvasFootY - pHeight));
        const shirtNum = p.shirt !== undefined && p.shirt !== null && p.shirt > 0 ? `#${p.shirt}` : (p.player_id !== undefined ? `ID ${p.player_id}` : '');

        if (shirtNum) {
          ctx.save();
          if (isSelected) {
            // === COACH SELECTED PLAYER COMPACT HUD ===
            // Validated speed in km/h only when valid and physically realistic (< 40 km/h); otherwise 'Speed unavailable'
            const hasValidSpeed = Boolean(p.speed_valid && typeof p.speed_kmh === 'number' && p.speed_kmh < 40.0 && p.speed_kmh >= 0.5);
            const speedText = hasValidSpeed ? `${p.speed_kmh.toFixed(1)} km/h` : 'Speed unavailable';
            const teamLabel = p.team_name || (isTeam0 ? 'Home' : 'Away');
            const stateLabel = isCarrier ? 'Ball Carrier' : (overlayData.ball_carrier ? 'Hypothetical' : 'Selected');

            const line1 = `${shirtNum} ${p.name || ''} (${teamLabel})`;
            const line2 = `${speedText} • ${stateLabel}`;

            ctx.font = 'bold 10px system-ui, sans-serif';
            const w1 = ctx.measureText(line1).width;
            ctx.font = '600 9px system-ui, sans-serif';
            const w2 = ctx.measureText(line2).width;
            const hudW = Math.max(w1, w2) + 16;
            const hudH = 30;
            const hudX = canvasFootX - hudW / 2;
            const hudY = headY - hudH - 8;

            ctx.beginPath();
            safeRoundRect(ctx, hudX, hudY, hudW, hudH, 4);
            ctx.fillStyle = 'rgba(15, 23, 42, 0.94)';
            ctx.fill();
            ctx.strokeStyle = '#fde047';
            ctx.lineWidth = 1.6;
            ctx.shadowColor = '#fde047';
            ctx.shadowBlur = 8;
            ctx.stroke();

            // Line 1: Player Name & Team
            ctx.font = 'bold 10px system-ui, sans-serif';
            ctx.fillStyle = '#fde047';
            ctx.textAlign = 'center';
            ctx.shadowBlur = 0;
            ctx.fillText(line1, canvasFootX, hudY + 12);

            // Line 2: Validated Speed & State
            ctx.font = '600 8.5px system-ui, sans-serif';
            ctx.fillStyle = hasValidSpeed ? '#67e8f9' : '#94a3b8';
            ctx.fillText(line2, canvasFootX, hudY + 24);
          } else if (isCarrier) {
            // === CONFIRMED CARRIER UNSELECTED BADGE ===
            const cName = p.name ? p.name.split(' ').pop() : 'Carrier';
            const cLabel = `${shirtNum} ${cName} [BALL]`;
            ctx.font = 'bold 9px system-ui, sans-serif';
            const textW = ctx.measureText(cLabel).width + 8;
            const bX = canvasFootX - textW / 2;
            const bY = headY - 18;

            ctx.beginPath();
            safeRoundRect(ctx, bX, bY, textW, 14, 3);
            ctx.fillStyle = 'rgba(15, 23, 42, 0.90)';
            ctx.fill();
            ctx.strokeStyle = '#f59e0b';
            ctx.lineWidth = 1.2;
            ctx.stroke();

            ctx.fillStyle = '#f59e0b';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(cLabel, canvasFootX, bY + 7);
          } else {
            // === UNOBTRUSIVE MINIMAL SHIRT NUMBER ONLY ===
            ctx.font = 'bold 8.5px system-ui, sans-serif';
            const textW = ctx.measureText(shirtNum).width + 6;
            const bX = canvasFootX - textW / 2;
            const bY = headY - 15;

            ctx.beginPath();
            safeRoundRect(ctx, bX, bY, textW, 12, 2);
            ctx.fillStyle = 'rgba(8, 12, 20, 0.78)';
            ctx.fill();
            ctx.strokeStyle = teamColor;
            ctx.lineWidth = 0.8;
            ctx.stroke();

            ctx.fillStyle = '#f1f5f9';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(shirtNum, canvasFootX, bY + 6);
          }
          ctx.restore();
        }
      });
    }

    // 7. Draw Ball with Certainty-Aware Marker & Temporal Smoothing (stick smoothly without jitter)
    if (overlayToggles?.ball && overlayData.ball && overlayData.ball.x !== undefined && overlayData.ball.x !== null) {
      const rawBx = overlayData.ball.x;
      const rawBy = overlayData.ball.y;
      const prevB = smoothedBallRef.current;
      let sBx = rawBx;
      let sBy = rawBy;

      if (prevB && prevB.rawBx !== undefined && prevB.rawBx !== null) {
        const jump = Math.hypot(rawBx - prevB.rawBx, rawBy - prevB.rawBy);
        if (jump < 180) {
          const ballAlpha = 0.45;
          sBx = prevB.sBx + (rawBx - prevB.sBx) * ballAlpha;
          sBy = prevB.sBy + (rawBy - prevB.sBy) * ballAlpha;
        }
      }
      smoothedBallRef.current = { sBx, sBy, rawBx, rawBy, lastSeen: performance.now() };

      const bx = sBx * scaleX;
      const by = sBy * scaleY;
      const status = overlayData.ball.status || 'detected';
      const isReliable = Boolean(overlayData.ball.is_reliable !== false && status === 'detected');

      if (!isNaN(bx) && !isNaN(by)) {
        ctx.save();
        if (isReliable) {
          // Outer soft radiant neon aura
          ctx.beginPath();
          ctx.arc(bx, by, 10, 0, 2 * Math.PI);
          ctx.fillStyle = 'rgba(0, 255, 157, 0.22)';
          ctx.fill();

          // Targeting ring
          ctx.beginPath();
          ctx.arc(bx, by, 5.5, 0, 2 * Math.PI);
          ctx.strokeStyle = '#00ff9d';
          ctx.lineWidth = 1.8;
          ctx.shadowColor = '#00ff9d';
          ctx.shadowBlur = 8;
          ctx.stroke();

          // High-contrast white center core
          ctx.beginPath();
          ctx.arc(bx, by, 2.8, 0, 2 * Math.PI);
          ctx.fillStyle = '#ffffff';
          ctx.fill();
        } else if (status === 'uncertain') {
          // Dimmed amber dashed ring for uncertain candidate
          ctx.beginPath();
          ctx.arc(bx, by, 6.0, 0, 2 * Math.PI);
          ctx.setLineDash([3, 2]);
          ctx.strokeStyle = '#f59e0b';
          ctx.lineWidth = 1.4;
          ctx.stroke();

          ctx.fillStyle = '#f59e0b';
          ctx.font = 'bold 8px system-ui, sans-serif';
          ctx.textAlign = 'center';
          ctx.fillText('?', bx, by - 8);
        }
        ctx.restore();
      }
    }
  } catch (err) {
    console.error('[TacticalPredictor VideoOverlay Error]:', err);
  }
}, [activeMatch?.has_tracking, overlayData, overlayToggles, selectedPlayerIds]);

  // Subtle continuous 60fps render loop to animate pulse smoothly
  useEffect(() => {
    let animId;
    const renderLoop = () => {
      drawOverlay();
      animId = requestAnimationFrame(renderLoop);
    };
    animId = requestAnimationFrame(renderLoop);
    return () => {
      if (animId) cancelAnimationFrame(animId);
    };
  }, [drawOverlay]);

  // Video source path: prefers local object URL for 100% instant native browser playback
  const videoSrc = activeMatch?.localBlobUrl || (activeMatch?.id ? `/api/videos/${activeMatch.id}/stream` : '');

  // Calculate percentages for draggable scrubber track
  const startPct = effectiveDuration > 0 ? (intervalStart / effectiveDuration) * 100 : 0;
  const endPct = effectiveDuration > 0 ? (intervalEnd / effectiveDuration) * 100 : 100;
  const playheadPct = effectiveDuration > 0 ? (currentTime / effectiveDuration) * 100 : 0;

  return (
    <div className="video-stage-card studio-pane-card">
      {/* 1. Top Floating Tactical HUD Ribbon (Stitch Design Specification) */}
      <div className="studio-pane-header">
        <div className="studio-pane-title-group">
          <span className="live-rec-dot" />
          <span className="studio-pane-title">BROADCAST VIEWPORT</span>
          <span className="studio-timecode-pill">
            {currentTime.toFixed(2)}s / {effectiveDuration.toFixed(0)}s • F#{Math.round(currentTime * fps)}
          </span>
        </div>

        {/* Tactical Telemetry Toggles with Checkmark Badges */}
        <div className="studio-header-toggles">
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.players ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, players: !prev?.players }))}
            title="Toggle Player Rings & Kit Numbers"
          >
            <span className="toggle-check">{overlayToggles?.players ? '✔' : ''}</span>
            <span>Players</span>
          </button>
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.ball ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, ball: !prev?.ball }))}
            title="Toggle Ball Tracking Reticle"
          >
            <span className="toggle-check">{overlayToggles?.ball ? '✔' : ''}</span>
            <span>Ball</span>
          </button>
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.lanes ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, lanes: !prev?.lanes }))}
            title="Toggle Dynamic Passing Lanes"
          >
            <span className="toggle-check">{overlayToggles?.lanes ? '✔' : ''}</span>
            <span>Lanes</span>
          </button>
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.shooting ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, shooting: !prev?.shooting }))}
            title="Toggle Shooting Threat Corridors"
          >
            <span className="toggle-check">{overlayToggles?.shooting ? '✔' : ''}</span>
            <span>Threats</span>
          </button>
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.spaces ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, spaces: !prev?.spaces }))}
            title="Toggle Space Control & Half-Spaces"
          >
            <span className="toggle-check">{overlayToggles?.spaces ? '✔' : ''}</span>
            <span>Spaces</span>
          </button>
          <button
            type="button"
            className={`studio-chip-toggle ${overlayToggles?.teamShape ? 'active' : ''}`}
            onClick={() => setOverlayToggles?.((prev) => ({ ...prev, teamShape: !prev?.teamShape }))}
            title="Toggle Team Shape & Backline Lines"
          >
            <span className="toggle-check">{overlayToggles?.teamShape ? '✔' : ''}</span>
            <span>Shape</span>
          </button>
        </div>
      </div>

      {/* Video Container + Canvas Overlay */}
      <div 
        className={`video-container ${isDragOver ? 'drag-over-stage' : ''}`}
        onDragOver={(e) => { e.preventDefault(); setIsDragOver(true); }}
        onDragLeave={() => setIsDragOver(false)}
        onDrop={handleDropOnStage}
      >
        {videoSrc ? (
          <video
            ref={videoRef}
            src={videoSrc}
            className="video-element"
            onTimeUpdate={handleTimeUpdate}
            onLoadedMetadata={handleLoadedMetadata}
            onError={handleVideoError}
            onEnded={() => setIsPlaying(false)}
            playsInline
          />
        ) : (
          <div className="no-video-placeholder">
            <span>No video loaded</span>
          </div>
        )}

        {/* Transparent Canvas Overlay for Tactical Graphics */}
        <canvas
          ref={canvasRef}
          width={1920}
          height={1080}
          className="canvas-overlay"
          onClick={handleCanvasClick}
          title="Click any player to select / inspect"
        />

        {/* Live Tactical Alert Overlay Banner (Stitch Spec) */}
        {overlayData?.box_run_candidates && overlayData.box_run_candidates.length > 0 && (
          <div className="tactical-hud-alert-banner">
            <span className="alert-banner-bolt">⚡</span>
            <div className="alert-banner-text">
              <span className="alert-banner-title">DANGEROUS AREA PENETRATION RUN</span>
              <span className="alert-banner-sub">
                #{overlayData.box_run_candidates[0].runner_shirt || 'Runner'} {overlayData.box_run_candidates[0].runner_name ? overlayData.box_run_candidates[0].runner_name : ''} ({overlayData.box_run_candidates[0].speed_kmh ? `${overlayData.box_run_candidates[0].speed_kmh} km/h` : 'High Speed'}) into Half-Space behind defensive line
              </span>
            </div>
          </div>
        )}

        {/* Viewport HUD Watermark */}
        <div className="viewport-hud-watermark">
          LIVE BROADCAST MATRIX • 25 FPS SYNC
        </div>

        {/* Video Decoding Error Overlay */}
        {videoError && (
          <div className="video-error-overlay">
            <AlertTriangle size={32} color="#ef4444" />
            <div style={{ fontWeight: 600, color: '#fff', fontSize: 14 }}>Playback Notice</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: 12, maxWidth: 360, textAlign: 'center', lineHeight: 1.5 }}>
              {videoError}
            </div>
            <button
              className="btn btn-primary"
              style={{ marginTop: 12 }}
              onClick={() => document.getElementById('header-upload-input')?.click()}
            >
              <UploadCloud size={14} />
              <span>Select Another Video</span>
            </button>
          </div>
        )}
      </div>

      {/* 3. Multi-Track Video Timeline Scrubber (Stitch Spec) */}
      <div className="video-controls-toolbar compact-studio-controls">
        <div className="timeline-multi-track-deck">
          <div 
            ref={trackRef} 
            className="timeline-track-container"
            onMouseDown={handleTrackMouseDown}
            onMouseMove={(e) => {
              if (!trackRef.current) return;
              const rect = trackRef.current.getBoundingClientRect();
              const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
              const pct = (x / rect.width) * 100;
              const time = (pct / 100) * effectiveDuration;
              setHoverTimeline({
                pct,
                time: time.toFixed(2),
                frame: Math.round(time * fps),
                label: `${time.toFixed(1)}s • Phase Progression`
              });
            }}
            onMouseLeave={() => setHoverTimeline(null)}
            title="Click or drag to scrub video. Drag handles or window body to adjust analysis interval."
          >
            {/* 1. Sleek Modern Base Progress Track Rail */}
            <div className="normal-timeline-rail">
              {/* Played Progress Fill */}
              <div 
                className="normal-timeline-played-bar" 
                style={{ width: `${Math.min(100, Math.max(0, playheadPct))}%` }} 
              />
            </div>

            {/* 2. Subtle Analysis Interval Range Window */}
            <div 
              className="timeline-selected-range" 
              style={{ left: `${startPct}%`, width: `${Math.max(0.8, endPct - startPct)}%` }}
            >
              <div
                className="timeline-handle handle-start"
                onMouseDown={handleInHandleMouseDown}
                title={`Drag to adjust Interval Start (${intervalStart.toFixed(1)}s)`}
              />

              <div 
                className="timeline-range-body" 
                onMouseDown={handleRangeBodyMouseDown}
                title="Drag to slide interval window"
              />

              <div
                className="timeline-handle handle-end"
                onMouseDown={handleOutHandleMouseDown}
                title={`Drag to adjust Interval End (${intervalEnd.toFixed(1)}s)`}
              />
            </div>

            {/* 3. Sleek Standard Playhead Thumb */}
            <div 
              className="normal-timeline-playhead" 
              style={{ left: `${playheadPct}%` }}
            >
              <div className="playhead-thumb-circle" />
            </div>

            {/* 4. Hover Tooltip Preview Pill */}
            {hoverTimeline && (
              <div 
                className="timeline-hover-pill"
                style={{ left: `${hoverTimeline.pct}%` }}
              >
                <span className="hover-dot" />
                <span>{hoverTimeline.time}s • F#{hoverTimeline.frame}</span>
              </div>
            )}
          </div>
        </div>

        {/* 4. Modern Standard Video Controls Bar (Spacious, Normal & Intuitive) */}
        <div className="unified-transport-bar modern-controls-deck">
          {/* Left Cluster: Standard Video Controls & Timecode */}
          <div className="transport-playback-cluster">
            <button 
              className="transport-btn main-play-btn" 
              onClick={togglePlay}
              title={isPlaying ? 'Pause (Space)' : 'Play (Space)'}
            >
              {isPlaying ? <Pause size={17} /> : <Play size={17} style={{ marginLeft: 2 }} />}
            </button>

            <button 
              className="transport-btn step-btn" 
              onClick={() => stepFrame(-1)}
              title="Step Back 1 Frame (-1s)"
            >
              <SkipBack size={14} />
            </button>

            <button 
              className="transport-btn step-btn" 
              onClick={() => stepFrame(1)}
              title="Step Forward 1 Frame (+1s)"
            >
              <SkipForward size={14} />
            </button>

            <div className="transport-timecode-box">
              <span className="timecode-current">{currentTime.toFixed(2)}s</span>
              <span className="timecode-divider">/</span>
              <span className="timecode-total">{effectiveDuration.toFixed(1)}s</span>
            </div>
          </div>

          {/* Center Cluster: Clean Interval Window & Analysis Trigger */}
          <div className="transport-interval-cluster">
            <div className="interval-display-pill">
              <span className="interval-pill-prefix">CLIP</span>
              <span className="interval-pill-range">
                {intervalStart.toFixed(1)}s – {intervalEnd.toFixed(1)}s
              </span>
            </div>

            <button
              type="button"
              className="interval-quick-btn"
              onClick={handleSetInToPlayhead}
              title="Set Interval Start to current playhead"
            >
              Set In
            </button>

            <button
              type="button"
              className="interval-quick-btn"
              onClick={handleSetOutToPlayhead}
              title="Set Interval End to current playhead"
            >
              Set Out
            </button>

            <button
              type="button"
              className="interval-quick-btn"
              onClick={resetInterval}
              title="Reset interval window"
            >
              Reset
            </button>

            <button 
              className="btn btn-primary transport-analyze-cta"
              onClick={() => onRunAnalysis(selectedModules)}
              disabled={isAnalyzing || isUploading || !activeMatch?.id}
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw size={12} className="spin-icon" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Cpu size={13} />
                  <span>Analyze Window</span>
                </>
              )}
            </button>
          </div>

          {/* Right Cluster: Speed, Loop & Mode Controls */}
          <div className="transport-settings-cluster">
            <button 
              type="button"
              className="transport-btn speed-toggle-btn"
              onClick={handleToggleSpeed}
              title="Toggle Playback Speed"
            >
              {playbackSpeed.toFixed(1)}x
            </button>

            <button 
              className={`transport-btn ${isLoopingInterval ? 'active' : ''}`}
              onClick={() => setIsLoopingInterval(!isLoopingInterval)}
              title="Loop Selected Interval Window"
            >
              <Repeat size={14} />
              <span className="loop-label">Loop</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
