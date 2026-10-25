import React, { useState, useEffect, useCallback, useRef } from 'react';
import VideoPlayer from './components/VideoPlayer';
import TacticalPitch from './components/TacticalPitch';
import PlayerSelectionBar from './components/PlayerSelectionBar';
import ContextualAnalysisPanel from './components/ContextualAnalysisPanel';
import CoachAILabSection from './components/CoachAILabSection';
import UploadPromptView from './components/UploadPromptView';
import ErrorBoundary from './components/ErrorBoundary';
import { ChevronDown, FileVideo, Layers, LayoutGrid, Map, MessageSquare, Plus } from 'lucide-react';

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
      <aside className="desk-rail" aria-label="Workspace navigation">
        <a className="desk-brand" href="/" aria-label="Tactical Predictor home">
          <span className="desk-mark" aria-hidden="true"><span /><span /><span /></span>

        </a>

        <nav className="desk-nav" aria-label="Match tools">
          <button className="desk-nav-item is-current" aria-label="Overview" title="Overview" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <LayoutGrid size={17} strokeWidth={1.6} /><span>Overview</span><span className="nav-current-dot" />
          </button>
          {[
            { id: 'video-section', label: 'Video review', icon: FileVideo },
            { id: 'pitch-section', label: 'Tactical pitch', icon: Map },
            { id: 'analysis-section', label: 'Analysis', icon: Layers },
            { id: 'coach-ai-lab-section', label: 'Coach analyst', icon: MessageSquare },
          ].map(({ id, label, icon: Icon }) => (
            <button key={id} className="desk-nav-item" aria-label={label}
              title={label}
              onClick={() => document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' })}>
              <Icon size={17} strokeWidth={1.6} /><span>{label}</span>
            </button>
          ))}
        </nav>
        <span className="studio-rail-end" title="Local workspace" aria-label="Local workspace">L</span>
      </aside>

      <div className="desk-shell">
        <header className="topbar desk-topbar">
          <div className="studio-wordmark">TACTICAL<span>Match analysis</span></div>
          <div className="studio-source-name">{activeVideo ? activeVideo.title : 'Untitled session'}</div>
          <button className="desk-import-button" onClick={() => document.getElementById('header-upload-input').click()}>
            <Plus size={16} /><span>{isUploading ? 'Importing…' : 'Import video'}</span>
          </button>
          <input id="header-upload-input" type="file" accept=".mp4,.webm,.mov,.mkv" hidden
            aria-label="Import match video" onChange={(e) => e.target.files?.[0] && handleUploadFile(e.target.files[0])} />
        </header>

        <main className={`main-content desk-content ${activeVideo ? 'has-match' : ''}`}>
          <div className="desk-match-heading">
              <div className="desk-match-title">
                <span className="desk-eyebrow">MATCH REVIEW</span>
                <h1>{activeVideo?.title || activeVideo?.original_filename || 'Match review'}</h1>
                {activeVideo && <span className="desk-match-meta">{activeVideo.has_tracking ? 'Tracking linked' : 'Video source loaded'}</span>}
              </div>
              <div className="desk-match-controls">
                <div className="desk-match-select">
                  <select aria-label="Select match" value={activeVideo?.id || ''}
                    onChange={(e) => { const match = catalog.find((m) => m.id === e.target.value); if (match) selectMatch(match); }}>
                    {!activeVideo && <option value="">Select match</option>}
                    {activeVideo && !catalog.some((m) => m.id === activeVideo.id) && <option value={activeVideo.id}>{activeVideo.title}</option>}
                    {catalog.map((m) => <option key={m.id} value={m.id}>{m.title || m.original_filename}</option>)}
                  </select>
                  <ChevronDown size={14} aria-hidden="true" />
                </div>
                <div className="desk-periods" aria-label="Match period">
                  { [['1st', '1st half'], ['2nd', '2nd half'], ['full', 'Full match']].map(([period, label]) => (
                    <button key={period} aria-pressed={activePeriod === period} className={activePeriod === period ? 'selected' : ''}
                      onClick={() => handlePeriodChange(period)}>{label}</button>
                  )) }
                </div>
              </div>
          </div>
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
        <footer className="desk-footer"><span><i />Local workspace</span><span>{activeVideo ? 'Source loaded' : 'No source loaded'}</span></footer>
      </div>
    </div>
  );
}
