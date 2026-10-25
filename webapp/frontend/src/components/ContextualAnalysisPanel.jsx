import React, { useState, useEffect, useRef } from 'react';
import { 
  Users, 
  ChevronRight, 
  ChevronLeft, 
  ChevronDown, 
  RefreshCw,
  Play,
  Sparkles,
  Zap,
  AlertTriangle,
  ArrowUpRight,
  Target
} from 'lucide-react';

function getMovementPace(speedKmh) {
  if (speedKmh == null || isNaN(speedKmh) || speedKmh < 0.5) return 'Stationary';
  if (speedKmh < 7) return 'Walking';
  if (speedKmh < 15) return 'Jogging';
  if (speedKmh < 22) return 'Running';
  return 'Sprinting';
}

function resolvePlayerData(targetId, selAnalysis, players = []) {
  if (targetId == null) return null;

  // 1. Check if individual_profiles has it (from multi-selection)
  const profile = selAnalysis?.individual_profiles?.find((pl) => String(pl.player_id) === String(targetId));
  // 2. Check if selAnalysis.player is this player (from single selection)
  const selP = String(selAnalysis?.player?.player_id) === String(targetId) ? selAnalysis.player : null;
  // 3. Fallback to raw player from players array
  const rawP = players.find((pl) => String(pl.player_id) === String(targetId));

  const p = profile || selP || rawP;
  if (!p) return null;

  const kin = profile?.kinematics || (selP ? selAnalysis.kinematics : null) || rawP?.kinematics || rawP || {};
  const tc = profile?.tactical_context || (selP ? selAnalysis.tactical_context : null) || rawP?.tactical_context || {};

  // Extract speed with robust fallbacks
  const rawSpeed = kin?.speed_kmh ?? p?.speed_kmh ?? rawP?.speed_kmh;
  const speedValid = (kin?.speed_valid ?? p?.speed_valid ?? rawP?.speed_valid ?? (rawSpeed != null && rawSpeed < 40.0)) && rawSpeed != null && rawSpeed < 40.0;
  const speedKmh = speedValid ? rawSpeed : null;

  // Tactical context with instant geometric fallback from players
  let nearestOpp = tc?.nearest_opponent ?? p?.nearest_opponent;
  let nearestDist = tc?.nearest_opponent_dist_m ?? p?.nearest_opponent_dist_m;
  let pressure = tc?.pressure_level ?? p?.pressure_level;
  let supports = tc?.support_teammates ?? p?.support_teammates;

  // On-the-fly geometric fallback if tc is missing or empty:
  if ((!nearestOpp || nearestDist == null) && p.pitch_x_m != null && players.length > 0) {
    const opps = players.filter((pl) => pl.team !== p.team && pl.has_pitch);
    let minD = 999;
    let minOppName = null;
    opps.forEach((o) => {
      const d = Math.hypot(p.pitch_x_m - o.pitch_x_m, p.pitch_y_m - o.pitch_y_m);
      if (d < minD) {
        minD = d;
        minOppName = o.name || `#${o.shirt}`;
      }
    });
    if (minOppName && minD < 100) {
      nearestOpp = minOppName;
      nearestDist = Math.round(minD * 10) / 10;
      pressure = minD < 2.5 ? 'High Pressure (<2.5m)' : (minD < 5.0 ? 'Contested (2.5-5m)' : 'Free / Unmarked (>5m)');
    }
  }

  if ((!supports || supports.length === 0) && p.pitch_x_m != null && players.length > 0) {
    const teammates = players.filter((pl) => pl.team === p.team && pl.player_id !== p.player_id && pl.has_pitch);
    supports = teammates
      .map((tm) => ({
        name: tm.name,
        shirt: tm.shirt,
        distance_m: Math.round(Math.hypot(p.pitch_x_m - tm.pitch_x_m, p.pitch_y_m - tm.pitch_y_m) * 10) / 10,
      }))
      .sort((a, b) => a.distance_m - b.distance_m)
      .slice(0, 3);
  }

  return {
    p,
    speedKmh,
    speedValid,
    nearestOpp,
    nearestDist,
    pressure: pressure || 'Uncontested',
    supports: supports || [],
  };
}

