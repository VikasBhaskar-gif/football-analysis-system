import React, { useState, useEffect, useCallback, useRef } from 'react';
import VideoPlayer from './components/VideoPlayer';
import TacticalPitch from './components/TacticalPitch';
import PlayerSelectionBar from './components/PlayerSelectionBar';
import ContextualAnalysisPanel from './components/ContextualAnalysisPanel';
import CoachAILabSection from './components/CoachAILabSection';
import UploadPromptView from './components/UploadPromptView';
import ErrorBoundary from './components/ErrorBoundary';
import { 
  Layers,
  Compass,
  PlaySquare,
  Sparkles,
  ChevronDown,
  UploadCloud
} from 'lucide-react';

export default function App() {
  const [catalog, setCatalog] = useState([]);
  const [activeVideo, setActiveVideo] = useState(null);
  const [matchSummary, setMatchSummary] = useState(null);

  // Coach Arbitrary Player Selection
  const [selectedPlayerIds, setSelectedPlayerIds] = useState([]);
  const [highlightedReceiverId, setHighlightedReceiverId] = useState(null);
  const [focusPlayerId, setFocusPlayerId] = useState(null);

  // Upload and indexing state
  const [isUploading, setIsUploading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);

  // Interval and Playback State
  const [intervalStart, setIntervalStart] = useState(0.0);
  const [intervalEnd, setIntervalEnd] = useState(15.0);
  const [currentTime, setCurrentTime] = useState(0.0);
  const [seekTargetTime, setSeekTargetTime] = useState(null);

  // Analysis State
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [overlayData, setOverlayData] = useState(null);
  const [coachAiReport, setCoachAiReport] = useState(null);
  const [pitchAnalyticsOverlay, setPitchAnalyticsOverlay] = useState(null);

  const handleSetIntervalStart = useCallback((newStart) => {
    setIntervalStart(newStart);
  }, []);

  const handleSetIntervalEnd = useCallback((newEnd) => {
    setIntervalEnd(newEnd);
  }, []);

  // Full set of video overlay toggles
  const [overlayToggles, setOverlayToggles] = useState({
    players: true,
    ball: true,
    lanes: true,
    shooting: true,
    spaces: true,
    multiPlayer: true,
    teamShape: true,
  });

  // Active match period filter: '1st' | '2nd' | 'full'
  const [activePeriod, setActivePeriod] = useState('2nd');

  const handlePeriodChange = useCallback((period) => {
    setActivePeriod(period);
    const dur = activeVideo?.duration_s || 15.0;
    if (period === '1st') {
      setIntervalStart(0.0);
      setIntervalEnd(Math.min(dur > 30 ? dur / 2 : 7.5, dur));
      setSeekTargetTime(0.0);
    } else if (period === '2nd') {
      const half = dur > 30 ? dur / 2 : 0.0;
      setIntervalStart(half);
      setIntervalEnd(Math.min(half + (dur > 30 ? dur / 2 : 15.0), dur));
      setSeekTargetTime(half);
    } else if (period === 'full') {
      setIntervalStart(0.0);
      setIntervalEnd(dur);
      setSeekTargetTime(0.0);
    }
  }, [activeVideo?.duration_s]);

  const prevBlobUrlRef = useRef(null);
  const lastFetchedFrameRef = useRef(-1);
  const lastFetchedSelectedRef = useRef('');
  const lastFetchedFocusRef = useRef(null);
  const uploadCounterRef = useRef(0);

  // Load match catalog on startup
  useEffect(() => {
    fetch('/api/matches')
      .then((res) => (res.ok ? res.json() : []))
      .then((matches) => {
        setCatalog(matches);
        if (matches && matches.length > 0 && !activeVideo) {
          const params = new URLSearchParams(window.location.search);
          const targetVideoId = params.get('video_id') || params.get('video') || params.get('match_id');
          const defaultMatch = matches.find((m) => m.id === targetVideoId) ||
                               matches.find((m) => m.id === 'game_39') ||
                               matches[0];
          if (defaultMatch) {
            selectMatch(defaultMatch);
          }
        }
      })
      .catch((err) => console.warn('Failed to load match catalog:', err));
  }, []);

  // Fetch match summary
  const loadMatchSummary = useCallback((videoId) => {
    if (!videoId) return;
    fetch(`/api/matches/${videoId}/summary`)
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) setMatchSummary(data);
      })
      .catch((err) => console.warn('Failed to load match summary:', err));
  }, []);

  // Select a match from catalog
  const selectMatch = useCallback((matchEntry) => {
    setActiveVideo({
      ...matchEntry,
      localBlobUrl: `/api/videos/${matchEntry.id}/stream`,
    });
    setIntervalStart(0.0);
    setIntervalEnd(Math.min(matchEntry.duration_s || 15.0, 15.0));
    setCurrentTime(0.0);
    setSelectedPlayerIds([]);
    setFocusPlayerId(null);
    setAnalysisResult(null);
    setCoachAiReport(null);
    setPitchAnalyticsOverlay(null);
    setOverlayData(null);
    lastFetchedFrameRef.current = -1;
    loadMatchSummary(matchEntry.id);
  }, [loadMatchSummary]);

  // Video Upload Handler
  const handleUploadFile = async (file) => {
    if (!file) return;

    const validExts = ['.mp4', '.webm', '.mov', '.mkv'];
    const fileNameLower = file.name.toLowerCase();
    const isSupported = validExts.some((ext) => fileNameLower.endsWith(ext));

    if (!isSupported) {
      setUploadStatus({
        type: 'error',
        message: `Unsupported file format: "${file.name}". Please upload an MP4, WebM, or MOV video.`,
      });
      return;
    }

    const currentUploadId = ++uploadCounterRef.current;

    if (prevBlobUrlRef.current) {
      try {
        URL.revokeObjectURL(prevBlobUrlRef.current);
      } catch (e) {
        // ignore
      }
    }

    const localBlobUrl = URL.createObjectURL(file);
    prevBlobUrlRef.current = localBlobUrl;

    const tempId = `local_${Date.now()}`;
    const initialDuration = 15.0;

    const localVideoEntry = {
      id: tempId,
      title: file.name,
      original_filename: file.name,
      match_id: 'uploaded_match',
      video_path: '',
      localBlobUrl: localBlobUrl,
      file: file,
      fps: 25.0,
      duration_s: initialDuration,
      width: 1920,
      height: 1080,
      has_tracking: false,
    };

    setActiveVideo(localVideoEntry);
    setIntervalStart(0.0);
    setIntervalEnd(initialDuration);
    setCurrentTime(0.0);
    setSelectedPlayerIds([]);
    setUploadStatus({
      type: 'info',
      message: `Uploading "${file.name}" to server...`,
    });
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (currentUploadId !== uploadCounterRef.current) return;

      const data = await res.json();
      if (res.ok && data.video) {
        setUploadStatus({
          type: 'success',
          message: `Indexed "${file.name}" successfully (${data.video.duration_s}s, ${data.video.fps} fps).`,
        });

        const registeredVideo = {
          ...data.video,
          localBlobUrl: localBlobUrl,
          file: file,
        };
        setActiveVideo(registeredVideo);
        loadMatchSummary(registeredVideo.id);

        if (data.video.duration_s && data.video.duration_s > 0) {
          setIntervalEnd(Math.min(data.video.duration_s, 15.0));
        }
      } else {
        setUploadStatus({
          type: 'error',
          message: data.detail || 'Backend registration notice. Local playback remains active.',
        });
      }
    } catch (err) {
      if (currentUploadId === uploadCounterRef.current) {
        setUploadStatus({
          type: 'error',
          message: `Notice: Backend indexing offline (${err.message}). Local playback active.`,
        });
      }
    } finally {
      if (currentUploadId === uploadCounterRef.current) {
        setIsUploading(false);
      }
    }
  };

  const handleDurationDiscovered = useCallback((dur) => {
    if (dur && isFinite(dur) && dur > 0) {
      const rounded = Math.round(dur * 100) / 100;
      setActiveVideo((prev) => {
        if (!prev) return null;
        if (!prev.duration_s || prev.duration_s === 0) {
          return { ...prev, duration_s: rounded };
        }
        return prev;
      });
      setIntervalEnd((prevEnd) => (prevEnd === 15.0 || prevEnd === 0 ? Math.min(rounded, 15.0) : Math.min(rounded, prevEnd)));
    }
  }, []);

  // Run tactical interval analysis
  const runAnalysis = useCallback(
    async (
      modules = { player_movement: true, unit_analysis: true },
      targetVideoId = null,
      customQuestion = '',
      customScope = 'interval'
    ) => {
      const videoId = targetVideoId || activeVideo?.id;
      if (!videoId) return;

      setIsAnalyzing(true);
      try {
        const payload = {
          video_id: videoId,
          start_time: intervalStart,
          end_time: intervalEnd,
          modules: Object.keys(modules).filter((k) => modules[k]),
          selected_players: selectedPlayerIds,
          question: customQuestion || '',
          scope: customScope || 'interval',
        };

        const res = await fetch('/api/analyze', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (res.ok) {
          const data = await res.json();
          setAnalysisResult(data);
          if (data.deep_report) {
            setCoachAiReport(data.deep_report);
            setTimeout(() => {
              document.getElementById('coach-ai-lab-section')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }
          if (data.pitch_analytics_overlay) {
            setPitchAnalyticsOverlay(data.pitch_analytics_overlay);
          }
        }
      } catch (e) {
        // silent fallback
      } finally {
        setIsAnalyzing(false);
      }
    },
    [activeVideo?.id, intervalStart, intervalEnd, selectedPlayerIds]
  );

  // Ask Coach AI
  const askCoachAi = useCallback(
    async (question = '', scope = 'full_match', coachFeedback = null, coachingTeam = null) => {
      const videoId = activeVideo?.id;
      if (!videoId) return null;

      setIsAnalyzing(true);
      try {
        const payload = {
          video_id: videoId,
          question: question,
          start_time: intervalStart,
          end_time: intervalEnd,
          scope: scope || 'full_match',
          selected_players: selectedPlayerIds,
          current_time: currentTime,
          coach_feedback: coachFeedback,
          coaching_team: coachingTeam,
        };

        const res = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (res.ok) {
          const data = await res.json();
          setCoachAiReport(data);
          if (data.pitch_analytics_overlay) {
            setPitchAnalyticsOverlay(data.pitch_analytics_overlay);
          }
          if (data.target_match_id && data.target_match_id !== videoId) {
            const targetMatch = catalog.find((m) => m.id === data.target_match_id);
            if (targetMatch) {
              selectMatch(targetMatch);
            }
          }
          return data;
        }
      } catch (e) {
        // silent fallback
      } finally {
        setIsAnalyzing(false);
      }
      return null;
    },
    [activeVideo?.id, intervalStart, intervalEnd, selectedPlayerIds, currentTime, catalog, selectMatch]
  );

  // Synchronize Frame Overlay & 2D Tactical State
  useEffect(() => {
    if (!activeVideo || !activeVideo.has_tracking) {
      setOverlayData(null);
      return;
    }

    const fps = activeVideo.fps || 25.0;
    const relFrame = Math.round(currentTime * fps);
    const selKey = selectedPlayerIds.slice().sort().join(',');

    if (
      relFrame !== lastFetchedFrameRef.current ||
      selKey !== lastFetchedSelectedRef.current ||
      focusPlayerId !== lastFetchedFocusRef.current
    ) {
      lastFetchedFrameRef.current = relFrame;
      lastFetchedSelectedRef.current = selKey;
      lastFetchedFocusRef.current = focusPlayerId;

      const params = new URLSearchParams();
      if (selectedPlayerIds.length > 0) {
        params.set('selected_players', selectedPlayerIds.join(','));
      }
      if (focusPlayerId !== null && focusPlayerId !== undefined) {
        params.set('focus_player', String(focusPlayerId));
      }
      const queryStr = params.toString() ? `?${params.toString()}` : '';

      fetch(`/api/overlay/${activeVideo.id}/${relFrame}${queryStr}`)
        .then((res) => (res.ok ? res.json() : null))
        .then((data) => {
          if (data && !data.error && data.has_tracking !== false) {
            setOverlayData(data);
          } else {
            setOverlayData(null);
          }
        })
        .catch(() => {
          setOverlayData(null);
        });
    }
  }, [currentTime, activeVideo, selectedPlayerIds, focusPlayerId]);

  // Coach Player Selection Handlers
  const handleTogglePlayerSelection = useCallback((playerId) => {
    setSelectedPlayerIds((prev) => {
      if (prev.includes(playerId)) {
        return prev.filter((id) => id !== playerId);
      }
      return [...prev, playerId];
    });
  }, []);

  const handleSelectUnit = useCallback((unitType) => {
    if (!overlayData?.players) return;
    const defRoles = [2, 3, 4, 5, 13];
    const midRoles = [6, 7, 8, 9];
    const attRoles = [10, 11, 12];

    let targetRoles = [];
    if (unitType === 'defenders') targetRoles = defRoles;
    else if (unitType === 'midfielders') targetRoles = midRoles;
    else if (unitType === 'attackers') targetRoles = attRoles;

    const unitPlayerIds = overlayData.players
      .filter((p) => targetRoles.includes(p.role))
      .map((p) => p.player_id);

    setSelectedPlayerIds(unitPlayerIds);
  }, [overlayData?.players]);

  const handleSelectTeam = useCallback((teamId) => {
    if (!overlayData?.players) return;
    const teamPlayerIds = overlayData.players
      .filter((p) => p.team === teamId)
      .map((p) => p.player_id);
    setSelectedPlayerIds(teamPlayerIds);
  }, [overlayData?.players]);

  const handleClearSelection = useCallback(() => {
    setSelectedPlayerIds([]);
    setFocusPlayerId(null);
  }, []);

  const handleSeekToTime = useCallback((time, interval = null) => {
    if (coachAiReport?.target_match_id && coachAiReport.target_match_id !== activeVideo?.id) {
      const targetMatch = catalog.find((m) => m.id === coachAiReport.target_match_id);
      if (targetMatch) {
        selectMatch(targetMatch);
      }
    }
    setSeekTargetTime(time);
    if (interval && interval.length === 2) {
      setIntervalStart(interval[0]);
      setIntervalEnd(interval[1]);
    }
  }, [coachAiReport?.target_match_id, activeVideo?.id, catalog, selectMatch]);

  return (
    <div className="app-container">
      {/* Top Application Bar (Ultra-Modern Dark Pro Header) */}
      <header className="topbar">
        {/* Left: Brand & Logo */}
        <div className="topbar-left">
          <div className="brand-row">
            <div className="brand-icon">
              <span className="brand-crest-symbol">⚽</span>
            </div>
            <div className="brand-text">
              <div className="brand-title-line">
                <h1>TACTICAL PREDICTOR</h1>
                <span className="brand-pro-badge">PRO OS</span>
              </div>
              <span className="brand-subtitle">AI SPATIAL INTELLIGENCE</span>
            </div>
          </div>
        </div>

        {/* Center: Match Selector & Half Switcher (Always properly spaced, zero overlap) */}
        <div className="topbar-center">
          <div className="match-selector-dropdown-wrapper">
            <span className="match-live-dot" />
            <select
              className="match-select-dropdown"
              value={activeVideo?.id || ''}
              onChange={(e) => {
                const target = catalog.find((m) => m.id === e.target.value);
                if (target) selectMatch(target);
              }}
            >
              {catalog.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.title || m.original_filename} • {m.competition || 'UCL'}
                </option>
              ))}
            </select>
            <ChevronDown size={14} className="dropdown-caret" />
          </div>

          <div className="period-tabs-group">
            <button
              type="button"
              className={`period-tab-btn ${activePeriod === '1st' ? 'active' : ''}`}
              onClick={() => handlePeriodChange('1st')}
            >
              1st Half
            </button>
            <button
              type="button"
              className={`period-tab-btn ${activePeriod === '2nd' ? 'active' : ''}`}
              onClick={() => handlePeriodChange('2nd')}
            >
              2nd Half
            </button>
            <button
              type="button"
              className={`period-tab-btn ${activePeriod === 'full' ? 'active' : ''}`}
              onClick={() => handlePeriodChange('full')}
            >
              Full 90m
            </button>
          </div>
        </div>

        {/* Right: Quick Jump Links & Upload */}
        <div className="topbar-right">
          <div className="layout-toggle-group">
            <button
              className="layout-btn"
              onClick={() => document.getElementById('video-section')?.scrollIntoView({ behavior: 'smooth' })}
              title="Jump to Broadcast Video Viewport"
            >
              <PlaySquare size={13} />
              <span>Video</span>
            </button>
            <button
              className="layout-btn"
              onClick={() => document.getElementById('pitch-section')?.scrollIntoView({ behavior: 'smooth' })}
              title="Jump to 2D Tactical Pitch"
            >
              <Compass size={13} />
              <span>2D Pitch</span>
            </button>
            <button
              className="layout-btn"
              onClick={() => document.getElementById('analysis-section')?.scrollIntoView({ behavior: 'smooth' })}
              title="Jump to Tactical Analysis & Lanes"
            >
              <Layers size={13} color="#00f0ff" />
              <span>Lanes & Analysis</span>
            </button>
            <button
              className="layout-btn ai-lab-nav-btn"
              onClick={() => document.getElementById('coach-ai-lab-section')?.scrollIntoView({ behavior: 'smooth' })}
              title="Jump to Dedicated Coach AI Analyst"
            >
              <Sparkles size={13} color="#10b981" />
              <span>Coach AI</span>
            </button>
          </div>

          <label className="btn btn-primary quick-upload-btn" title="Upload new match or tactical clip">
            <UploadCloud size={14} />
            <span>Upload Clip</span>
            <input
              type="file"
              accept=".mp4,.webm,.mov,.mkv"
              onChange={(e) => e.target.files?.[0] && handleUploadFile(e.target.files[0])}
              style={{ display: 'none' }}
              id="header-upload-input"
            />
          </label>
        </div>
      </header>

      {/* Main Workspace Body */}
      <main className="main-content">
        {!activeVideo ? (
          <UploadPromptView
            onUploadFile={handleUploadFile}
            isUploading={isUploading}
            uploadStatus={uploadStatus}
          />
        ) : (
          <div className="tactical-workspace-layout">
            {/* 1. Squad Roster & Multi-Player Selection Dock */}
            <div className="player-bar-container">
              <PlayerSelectionBar
                players={overlayData?.players || []}
                selectedPlayerIds={selectedPlayerIds}
                onTogglePlayerSelection={handleTogglePlayerSelection}
                onSelectUnit={handleSelectUnit}
                onSelectTeam={handleSelectTeam}
                onClearSelection={handleClearSelection}
                matchSummary={matchSummary}
                overlayData={overlayData}
                currentMatch={activeVideo}
              />
            </div>

            {/* 2. Two-Column Split:
                 Left Column: Video on top (good size) + 2D Pitch directly below it
                 Right Column: Pass Lanes, Shooting Lanes & Selected Player Box */}
            <ErrorBoundary>
              <div className="workspace-columns-container">
                {/* Left Column: Broadcast Video at top, 2D Pitch directly below */}
                <div className="left-stage-column" id="left-stage-column">
                  <div className="video-pane-wrapper" id="video-section">
                    <VideoPlayer
                      activeMatch={activeVideo}
                      intervalStart={intervalStart}
                      setIntervalStart={handleSetIntervalStart}
                      intervalEnd={intervalEnd}
                      setIntervalEnd={handleSetIntervalEnd}
                      currentTime={currentTime}
                      setCurrentTime={setCurrentTime}
                      onDurationDiscovered={handleDurationDiscovered}
                      onRunAnalysis={runAnalysis}
                      isAnalyzing={isAnalyzing}
                      overlayData={overlayData}
                      analysisResult={analysisResult}
                      seekTargetTime={seekTargetTime}
                      setSeekTargetTime={setSeekTargetTime}
                      overlayToggles={overlayToggles}
                      setOverlayToggles={setOverlayToggles}
                      onUploadAnotherVideo={handleUploadFile}
                      isUploading={isUploading}
                      selectedPlayerIds={selectedPlayerIds}
                      onTogglePlayerSelection={handleTogglePlayerSelection}
                      highlightedReceiverId={highlightedReceiverId}
                      onHighlightReceiver={setHighlightedReceiverId}
                    />
                  </div>

                  <div className="pitch-pane-wrapper" id="pitch-section">
                    <TacticalPitch
                      overlayData={overlayData}
                      selectedPlayerIds={selectedPlayerIds}
                      onTogglePlayerSelection={handleTogglePlayerSelection}
                      onClearSelection={handleClearSelection}
                      currentTime={currentTime}
                      highlightedReceiverId={highlightedReceiverId}
                    />
                  </div>
                </div>

                {/* Right Column: Pass Lanes, Shooting Lanes & Selected Player Box */}
                <div className="right-analysis-column" id="analysis-section">
                  <ContextualAnalysisPanel
                    intervalStart={intervalStart}
                    intervalEnd={intervalEnd}
                    isAnalyzing={isAnalyzing}
                    onRunAnalysis={runAnalysis}
                    onAskCoachAi={askCoachAi}
                    overlayData={overlayData}
                    currentTime={currentTime}
                    selectedPlayerIds={selectedPlayerIds}
                    onTogglePlayerSelection={handleTogglePlayerSelection}
                    focusPlayerId={focusPlayerId}
                    setFocusPlayerId={setFocusPlayerId}
                    onSeekToTime={handleSeekToTime}
                    matchSummary={matchSummary}
                    overlayToggles={overlayToggles}
                    setOverlayToggles={setOverlayToggles}
                    highlightedReceiverId={highlightedReceiverId}
                    onHighlightReceiver={setHighlightedReceiverId}
                    currentMatch={activeVideo}
                  />
                </div>
              </div>

              {/* 3. Bottom of the Whole Page: Dedicated Coach AI Analyst & Multi-Pitch 2D Maps */}
              <CoachAILabSection
                intervalStart={intervalStart}
                intervalEnd={intervalEnd}
                isAnalyzing={isAnalyzing}
                onAskCoachAi={askCoachAi}
                coachAiReport={coachAiReport}
                selectedPlayerIds={selectedPlayerIds}
                players={overlayData?.players || []}
                onSeekToTime={handleSeekToTime}
                currentMatch={activeVideo}
                matchSummary={matchSummary}
              />
            </ErrorBoundary>
          </div>
        )}
      </main>
    </div>
  );
}