export default function ContextualAnalysisPanel({
  intervalStart = 0.0,
  intervalEnd = 15.0,
  isAnalyzing = false,
  onRunAnalysis,
  onAskCoachAi,
  overlayData,
  currentTime = 0.0,
  isCollapsed = false,
  onToggleCollapse,
  selectedPlayerIds = [],
  onTogglePlayerSelection,
  focusPlayerId = null,
  setFocusPlayerId,
  overlayToggles,
  setOverlayToggles,
  highlightedReceiverId = null,
  onHighlightReceiver = () => {},
  currentMatch = null,
  matchSummary = null,
}) {
  const [activeTab, setActiveTab] = useState('passing');
  const [showAllPassingLanes, setShowAllPassingLanes] = useState(false);
  const [expandedLaneIdx, setExpandedLaneIdx] = useState(null);
  const [inspectedPlayerId, setInspectedPlayerId] = useState(null);
  const bodyRef = useRef(null);

  useEffect(() => {
    if (inspectedPlayerId !== null && !selectedPlayerIds.some((pid) => String(pid) === String(inspectedPlayerId))) {
      setInspectedPlayerId(null);
    }
  }, [selectedPlayerIds, inspectedPlayerId]);

  // If focusPlayerId is no longer in selectedPlayerIds, reset to null (Auto Ball Carrier)
  useEffect(() => {
    if (focusPlayerId !== null && !selectedPlayerIds.includes(focusPlayerId)) {
      setFocusPlayerId?.(null);
    }
  }, [selectedPlayerIds, focusPlayerId, setFocusPlayerId]);

  useEffect(() => {
    if (bodyRef.current) {
      bodyRef.current.scrollTop = 0;
    }
  }, [activeTab, inspectedPlayerId]);

  const handleTabChange = (tab) => {
    const applyChange = () => {
      setActiveTab(tab);
      // Switching to Pass Lanes or Shooting automatically defaults to the active Ball Carrier
      if (tab === 'passing' || tab === 'shooting') {
        setFocusPlayerId?.(null);
      }
      if (!setOverlayToggles) return;
      if (tab === 'shooting') {
        setOverlayToggles((prev) => ({ ...prev, shooting: true }));
      } else if (tab === 'passing') {
        setOverlayToggles((prev) => ({ ...prev, lanes: true }));
      } else if (tab === 'space_runs') {
        setOverlayToggles((prev) => ({ ...prev, spaces: true }));
      } else if (tab === 'player_group') {
        setOverlayToggles((prev) => ({ ...prev, players: true, multiPlayer: true }));
      }
    };

    if (typeof document !== 'undefined' && document.startViewTransition && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.startViewTransition(() => applyChange());
    } else {
      applyChange();
    }
  };

  if (isCollapsed) {
    return (
      <button
        className="btn btn-secondary collapsed-analysis-trigger"
        onClick={onToggleCollapse}
        title="Expand Coaching Workspace"
      >
        <ChevronLeft size={16} />
        <span style={{ fontSize: 11, fontWeight: 700 }}>COACHING AI</span>
      </button>
    );
  }

  const duration = Math.max(0, intervalEnd - intervalStart);
  const players = overlayData?.players || [];
  const passingLanes = overlayData?.passing_lanes || [];
  const spaceOpps = overlayData?.space_opportunities || [];
  const selAnalysis = overlayData?.selection_analysis || {};
  const carrierId = overlayData?.ball_carrier;
  const carrierPlayer = players.find((p) => p.player_id === carrierId || p.is_carrier);

  return (
    <div className="analysis-panel">
      {/* Top Header: Navigation Tabs & Collapse Button (Stitch Spec) */}
      <div className="analysis-panel-header">
        <div className="panel-header-top-row">
          <div style={{ display: 'flex', alignItems: 'center', gap: 7 }}>
            <Sparkles size={15} color="#00f0ff" />
            <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--text-primary)', letterSpacing: '-0.01em' }}>
              Tactical Studio & Lanes
            </span>
            <span className="dossier-live-sync-pill">
              <span className="sync-pulse-dot" />
              Live Sync
            </span>
          </div>
          {onToggleCollapse && (
            <button
              className="btn btn-outline panel-collapse-btn"
              onClick={onToggleCollapse}
              title="Collapse Panel for Wider Video"
              style={{ padding: '3px 8px', fontSize: 10, display: 'flex', alignItems: 'center', gap: 4 }}
            >
              <span>Collapse</span>
              <ChevronRight size={12} />
            </button>
          )}
        </div>

        <div className="analysis-mode-tabs">
          <button
            className={`analysis-tab-btn ${activeTab === 'passing' ? 'active' : ''}`}
            onClick={() => handleTabChange('passing')}
            title="Passing Options & Lane Geometry (Ball Carrier Tracked)"
          >
            <ArrowUpRight size={12} color="#00f0ff" />
            <span>Pass Lanes</span>
          </button>

          <button
            className={`analysis-tab-btn ${activeTab === 'shooting' ? 'active' : ''}`}
            onClick={() => handleTabChange('shooting')}
            title="Shooting Options & Goal Corridors (Ball Carrier Tracked)"
          >
            <Target size={12} color="#ef4444" />
            <span>Shooting</span>
          </button>

          <button
            className={`analysis-tab-btn ${activeTab === 'space_runs' ? 'active' : ''}`}
            onClick={() => handleTabChange('space_runs')}
            title="Space & Running Opportunities"
          >
            <Zap size={12} color="#38bdf8" />
            <span>Spaces</span>
          </button>

          <button
            className={`analysis-tab-btn ${activeTab === 'player_group' ? 'active' : ''}`}
            onClick={() => handleTabChange('player_group')}
            title="Individual & Multi-Player Group Intelligence"
          >
            <Users size={12} />
            <span>Squad</span>
          </button>
        </div>
      </div>

      {/* Internal Body */}
      <div className="analysis-panel-body" ref={bodyRef}>
        {/* Sleek Top Playhead Status Ribbon */}
        <div className="card panel-playhead-ribbon">
          <div className="playhead-info-group">
            <span className="playhead-live-dot" />
            <span className="playhead-timecode">
              {currentTime.toFixed(2)}s <span className="playhead-frame">F#{Math.round(currentTime * 25)}</span>
            </span>
            {carrierPlayer && (
              <span className="carrier-inline-pill" title="Tracked Ball Carrier">
                <span className="carrier-dot" />
                #{carrierPlayer.shirt} {carrierPlayer.name?.split(' ').pop() || carrierPlayer.name}
              </span>
            )}
          </div>
          <div className="playhead-action-group">
            <span className="interval-range-text">
              {intervalStart.toFixed(0)}s–{intervalEnd.toFixed(0)}s
            </span>
            <button
              className="btn btn-primary playhead-ai-btn"
              onClick={() => {
                if (onAskCoachAi) {
                  onAskCoachAi('', 'interval');
                } else {
                  onRunAnalysis?.({ [activeTab]: true });
                }
                document.getElementById('coach-ai-lab-section')?.scrollIntoView({ behavior: 'smooth' });
              }}
              disabled={isAnalyzing}
              title="Analyze interval in Coach AI Lab"
            >
              {isAnalyzing ? (
                <>
                  <RefreshCw size={11} className="spin-icon" />
                  <span>Analyzing</span>
                </>
              ) : (
                <>
                  <Sparkles size={11} />
                  <span>AI Lab ↓</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* ================================================================= */}
        {/* TAB 1: PASSING OPTIONS & LANE GEOMETRY (Ball Carrier Locked)      */}
        {/* ================================================================= */}
        {activeTab === 'passing' && (
          <div className="tab-pane">
            <div className="card-header-row">
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <ArrowUpRight size={15} color="var(--accent-cyan)" />
                <span style={{ fontWeight: 700, fontSize: 13 }}>Passing Options</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                {focusPlayerId !== null ? (
                  <span className="badge-pill" style={{ color: '#fde047', borderColor: 'rgba(253, 224, 71, 0.4)' }}>
                    Hypothetical Override
                  </span>
                ) : (
                  <span className="badge-pill" style={{ color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.4)' }}>
                    ⚽ Ball Carrier Locked
                  </span>
                )}
                {passingLanes.length > 4 && (
                  <button
                    type="button"
                    className="btn btn-outline"
                    style={{ fontSize: 10, padding: '2px 7px', height: 22 }}
                    onClick={() => setShowAllPassingLanes((prev) => !prev)}
                    title={showAllPassingLanes ? "Show Top 4 Promising Lanes" : "Show All Options"}
                  >
                    {showAllPassingLanes ? 'Top 4' : `All (${passingLanes.length})`}
                  </button>
                )}
              </div>
            </div>

            {/* Active Passer Selector Strip: Defaults to Ball Carrier even when multiple players are selected */}
            {selectedPlayerIds.length > 0 && (
              <div style={{ marginBottom: 10 }}>
                <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 4 }}>
                  Passer Source (Auto-tracks Ball Carrier while you follow players):
                </div>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    className={`filter-pill ${focusPlayerId === null ? 'active' : ''}`}
                    onClick={() => setFocusPlayerId?.(null)}
                    title="Automatically show passing lanes for whoever has the ball"
                  >
                    ⚽ Active Ball Carrier ({overlayData?.carrier_shirt ? `#${overlayData.carrier_shirt}` : 'Auto'})
                  </button>
                  {selectedPlayerIds.map((pid) => {
                    const pl = players.find((p) => p.player_id === pid);
                    if (!pl || pl.player_id === carrierId) return null;
                    return (
                      <button
                        key={pid}
                        type="button"
                        className={`filter-pill ${focusPlayerId === pid ? 'active' : ''}`}
                        onClick={() => setFocusPlayerId?.(focusPlayerId === pid ? null : pid)}
                        title={`Explore hypothetical passes from #${pl.shirt} ${pl.name}`}
                      >
                        Hypothetical: #{pl.shirt} {pl.name?.split(' ').pop()}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4, marginBottom: 8 }}>
              {passingLanes.length > 0 && passingLanes[0].is_hypothetical
                ? `Hypothetical passing options from #${passingLanes[0].passer_shirt} ${passingLanes[0].passer_name}.`
                : overlayData?.ball_carrier
                ? `Live passing lanes for ball carrier #${overlayData.carrier_shirt} ${overlayData.carrier_name}.`
                : 'Synchronizing ball carrier passing lanes...'}
            </div>

            {passingLanes.length === 0 ? (
              <div className="empty-panel-notice">
                <AlertTriangle size={18} color="#d97706" style={{ margin: '0 auto 6px auto', display: 'block' }} />
                <div style={{ fontWeight: 700, fontSize: 13, color: 'var(--text-primary)', marginBottom: 4 }}>
                  No Passing Lanes in Current Frame
                </div>
                <p style={{ fontSize: 11, color: 'var(--text-secondary)', margin: 0, lineHeight: 1.4 }}>
                  Step or play the video to evaluate open teammate passing corridors.
                </p>
              </div>
            ) : (
              <div className="passing-lanes-list">
                {(showAllPassingLanes ? passingLanes : passingLanes.slice(0, 4)).map((lane, idx) => {
                  const isHighlighted = lane.receiver_id === highlightedReceiverId;
                  const isExpanded = expandedLaneIdx === idx;

                  return (
                    <div
                      key={idx}
                      className={`pass-lane-card ${isHighlighted ? 'highlighted' : ''}`}
                      onMouseEnter={() => onHighlightReceiver?.(lane.receiver_id)}
                      onMouseLeave={() => onHighlightReceiver?.(null)}
                      onClick={() => onHighlightReceiver?.(isHighlighted ? null : lane.receiver_id)}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                          <span className="lane-rank-badge">#{lane.rank || idx + 1}</span>
                          <strong>#{lane.target_shirt} {lane.target_name}</strong>
                          {lane.progression_m !== undefined && (
                            <span style={{ fontSize: 10, color: lane.progression_m > 0 ? '#10b981' : 'var(--text-muted)' }}>
                              {lane.progression_m > 0 ? `+${lane.progression_m}m` : `${lane.progression_m}m`}
                            </span>
                          )}
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                          <span className="badge-pill" style={{ color: lane.risk_color, borderColor: `${lane.risk_color}55` }}>
                            {lane.risk_label || lane.interception_risk}
                          </span>
                          <button
                            type="button"
                            style={{ background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', padding: 2 }}
                            onClick={(e) => {
                              e.stopPropagation();
                              setExpandedLaneIdx((prev) => (prev === idx ? null : idx));
                            }}
                            title="Toggle detailed geometric metrics"
                          >
                            <ChevronDown size={13} style={{ transform: isExpanded ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
                          </button>
                        </div>
                      </div>

                      <div className="pass-rationale-text" style={{ color: 'var(--text-secondary)', fontSize: 11, marginTop: 2 }}>
                        {lane.rationale}
                      </div>

                      {/* Aerial Delivery & Dangerous Run Badges */}
                      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 4 }}>
                        {lane.is_box_run && (
                          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '2px 7px', background: 'rgba(239, 68, 68, 0.16)', border: '1px solid rgba(239, 68, 68, 0.45)', borderRadius: 4, fontSize: 10, color: '#f87171', fontWeight: 700 }}>
                            <span>⚡ MAKING RUN INTO DANGEROUS AREA</span>
                            {lane.runner_speed_kmh && <span style={{ opacity: 0.9 }}>({Number(lane.runner_speed_kmh).toFixed(1)} km/h)</span>}
                          </div>
                        )}
                        {lane.is_aerial_threat && (
                          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 5, padding: '2px 7px', background: 'rgba(56, 189, 248, 0.16)', border: '1px solid rgba(56, 189, 248, 0.45)', borderRadius: 4, fontSize: 10, color: '#38bdf8', fontWeight: 700 }}>
                            <span>✈ {lane.aerial_type || 'Aerial Cross into Box'}</span>
                          </div>
                        )}
                      </div>

                      {isExpanded && (
                        <div style={{ marginTop: 6, paddingTop: 6, borderTop: '1px solid var(--border-subtle)' }}>
                          <div className="pass-lane-metrics-row">
                            <span>Pass Distance: <strong>{lane.distance_m}m</strong></span>
                            <span>Lane Window: <strong>{lane.corridor_clearance_m ? `${lane.corridor_clearance_m}m open` : 'Wide Open'}</strong></span>
                            <span>Target Space: <strong>{lane.receiver_space_m ? `${lane.receiver_space_m}m clear` : 'Unmarked'}</strong></span>
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 2: SHOOTING OPTIONS & GOAL CORRIDORS (Ball Carrier Locked)    */}
        {/* ================================================================= */}
        {activeTab === 'shooting' && (
          <div className="tab-pane">
            <div className="card-header-row">
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Target size={15} color="#ef4444" />
                <span style={{ fontWeight: 700, fontSize: 13 }}>Shooting Options & Corridors</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                {focusPlayerId !== null ? (
                  <span className="badge-pill" style={{ color: '#fde047', borderColor: 'rgba(253, 224, 71, 0.4)' }}>
                    Hypothetical Override
                  </span>
                ) : (
                  <span className="badge-pill" style={{ color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.4)' }}>
                    ⚽ Ball Carrier Locked
                  </span>
                )}
                <span className="badge-pill">
                  {overlayData?.shooting_options?.viable ? 'Viable Corridor' : 'Out of Range'}
                </span>
              </div>
            </div>

            {/* Active Shooter Source Selector if players are selected */}
            {selectedPlayerIds.length > 0 && (
              <div style={{ marginBottom: 10 }}>
                <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 4 }}>
                  Shooter Source (Auto-tracks Ball Carrier):
                </div>
                <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                  <button
                    type="button"
                    className={`filter-pill ${focusPlayerId === null ? 'active' : ''}`}
                    onClick={() => setFocusPlayerId?.(null)}
                  >
                    ⚽ Active Ball Carrier ({overlayData?.carrier_shirt ? `#${overlayData.carrier_shirt}` : 'Auto'})
                  </button>
                  {selectedPlayerIds.map((pid) => {
                    const pl = players.find((p) => p.player_id === pid);
                    if (!pl || pl.player_id === carrierId) return null;
                    return (
                      <button
                        key={pid}
                        type="button"
                        className={`filter-pill ${focusPlayerId === pid ? 'active' : ''}`}
                        onClick={() => setFocusPlayerId?.(focusPlayerId === pid ? null : pid)}
                      >
                        Hypothetical: #{pl.shirt} {pl.name?.split(' ').pop()}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            {overlayData?.shooting_options?.viable ? (
              <div className="card deep-dive-card">
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 13, fontWeight: 700 }}>
                      Shooter: #{overlayData.shooting_options.shirt || overlayData.shooting_options.shooter_shirt} {overlayData.shooting_options.player_name || overlayData.shooting_options.shooter_name || ''}
                    </span>
                  </div>
                  <span className="badge-pill" style={{ color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.4)' }}>
                    Angle: {overlayData.shooting_options.angle_deg || overlayData.shooting_options.shooting_angle_deg}°
                  </span>
                </div>

                <div className="stats-kpi-grid">
                  <div className="kpi-box">
                    <span className="kpi-label">Goal Distance</span>
                    <span className="kpi-val" style={{ color: '#00e5ff' }}>
                      {overlayData.shooting_options.distance_m || overlayData.shooting_options.distance_to_goal_m}m
                    </span>
                  </div>
                  <div className="kpi-box">
                    <span className="kpi-label">Best Target</span>
                    <span className="kpi-val" style={{ color: '#10b981' }}>
                      {overlayData.shooting_options.best_target?.name || 'Far Post Target'}
                    </span>
                  </div>
                  <div className="kpi-box">
                    <span className="kpi-label">Blockers In Lane</span>
                    <span className="kpi-val" style={{ color: overlayData.shooting_options.blocked_by_defenders?.length > 0 ? '#ef4444' : '#10b981' }}>
                      {overlayData.shooting_options.blocked_by_defenders?.length || 0}
                    </span>
                  </div>
                  <div className="kpi-box">
                    <span className="kpi-label">Corridor Status</span>
                    <span className="kpi-val" style={{ fontSize: 11, color: '#fde047' }}>
                      {overlayData.shooting_options.corridor_status || 'Open'}
                    </span>
                  </div>
                </div>

                <div style={{ marginTop: 10 }}>
                  <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-cyan)', marginBottom: 6 }}>
                    GOAL TARGET CORRIDORS
                  </div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {(overlayData.shooting_options.target_corridors || overlayData.shooting_options.corridors)?.map((corr, idx) => (
                      <div key={idx} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-input)', borderRadius: 4 }}>
                        <span style={{ fontSize: 12, fontWeight: 600 }}>{corr.target_name || corr.target_label}</span>
                        <span className="badge-pill" style={{ 
                          color: corr.obstruction === 'clear' || corr.status === 'Clear Lane' ? '#10b981' : (corr.obstruction === 'blocked' || corr.status === 'Blocked by Defender' ? '#ef4444' : '#f59e0b')
                        }}>
                          {(corr.status || corr.obstruction || 'CLEAR').toUpperCase()}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {overlayData.shooting_options.blocked_by_defenders?.length > 0 && (
                  <div style={{ marginTop: 10 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: '#ef4444', marginBottom: 4 }}>
                      DEFENDERS IN TRAJECTORY:
                    </div>
                    {overlayData.shooting_options.blocked_by_defenders.map((b, i) => (
                      <div key={i} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, padding: '3px 0' }}>
                        <span>#{b.shirt} {b.name}</span>
                        <span style={{ color: 'var(--text-muted)' }}>{b.dist_to_lane_m}m to shot corridor</span>
                      </div>
                    ))}
                  </div>
                )}

                <div style={{ marginTop: 12, padding: '10px 12px', background: 'var(--bg-input)', border: '1px solid var(--border-subtle)', borderRadius: 6 }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 4 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                      <Target size={13} color="var(--accent-cyan)" />
                      <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--accent-cyan)' }}>COACH ACTION SUMMARY</span>
                    </div>
                    <span className="badge-pill" style={{ fontSize: 10, color: '#16a34a', borderColor: 'rgba(22, 163, 74, 0.3)' }}>
                      Clear Window: {overlayData.shooting_options.xg_data?.geometric_clearance_pct ?? 100}%
                    </span>
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                    {overlayData.shooting_options.best_target?.name === 'Far Post Target' 
                      ? 'Corridor to far post is open. Recommend driven strike across the keeper into the bottom far corner.'
                      : 'Attacking shooting window available. Look for quick strike on target before defensive line recovers.'}
                  </div>
                </div>
              </div>
            ) : (
              <div className="empty-panel-notice">
                <Target size={28} color="var(--text-muted)" />
                <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginTop: 8 }}>
                  {overlayData?.shooting_options?.shooter_name
                    ? `#${overlayData.shooting_options.shooter_shirt} ${overlayData.shooting_options.shooter_name} Outside Shooting Zone`
                    : 'Shooting Lane Not Viable'}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', maxWidth: 280, marginTop: 4, lineHeight: 1.5 }}>
                  {overlayData?.shooting_options?.reason || 'Ball carrier is currently outside direct shooting range (> 38m from opponent goal). Check Pass Lanes for progression options.'}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 3: ARBITRARY PLAYER & GROUP INTELLIGENCE                      */}
        {/* ================================================================= */}
        {activeTab === 'player_group' && (
          <div className="tab-pane">
            <div className="card-header-row">
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Users size={15} color="var(--accent-cyan)" />
                <span style={{ fontWeight: 700, fontSize: 13 }}>Player & Group Intelligence</span>
              </div>
              <span className="badge-pill">
                {selectedPlayerIds.length === 0 ? 'No Selection' : `${selectedPlayerIds.length} Selected`}
              </span>
            </div>

            {selectedPlayerIds.length === 0 && (
              <div className="empty-panel-notice">
                <Users size={28} color="var(--text-muted)" />
                <div style={{ fontWeight: 600, color: 'var(--text-primary)', marginTop: 8 }}>
                  No Players Selected
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', maxWidth: 260, marginTop: 4 }}>
                  Click any player in the video, 2D tactical pitch, or squad roster to inspect kinematics, relationships, and pressure.
                </div>
              </div>
            )}

            {/* 1 PLAYER SELECTED: INDIVIDUAL DEEP DIVE */}
            {selectedPlayerIds.length === 1 && (
              <div className="card deep-dive-card">
                {(() => {
                  const resolved = resolvePlayerData(selectedPlayerIds[0], selAnalysis, players);
                  if (!resolved) return null;
                  const { p, speedKmh, speedValid, nearestOpp, nearestDist, pressure, supports } = resolved;
                  return (
                    <>
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                          <div className="player-avatar-circle" style={{ backgroundColor: p.accent_color || (p.team === 0 ? '#00e5ff' : '#ef4444') }}>
                            #{p.shirt}
                          </div>
                          <div>
                            <div style={{ fontSize: 14, fontWeight: 700 }}>
                              {p.name}
                              {p.is_carrier && (
                                <span style={{ marginLeft: 6, fontSize: 10, padding: '2px 6px', borderRadius: 4, background: 'rgba(245, 158, 11, 0.2)', color: '#fde047' }}>
                                  ⚽ Ball Carrier
                                </span>
                              )}
                            </div>
                            <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                              {p.team_name} • Role {p.role ?? p.pos ?? ''}
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="stats-kpi-grid">
                        <div className="kpi-box">
                          <span className="kpi-label">Current Speed</span>
                          <span className="kpi-val" style={{ color: 'var(--accent-cyan)' }}>
                            {speedValid && speedKmh !== null && speedKmh !== undefined ? (
                              <>{speedKmh} <span style={{ fontSize: 10 }}>km/h</span></>
                            ) : (
                              <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>--</span>
                            )}
                          </span>
                        </div>
                        <div className="kpi-box">
                          <span className="kpi-label">Movement</span>
                          <span className="kpi-val" style={{ color: '#fde047' }}>
                            {speedValid ? getMovementPace(speedKmh) : 'Active'}
                          </span>
                        </div>
                        <div className="kpi-box">
                          <span className="kpi-label">Pressure</span>
                          <span className="kpi-val" style={{ color: (nearestDist && nearestDist < 2.5) ? '#ef4444' : '#10b981' }}>
                            {pressure}
                          </span>
                        </div>
                        <div className="kpi-box">
                          <span className="kpi-label">Nearest Marker</span>
                          <span className="kpi-val" style={{ fontSize: 11 }}>
                            {nearestOpp ? `${nearestOpp} (${nearestDist || 0}m)` : 'None in 5m'}
                          </span>
                        </div>
                      </div>

                      <div className="tactical-context-block">
                        <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-cyan)', marginBottom: 6 }}>
                          PASSING & SUPPORT OPTIONS
                        </div>
                        {supports && supports.length > 0 ? (
                          <div>
                            <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 4 }}>
                              Closest Passing Outlets:
                            </div>
                            {supports.slice(0, 3).map((tm, i) => (
                              <div key={i} className="support-tm-item">
                                <span>#{tm.shirt} {tm.name}</span>
                                <span style={{ fontFamily: 'monospace', color: 'var(--accent-cyan)' }}>{tm.distance_m}m open</span>
                              </div>
                            ))}
                          </div>
                        ) : (
                          <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                            No immediate teammate within 10m.
                          </div>
                        )}
                      </div>
                    </>
                  );
                })()}
              </div>
            )}

            {/* 2+ PLAYERS SELECTED: COEXISTING GROUP & INDIVIDUAL VIEW */}
            {selectedPlayerIds.length >= 2 && (
              <>
                <div style={{ display: 'flex', gap: 6, marginBottom: 12, overflowX: 'auto', paddingBottom: 4 }}>
                  <button
                    className={`filter-pill ${inspectedPlayerId === null ? 'active' : ''}`}
                    onClick={() => setInspectedPlayerId(null)}
                    title="View Collective Group Dynamics"
                  >
                    Group Overview ({selectedPlayerIds.length})
                  </button>
                  {selectedPlayerIds.map((pid) => {
                    const pl = players.find((p) => String(p.player_id) === String(pid)) || selAnalysis?.individual_profiles?.find((p) => String(p.player_id) === String(pid));
                    const label = pl ? `#${pl.shirt} ${pl.name?.split(' ').pop() || ''}${pl.is_carrier ? ' ⚽' : ''}` : `ID ${pid}`;
                    return (
                      <button
                        key={pid}
                        className={`filter-pill ${String(inspectedPlayerId) === String(pid) ? 'active' : ''}`}
                        onClick={() => setInspectedPlayerId(pid)}
                        title={`Inspect Individual Stats for ${label}`}
                      >
                        {label}
                      </button>
                    );
                  })}
                </div>

                {inspectedPlayerId !== null ? (
                  <div className="card deep-dive-card">
                    {(() => {
                      const resolved = resolvePlayerData(inspectedPlayerId, selAnalysis, players);
                      if (!resolved) return null;
                      const { p, speedKmh, speedValid, nearestOpp, nearestDist, pressure, supports } = resolved;
                      return (
                        <>
                          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                              <div className="player-avatar-circle" style={{ backgroundColor: p.accent_color || (p.team === 0 ? '#00e5ff' : '#ef4444') }}>
                                #{p.shirt}
                              </div>
                              <div>
                                <div style={{ fontSize: 14, fontWeight: 700 }}>{p.name}</div>
                                <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                                  {p.team_name} • Role {p.role ?? p.pos ?? ''}
                                </div>
                              </div>
                            </div>
                            <button
                              type="button"
                              className="btn btn-outline"
                              style={{ fontSize: 10, padding: '3px 8px' }}
                              onClick={() => setInspectedPlayerId(null)}
                            >
                              ← Group Overview
                            </button>
                          </div>

                          <div className="stats-kpi-grid">
                            <div className="kpi-box">
                              <span className="kpi-label">Current Speed</span>
                              <span className="kpi-val" style={{ color: 'var(--accent-cyan)' }}>
                                {speedValid && speedKmh !== null && speedKmh !== undefined ? (
                                  <>{speedKmh} <span style={{ fontSize: 10 }}>km/h</span></>
                                ) : (
                                  <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>--</span>
                                )}
                              </span>
                            </div>
                            <div className="kpi-box">
                              <span className="kpi-label">Movement</span>
                              <span className="kpi-val" style={{ color: '#fde047' }}>
                                {speedValid ? getMovementPace(speedKmh) : 'Active'}
                              </span>
                            </div>
                            <div className="kpi-box">
                              <span className="kpi-label">Pressure</span>
                              <span className="kpi-val" style={{ color: (nearestDist && nearestDist < 2.5) ? '#ef4444' : '#10b981' }}>
                                {pressure}
                              </span>
                            </div>
                            <div className="kpi-box">
                              <span className="kpi-label">Nearest Marker</span>
                              <span className="kpi-val" style={{ fontSize: 11 }}>
                                {nearestOpp ? `${nearestOpp} (${nearestDist || 0}m)` : 'None in 5m'}
                              </span>
                            </div>
                          </div>

                          <div className="tactical-context-block">
                            <div style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-cyan)', marginBottom: 6 }}>
                              PASSING & SUPPORT OPTIONS
                            </div>
                            {supports && supports.length > 0 ? (
                              <div>
                                <div style={{ fontSize: 10, color: 'var(--text-muted)', marginBottom: 4 }}>
                                  Closest Passing Outlets:
                                </div>
                                {supports.slice(0, 3).map((tm, i) => (
                                  <div key={i} className="support-tm-item">
                                    <span>#{tm.shirt} {tm.name}</span>
                                    <span style={{ fontFamily: 'monospace', color: 'var(--accent-cyan)' }}>{tm.distance_m}m open</span>
                                  </div>
                                ))}
                              </div>
                            ) : (
                              <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                                No immediate teammate within 10m.
                              </div>
                            )}
                          </div>
                        </>
                      );
                    })()}
                  </div>
                ) : (
                  <>
                    {/* 2 PLAYERS: PAIRWISE DYNAMICS */}
                    {selectedPlayerIds.length === 2 && (
                      <div className="card deep-dive-card">
                        <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-cyan)', marginBottom: 8 }}>
                          PAIRWISE DYNAMICS & COORDINATION
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: 8, background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)' }}>
                          <strong>{selAnalysis.player_1 || 'Player A'}</strong>
                          <span style={{ color: 'var(--accent-cyan)', fontWeight: 700 }}>↔</span>
                          <strong>{selAnalysis.player_2 || 'Player B'}</strong>
                        </div>

                        <div className="stats-kpi-grid" style={{ marginTop: 10 }}>
                          <div className="kpi-box">
                            <span className="kpi-label">Spacing</span>
                            <span className="kpi-val" style={{ color: '#fde047' }}>{selAnalysis.pairwise_distance_m || '--'}m</span>
                          </div>
                          <div className="kpi-box">
                            <span className="kpi-label">Tactical Link</span>
                            <span className="kpi-val" style={{ color: 'var(--accent-cyan)', fontSize: 11 }}>
                              {selAnalysis.pairwise_distance_m && selAnalysis.pairwise_distance_m < 15 ? 'Immediate Support' : 'Switch Outlet'}
                            </span>
                          </div>
                          <div className="kpi-box" style={{ gridColumn: 'span 2' }}>
                            <span className="kpi-label">Unit Coordination</span>
                            <span className="kpi-val" style={{ color: 'var(--accent-green)' }}>
                              {selAnalysis.coordination_label || 'Synchronized Movement'}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* 3+ PLAYERS: CUSTOM UNIT / GROUP OVERLOAD */}
                    {selectedPlayerIds.length >= 3 && (
                      <div className="card deep-dive-card">
                        <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-cyan)', marginBottom: 8 }}>
                          CUSTOM GROUP & OVERLOAD ANALYSIS ({selectedPlayerIds.length} PLAYERS)
                        </div>

                        <div className="stats-kpi-grid">
                          <div className="kpi-box">
                            <span className="kpi-label">Group Width</span>
                            <span className="kpi-val">{selAnalysis.group_width_m || '--'}m</span>
                          </div>
                          <div className="kpi-box">
                            <span className="kpi-label">Group Depth</span>
                            <span className="kpi-val">{selAnalysis.group_depth_m || '--'}m</span>
                          </div>
                          <div className="kpi-box">
                            <span className="kpi-label">Dispersion</span>
                            <span className="kpi-val">{selAnalysis.compactness_dispersion_m || '--'}m</span>
                          </div>
                          <div className="kpi-box">
                            <span className="kpi-label">Local Situation</span>
                            <span className="kpi-val" style={{ fontSize: 11, color: '#fde047' }}>
                              {selAnalysis.numerical_situation || `${selectedPlayerIds.length}v3`}
                            </span>
                          </div>
                        </div>

                        <div style={{ marginTop: 10, padding: 8, background: 'var(--bg-input)', borderRadius: 'var(--radius-sm)' }}>
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Overload Assessment:</div>
                          <div style={{ fontSize: 12, fontWeight: 700, color: 'var(--accent-green)', marginTop: 2 }}>
                            {selAnalysis.overload_status || 'Local Numerical Superiority Established'}
                          </div>
                        </div>
                      </div>
                    )}
                  </>
                )}
              </>
            )}
          </div>
        )}

        {/* ================================================================= */}
        {/* TAB 4: SPACE & RUNNING OPPORTUNITIES                              */}
        {/* ================================================================= */}
        {activeTab === 'space_runs' && (
          <div className="tab-pane">
            <div className="card-header-row">
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Zap size={15} color="var(--accent-cyan)" />
                <span style={{ fontWeight: 700, fontSize: 13 }}>Space & Running Opportunities</span>
              </div>
            </div>

            {spaceOpps.length === 0 ? (
              <div className="empty-panel-notice">
                <Zap size={26} color="var(--text-muted)" />
                <div style={{ fontWeight: 600, color: '#fff', marginTop: 8 }}>
                  No Open Pockets Detected
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', maxWidth: 260, marginTop: 4 }}>
                  Defensive block is compact in this frame. Advance playback to detect open pockets or channel gaps.
                </div>
              </div>
            ) : (
              <div className="space-opps-list">
                {spaceOpps.map((opp, idx) => (
                  <div key={idx} className="space-opp-card">
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span className="space-opp-type-badge">{opp.label}</span>
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-primary)', marginTop: 4 }}>
                      {opp.area_description}
                    </div>
                    <div style={{ fontSize: 11, color: 'var(--accent-cyan)', marginTop: 4 }}>
                      {opp.tactical_value}
                    </div>
                    {opp.candidate_runners && opp.candidate_runners.length > 0 && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 6, fontSize: 10, color: 'var(--text-muted)' }}>
                        <span>Runners:</span>
                        {opp.candidate_runners.map((r, i) => (
                          <span key={i} className="rec-player-badge">{r}</span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
