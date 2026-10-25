import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Flame,
  Zap,
  Target,
  Shield,
  Play,
  Maximize2,
  Minimize2,
  Brain,
  CheckCircle2,
  Clock,
  Compass,
  Send,
  Gauge,
  Users,
  Share2
} from 'lucide-react';

/**
 * Clean 105m x 68m 2D Pitch SVG canvas for the Coach AI Multi-Pitch Deck.
 */
function AIPitchCanvas({
  title,
  subtitle,
  badgeText,
  badgeColor = '#10b981',
  icon: Icon = Compass,
  isExpanded = false,
  onToggleExpand,
  legendItems = [],
  footerNote,
  children,
}) {
  const pitchWidth = 1050;
  const pitchHeight = 680;
  const pad = 28;
  const innerW = pitchWidth - pad * 2;
  const innerH = pitchHeight - pad * 2;

  const toX = (normX) => pad + Math.max(0, Math.min(1, normX ?? 0.5)) * innerW;
  const toY = (normY) => pad + Math.max(0, Math.min(1, normY ?? 0.5)) * innerH;

  return (
    <div className={`ai-multi-pitch-card ${isExpanded ? 'expanded-full' : ''}`}>
      <div className="ai-pitch-card-header">
        <div className="ai-pitch-title-group">
          <div className="ai-pitch-icon-box" style={{ borderColor: `${badgeColor}44`, color: badgeColor }}>
            <Icon size={16} />
          </div>
          <div>
            <div className="ai-pitch-title-row">
              <h4>{title}</h4>
              {badgeText && (
                <span
                  className="ai-pitch-badge"
                  style={{
                    color: badgeColor,
                    borderColor: `${badgeColor}44`,
                    backgroundColor: `${badgeColor}14`,
                  }}
                >
                  {badgeText}
                </span>
              )}
            </div>
            {subtitle && <p className="ai-pitch-subtitle">{subtitle}</p>}
          </div>
        </div>

        <div className="ai-pitch-header-actions">
          {legendItems.length > 0 && (
            <div className="ai-pitch-legend">
              {legendItems.map((item, idx) => (
                <span key={idx} className="ai-legend-item">
                  <span className="ai-legend-dot" style={{ backgroundColor: item.color }} />
                  {item.label}
                </span>
              ))}
            </div>
          )}
          {onToggleExpand && (
            <button
              type="button"
              className="pitch-pill-btn"
              onClick={onToggleExpand}
              title={isExpanded ? 'Restore Grid Size' : 'Expand Map to Full Width'}
            >
              {isExpanded ? <Minimize2 size={12} /> : <Maximize2 size={12} />}
              <span style={{ marginLeft: 4 }}>{isExpanded ? 'Grid View' : 'Expand'}</span>
            </button>
          )}
        </div>
      </div>

      <div className="ai-pitch-svg-stage">
        <svg
          viewBox={`0 0 ${pitchWidth} ${pitchHeight}`}
          className="ai-dedicated-pitch-svg"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            <linearGradient id="aiTurfGrad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#15803d" />
              <stop offset="50%" stopColor="#166534" />
              <stop offset="100%" stopColor="#14532d" />
            </linearGradient>
            <pattern id="aiTurfStripes" width="99.4" height="680" patternUnits="userSpaceOnUse">
              <rect x="0" y="0" width="49.7" height="680" fill="#16a34a" opacity="0.22" />
              <rect x="49.7" y="0" width="49.7" height="680" fill="#14532d" opacity="0.28" />
            </pattern>
            <marker id="aiArrowGold" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#fde047" />
            </marker>
            <marker id="aiArrowCyan" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#38bdf8" />
            </marker>
            <marker id="aiArrowGreen" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#22c55e" />
            </marker>
            <marker id="aiArrowAmber" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#f59e0b" />
            </marker>
            <marker id="aiArrowRed" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#ef4444" />
            </marker>
          </defs>

          {/* Pitch Turf & Mow Stripes */}
          <rect x="0" y="0" width={pitchWidth} height={pitchHeight} fill="url(#aiTurfGrad)" />
          <rect x={pad} y={pad} width={innerW} height={innerH} fill="url(#aiTurfStripes)" />

          {/* Pitch Lines */}
          <rect x={pad} y={pad} width={innerW} height={innerH} fill="none" stroke="rgba(255, 255, 255, 0.82)" strokeWidth="2.4" rx="4" />
          <line x1={pad + innerW / 2} y1={pad} x2={pad + innerW / 2} y2={pad + innerH} stroke="rgba(255, 255, 255, 0.82)" strokeWidth="2" />
          <circle cx={pad + innerW / 2} cy={pad + innerH / 2} r="84" fill="none" stroke="rgba(255, 255, 255, 0.82)" strokeWidth="2" />
          <circle cx={pad + innerW / 2} cy={pad + innerH / 2} r="3.5" fill="#ffffff" />

          {/* Thirds subtle guide lines */}
          <line x1={pad + innerW / 3} y1={pad} x2={pad + innerW / 3} y2={pad + innerH} stroke="rgba(255, 255, 255, 0.28)" strokeWidth="1.2" strokeDasharray="6 6" />
          <line x1={pad + (innerW * 2) / 3} y1={pad} x2={pad + (innerW * 2) / 3} y2={pad + innerH} stroke="rgba(255, 255, 255, 0.28)" strokeWidth="1.2" strokeDasharray="6 6" />

          {/* Left Penalty & 6-yard Box */}
          <rect x={pad} y={pad + innerH * 0.21} width={innerW * 0.16} height={innerH * 0.58} fill="none" stroke="rgba(255, 255, 255, 0.82)" strokeWidth="2" />
          <rect x={pad} y={pad + innerH * 0.36} width={innerW * 0.055} height={innerH * 0.28} fill="none" stroke="rgba(255, 255, 255, 0.78)" strokeWidth="1.8" />
          <rect x={pad - 10} y={pad + innerH * 0.44} width="10" height={innerH * 0.12} fill="rgba(255, 255, 255, 0.2)" stroke="#ffffff" strokeWidth="1.5" />

          {/* Right Penalty & 6-yard Box */}
          <rect x={pad + innerW * 0.84} y={pad + innerH * 0.21} width={innerW * 0.16} height={innerH * 0.58} fill="none" stroke="rgba(255, 255, 255, 0.82)" strokeWidth="2" />
          <rect x={pad + innerW * 0.945} y={pad + innerH * 0.36} width={innerW * 0.055} height={innerH * 0.28} fill="none" stroke="rgba(255, 255, 255, 0.78)" strokeWidth="1.8" />
          <rect x={pad + innerW} y={pad + innerH * 0.44} width="10" height={innerH * 0.12} fill="rgba(255, 255, 255, 0.2)" stroke="#ffffff" strokeWidth="1.5" />

          {children({ toX, toY, pad, innerW, innerH })}
        </svg>
      </div>

      {footerNote && <div className="ai-pitch-card-footer">{footerNote}</div>}
    </div>
  );
}

export default function CoachAILabSection({
  intervalStart = 0,
  intervalEnd = 15,
  isAnalyzing = false,
  onAskCoachAi,
  coachAiReport = null,
  selectedPlayerIds = [],
  players = [],
  onSeekToTime,
  currentMatch = null,
  matchSummary = null,
}) {
  const [aiQuestion, setAiQuestion] = useState('');
  const [expandedPitchId, setExpandedPitchId] = useState(null);
  const [clipFilter, setClipFilter] = useState('all'); // 'all' | 'highlights'

  // Extract Teams from matchSummary or fallback
  const team0 = matchSummary?.teams?.team_0 || { name: 'Newcastle United', short_name: 'Newcastle', code: 'NEW', color_rgb: [0, 229, 255] };
  const team1 = matchSummary?.teams?.team_1 || { name: 'Paris Saint-Germain', short_name: 'PSG', code: 'PSG', color_rgb: [239, 68, 68] };
  const [coachingTeam, setCoachingTeam] = useState(team0.name);

  useEffect(() => {
    if (matchSummary?.teams?.team_0?.name) {
      setCoachingTeam(matchSummary.teams.team_0.name);
    }
  }, [matchSummary?.teams?.team_0?.name]);

  const handleToggleExpand = (mapId) => {
    const update = () => setExpandedPitchId((prev) => (prev === mapId ? null : mapId));
    if (typeof document !== 'undefined' && document.startViewTransition && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      document.startViewTransition(() => update());
    } else {
      update();
    }
  };

  const handleJumpAndScrollVideo = (timestampS) => {
    if (timestampS == null) return;
    onSeekToTime?.(timestampS);
    document.getElementById('video-section')?.scrollIntoView({ behavior: 'smooth' });
  };

  const pitchMaps = coachAiReport?.pitch_maps || [];
  const comparisonCards = coachAiReport?.comparison_cards || [];
  const clipTimings = coachAiReport?.clip_timings || [];
  const filteredClips = clipFilter === 'highlights'
    ? clipTimings.filter((c) => c.highlight)
    : clipTimings;

  const duelData = coachAiReport?.duel_1v1 || null;
  const speedComp = duelData?.speed_comparison || null;
  const primaryProfile = coachAiReport?.player_profiles?.[0] || null;
  const intents = coachAiReport?.intents || [];

  return (
    <section className="coach-ai-lab-wrapper" id="coach-ai-lab-section">
      {/* =================================================================== */}
      {/* 1. CLEAN PROMPT BAR, TEAM SELECTOR & 90-MIN SCOPE                   */}
      {/* =================================================================== */}
      <div className="coach-ai-command-card">
        <div className="coach-ai-header-top">
          <div className="coach-ai-brand">
            <div className="coach-ai-orb">
              <Sparkles size={18} color="#ffffff" />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, flexWrap: 'wrap' }}>
                <h2>Coach AI Analyst</h2>
                <span className="ai-lab-status-pill">
                  <Brain size={12} />
                  {coachAiReport?.learned_memory
                    ? `Auto-Trained (${coachAiReport.learned_memory.model_version || 'v2'} • ${coachAiReport.learned_memory.total_queries_learned} queries learned)`
                    : 'Self-Training 90-Min Engine'}
                </span>
              </div>
              <p>
                Full 90-Minute Tactical Decision Engine & Match Intelligence
              </p>
            </div>
          </div>

          <div className="ai-scope-status-badge">
            <Compass size={14} color="#00e5ff" />
            <span>Full 90 Minutes Analysis Mode</span>
          </div>
        </div>

        {/* Coach Team Selector Bar */}
        <div className="coaching-team-selector-strip">
          <div className="selector-title">
            <Shield size={14} color="#00e5ff" />
            <span>Select Your Coaching Team:</span>
          </div>
          <div className="team-toggle-options">
            <button
              type="button"
              className={`team-select-pill ${coachingTeam === team0.name ? 'active-coaching-team' : ''}`}
              onClick={() => setCoachingTeam(team0.name)}
            >
              <span 
                className="team-dot" 
                style={{ backgroundColor: team0.color_rgb ? `rgb(${team0.color_rgb.join(',')})` : '#00e5ff' }} 
              />
              <span className="team-title">{team0.name}</span>
              {coachingTeam === team0.name && <span className="active-team-tag">OUR SQUAD</span>}
            </button>
            <button
              type="button"
              className={`team-select-pill ${coachingTeam === team1.name ? 'active-coaching-team' : ''}`}
              onClick={() => setCoachingTeam(team1.name)}
            >
              <span 
                className="team-dot" 
                style={{ backgroundColor: team1.color_rgb ? `rgb(${team1.color_rgb.join(',')})` : '#ef4444' }} 
              />
              <span className="team-title">{team1.name}</span>
              {coachingTeam === team1.name && <span className="active-team-tag">OUR SQUAD</span>}
            </button>
          </div>
        </div>

        <form
          className="coach-ai-prompt-form"
          onSubmit={(e) => {
            e.preventDefault();
            onAskCoachAi?.(aiQuestion, 'full_match', null, coachingTeam);
          }}
        >
          <div className="prompt-input-container">
            <Sparkles size={16} color="#00e5ff" className="prompt-sparkle-icon" />
            <input
              type="text"
              className="coach-ai-prompt-input"
              value={aiQuestion}
              onChange={(e) => setAiQuestion(e.target.value)}
              placeholder=""
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary coach-ai-submit-btn"
            disabled={isAnalyzing}
          >
            <Send size={14} />
            <span>{isAnalyzing ? 'Scanning 90m Data...' : 'Ask Coach AI'}</span>
          </button>
        </form>
      </div>

      {/* =================================================================== */}
      {/* 2. DYNAMIC PROMPT-DRIVEN ANSWER, KPI CARDS, CLIP TIMINGS & 2D MAPS  */}
      {/* =================================================================== */}
      {isAnalyzing ? (
        <div className="ai-football-scanner-box">
          <div className="scanner-header">
            <div className="scanner-orb">
              <Sparkles size={22} color="#00e5ff" />
            </div>
            <div>
              <h3>Deep 90-Minute Match Telemetry Scan</h3>
              <p>
                Auditing 90 minutes of 25 FPS tracking data for <strong>{coachingTeam}</strong>...
              </p>
            </div>
          </div>

          <div className="football-track-container">
            <div className="pitch-yard-markers">
              <span>0' Kickoff</span>
              <span>15' High Press</span>
              <span>45' Half-Time</span>
              <span>60' Subs</span>
              <span>75' Transitions</span>
              <span>90' Full-Time</span>
            </div>
            <div className="football-pitch-line">
              <div className="scan-line-progress" />
              <div className="football-ball-animated">
                <svg viewBox="0 0 24 24" className="soccer-ball-svg">
                  <circle cx="12" cy="12" r="10" fill="#ffffff" stroke="#09101d" strokeWidth="1.5" />
                  <polygon points="12,7 15.5,9.5 14,14 10,14 8.5,9.5" fill="#09101d" />
                  <line x1="12" y1="2" x2="12" y2="7" stroke="#09101d" strokeWidth="1.2" />
                  <line x1="21.5" y1="9" x2="15.5" y2="9.5" stroke="#09101d" strokeWidth="1.2" />
                  <line x1="18" y1="19.5" x2="14" y2="14" stroke="#09101d" strokeWidth="1.2" />
                  <line x1="6" y1="19.5" x2="10" y2="14" stroke="#09101d" strokeWidth="1.2" />
                  <line x1="2.5" y1="9" x2="8.5" y2="9.5" stroke="#09101d" strokeWidth="1.2" />
                </svg>
              </div>
            </div>
          </div>

          <div className="scanner-status-ticker">
            <span className="ticker-pulse-dot" />
            <span className="ticker-status-text">
              Synthesizing UEFA Pro tactical adjustments and backline discipline with Gemini AI...
            </span>
          </div>
        </div>
      ) : !coachAiReport ? (
        <div className="ai-lab-empty-state">
          <div className="empty-orb">
            <Compass size={28} color="#00e5ff" />
          </div>
          <h3>Ask Any Tactical Question Above</h3>
          <p>
            Coach AI scans the full 90 minutes (or your selected interval) for the exact players you mention, generating their 2D heatmaps, head-to-head speed comparisons, dribble outcomes, and clickable video clip timings.
          </p>
        </div>
      ) : (
        <div className="coach-ai-results-container">
          {/* Top Executive Bento Row: Left (Answer & KPI Cards) | Right (Interactive Clip Timings Reel) */}
          <div className={`ai-executive-bento-row ${clipTimings.length > 0 ? 'has-clips' : 'single-col'}`}>
            {/* A. Direct Answer Summary Card */}
            <div className="ai-executive-banner">
              <div className="ai-exec-headline-row">
                <span className="ai-exec-tag">{coachAiReport.scope_label}</span>
                <h3>{coachAiReport.headline}</h3>
                <span className="ai-compute-badge">
                  ⚡ {coachAiReport.compute_time_ms}ms • Auto-Trained
                </span>
              </div>

              {coachAiReport.question && (
                <div className="ai-asked-question-strip">
                  <strong>Prompt:</strong> “{coachAiReport.question}”
                </div>
              )}

              {/* UEFA Pro Tactical Briefing (Gemini 3.5 Flash Lite) */}
              {coachAiReport.tactical_briefing && (
                <div className="ai-tactical-briefing-card">
                  <div className="briefing-header">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <Sparkles size={15} color="#10b981" />
                      <span className="briefing-badge-text">UEFA PRO TACTICAL SYNTHESIZER</span>
                    </div>
                    <span className="briefing-model-pill">
                      ⚡ {coachAiReport.tactical_briefing.powered_by || 'gemini-3.5-flash-lite'}
                    </span>
                  </div>

                  {coachAiReport.tactical_briefing.executive_verdict && (
                    <div className="briefing-verdict-box">
                      <div className="verdict-label">EXECUTIVE DIAGNOSIS</div>
                      <p className="verdict-text">{coachAiReport.tactical_briefing.executive_verdict}</p>
                    </div>
                  )}

                  {coachAiReport.tactical_briefing.actionable_instructions?.length > 0 && (
                    <div className="briefing-instructions-box">
                      <div className="instructions-label">ACTIONABLE IN-GAME INSTRUCTIONS</div>
                      <div className="instructions-list">
                        {coachAiReport.tactical_briefing.actionable_instructions.map((inst, idx) => (
                          <div key={idx} className="instruction-item">
                            <span className="instruction-num">{idx + 1}</span>
                            <span className="instruction-text">{inst}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}

              <div className="ai-exec-bullets">
                {coachAiReport.narrative_bullets?.map((b, i) => (
                  <div key={i} className="ai-exec-bullet-item">
                    <CheckCircle2 size={15} color="#34d399" style={{ flexShrink: 0, marginTop: 2 }} />
                    <span>{b}</span>
                  </div>
                ))}
              </div>

              {/* B. Key Comparison Stat Cards */}
              {comparisonCards.length > 0 && (
                <div className="ai-comparison-kpi-grid">
                  {comparisonCards.map((card, idx) => (
                    <div key={idx} className="ai-comparison-kpi-card" style={{ borderTop: `3px solid ${card.color || '#38bdf8'}` }}>
                      <div className="ai-kpi-card-label">{card.label}</div>
                      <div className="ai-kpi-card-value" style={{ color: card.color || '#f8fafc' }}>
                        {card.value}
                      </div>
                      <div className="ai-kpi-card-sub">{card.sub}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* C. Interactive Video Clip Timings Strip */}
            {clipTimings.length > 0 && (
              <div className="ai-clips-card">
                <div className="ai-clips-header">
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <Play size={15} color="#00e5ff" />
                    <h4>Clip Timings ({filteredClips.length})</h4>
                  </div>
                  {clipTimings.some((c) => c.highlight) && (
                    <div style={{ display: 'flex', gap: 5 }}>
                      <button
                        type="button"
                        className={`pitch-pill-btn ${clipFilter === 'all' ? 'active' : ''}`}
                        onClick={() => setClipFilter('all')}
                      >
                        All ({clipTimings.length})
                      </button>
                      <button
                        type="button"
                        className={`pitch-pill-btn ${clipFilter === 'highlights' ? 'active' : ''}`}
                        onClick={() => setClipFilter('highlights')}
                      >
                        Got Past ({clipTimings.filter((c) => c.highlight).length})
                      </button>
                    </div>
                  )}
                </div>

                <div className="ai-clips-grid">
                  {filteredClips.map((clip, idx) => (
                    <button
                      key={idx}
                      type="button"
                      className={`ai-clip-item-btn ${clip.highlight ? 'highlight' : ''}`}
                      onClick={() => handleJumpAndScrollVideo(clip.timestamp_s)}
                    >
                      <div className="ai-clip-top">
                        <span className="ai-clip-clock">
                          <Play size={10} /> {clip.clock} ({clip.half})
                        </span>
                        <span className="ai-clip-sec">@{clip.timestamp_s}s</span>
                      </div>
                      <div className="ai-clip-label">{clip.label}</div>
                      <div className="ai-clip-detail">{clip.detail}</div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* D. Dynamic 2D Pitch Maps (Heatmaps for Mentioned Players, 1v1 Dribbles, Runs, Shots) */}
          {pitchMaps.length > 0 && (
            <div className="ai-multi-pitch-grid">
              {pitchMaps.map((pm) => {
                if (pm.type === 'heatmap') {
                  const avgPos = pm.avg_position_m || [52.5, 34.0];
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#f59e0b"
                      icon={Flame}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#22c55e', label: 'Low' },
                        { color: '#eab308', label: 'Medium' },
                        { color: '#f97316', label: 'High' },
                        { color: '#ef4444', label: 'Peak Zone' },
                      ]}
                      footerNote={`Average Operating Coordinate: (${avgPos[0]}m, ${avgPos[1]}m)`}
                    >
                      {({ toX, toY, innerW, innerH }) => {
                        const avgX = toX(avgPos[0] / 105.0);
                        const avgY = toY(avgPos[1] / 68.0);
                        return (
                          <g>
                            {pm.heatmap_cells?.map((cell, idx) => {
                              const cx = toX(cell.x_norm);
                              const cy = toY(cell.y_norm);
                              const cw = cell.w_norm * innerW;
                              const ch = cell.h_norm * innerH;
                              const v = cell.intensity || 0;
                              let fillCol = `rgba(34, 197, 94, ${0.22 + v * 0.35})`;
                              if (v >= 0.7) fillCol = `rgba(239, 68, 68, ${0.48 + v * 0.36})`;
                              else if (v >= 0.42) fillCol = `rgba(249, 115, 22, ${0.38 + v * 0.34})`;
                              else if (v >= 0.2) fillCol = `rgba(234, 179, 8, ${0.3 + v * 0.3})`;

                              return (
                                <g key={idx}>
                                  <rect
                                    x={cx + 2}
                                    y={cy + 2}
                                    width={Math.max(4, cw - 4)}
                                    height={Math.max(4, ch - 4)}
                                    rx="10"
                                    fill={fillCol}
                                    stroke={v >= 0.45 ? 'rgba(255,255,255,0.35)' : 'none'}
                                    strokeWidth="1"
                                  />
                                  {v >= 0.32 && (
                                    <text
                                      x={cx + cw / 2}
                                      y={cy + ch / 2 + 4}
                                      fill="#ffffff"
                                      fontSize="11"
                                      fontWeight="800"
                                      fontFamily="monospace"
                                      textAnchor="middle"
                                    >
                                      {Math.round(v * 100)}%
                                    </text>
                                  )}
                                </g>
                              );
                            })}

                            {/* Average Position Node */}
                            <circle cx={avgX} cy={avgY} r="20" fill="none" stroke="#ffffff" strokeWidth="2" strokeDasharray="4 3" />
                            <circle cx={avgX} cy={avgY} r="13" fill={pm.player?.accent_color || '#2563eb'} stroke="#ffffff" strokeWidth="2.5" />
                            <text x={avgX} y={avgY + 4} fill="#ffffff" fontSize="11" fontWeight="900" fontFamily="monospace" textAnchor="middle">
                              #{pm.player?.shirt}
                            </text>
                          </g>
                        );
                      }}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'pass_combination') {
                  const passes = pm.passes || [];
                  const revPasses = pm.reverse_passes || [];
                  const passerLast = pm.passer?.name?.split(' ').pop() || 'Passer';
                  const receiverLast = pm.receiver?.name?.split(' ').pop() || 'Receiver';
                  const passerShirt = pm.passer?.shirt ? `#${pm.passer.shirt}` : '';
                  const receiverShirt = pm.receiver?.shirt ? `#${pm.receiver.shirt}` : '';

                  const legend = [
                    { color: '#22c55e', label: `${passerLast} -> ${receiverLast} (${passes.length} Passes)` },
                    { color: '#f59e0b', label: 'Key / Progressive Pass' },
                  ];
                  if (revPasses.length > 0) {
                    legend.push({ color: '#38bdf8', label: `Reverse: ${receiverLast} -> ${passerLast} (${revPasses.length})` });
                  }

                  const totalDist = passes.reduce((acc, p) => acc + (p.distance_m || 0), 0).toFixed(1);

                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#16a34a"
                      icon={Share2}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={legend}
                      footerNote={`Direct Connection: ${passerLast} found ${receiverLast} ${passes.length} times (${totalDist}m total pass length) • ${revPasses.length} reverse linkup passes`}
                    >
                      {({ toX, toY }) => (
                        <g>
                          {/* Forward Passes: Passer -> Receiver */}
                          {passes.map((p, idx) => {
                            const x1 = toX(p.start_x);
                            const y1 = toY(p.start_y);
                            const x2 = toX(p.end_x);
                            const y2 = toY(p.end_y);
                            const isKey = p.is_key_pass;
                            const isSpecial = isKey || p.is_progressive || p.is_switch || p.is_long_ball;
                            const strokeCol = isKey ? '#f59e0b' : (isSpecial ? '#10b981' : '#22c55e');
                            const midX = (x1 + x2) / 2;
                            const midY = (y1 + y2) / 2;
                            return (
                              <g
                                key={`pass-combo-${idx}`}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(p.timestamp_s)}
                              >
                                <line
                                  x1={x1}
                                  y1={y1}
                                  x2={x2}
                                  y2={y2}
                                  stroke={strokeCol}
                                  strokeWidth={isSpecial ? '3.0' : '2.2'}
                                  opacity="0.9"
                                  markerEnd={isKey ? 'url(#aiArrowGold)' : 'url(#aiArrowGreen)'}
                                />
                                {/* Passer Start Node */}
                                <circle cx={x1} cy={y1} r="5" fill={strokeCol} stroke="#0f172a" strokeWidth="1.5" />
                                <text x={x1} y={y1 - 7} fill="#e2e8f0" fontSize="9" fontWeight="bold" textAnchor="middle">
                                  {passerShirt}
                                </text>
                                {/* Receiver End Node */}
                                <circle cx={x2} cy={y2} r="6.5" fill="none" stroke={strokeCol} strokeWidth="1.8" strokeDasharray="3 2" />
                                <circle cx={x2} cy={y2} r="3" fill={strokeCol} />
                                <text x={x2} y={y2 + 13} fill="#e2e8f0" fontSize="9" fontWeight="bold" textAnchor="middle">
                                  {receiverShirt} ({p.clock})
                                </text>
                                {/* Distance & Tag Badge at Midpoint */}
                                <rect
                                  x={midX - 24}
                                  y={midY - 8}
                                  width="48"
                                  height="16"
                                  rx="4"
                                  fill="#0f172a"
                                  fillOpacity="0.88"
                                  stroke={strokeCol}
                                  strokeWidth="0.8"
                                />
                                <text
                                  x={midX}
                                  y={midY + 3.5}
                                  fill="#e2e8f0"
                                  fontSize="9"
                                  fontWeight="bold"
                                  textAnchor="middle"
                                >
                                  {p.distance_m?.toFixed(1)}m
                                </text>
                              </g>
                            );
                          })}

                          {/* Reverse Passes: Receiver -> Passer */}
                          {revPasses.map((rp, idx) => {
                            const x1 = toX(rp.start_x);
                            const y1 = toY(rp.start_y);
                            const x2 = toX(rp.end_x);
                            const y2 = toY(rp.end_y);
                            return (
                              <g
                                key={`rev-pass-${idx}`}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(rp.timestamp_s)}
                              >
                                <line
                                  x1={x1}
                                  y1={y1}
                                  x2={x2}
                                  y2={y2}
                                  stroke="#38bdf8"
                                  strokeWidth="2.0"
                                  strokeDasharray="5 3"
                                  opacity="0.85"
                                  markerEnd="url(#aiArrowCyan)"
                                />
                                <circle cx={x1} cy={y1} r="4" fill="#38bdf8" stroke="#0f172a" strokeWidth="1.2" />
                                <circle cx={x2} cy={y2} r="4" fill="#38bdf8" stroke="#0f172a" strokeWidth="1.2" />
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'passes_and_dribbles' && pm.pass_report) {
                  const pr = pm.pass_report;
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#2563eb"
                      icon={Zap}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#fde047', label: 'Switch / Long Ball' },
                        { color: '#22c55e', label: 'Completed Pass' },
                        { color: '#38bdf8', label: 'On-Ball Dribble' },
                      ]}
                      footerNote={`Passes: ${pr.passes_completed}/${pr.passes_attempted} (${pr.pass_accuracy_pct}%) • Switches: ${pr.switches_completed}/${pr.switches_attempted} • Long Balls: ${pr.long_balls_completed}/${pr.long_balls_attempted} • On-Ball Dribbles: ${pr.on_ball_dribbles_succeeded}/${pr.on_ball_dribbles_total}`}
                    >
                      {({ toX, toY }) => (
                        <g>
                          {/* Completed Passes & Switches */}
                          {pr.passes_events?.filter((p) => p.completed).map((pev, idx) => {
                            const x1 = toX(pev.start_x);
                            const y1 = toY(pev.start_y);
                            const x2 = toX(pev.end_x);
                            const y2 = toY(pev.end_y);
                            const isSpecial = pev.is_switch || pev.is_long_ball;
                            const col = isSpecial ? '#fde047' : '#22c55e';
                            return (
                              <g
                                key={`p-${idx}`}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(pev.timestamp_s)}
                              >
                                <line
                                  x1={x1}
                                  y1={y1}
                                  x2={x2}
                                  y2={y2}
                                  stroke={col}
                                  strokeWidth={isSpecial ? '3.0' : '2.0'}
                                  opacity={isSpecial ? '0.95' : '0.75'}
                                  markerEnd={isSpecial ? 'url(#aiArrowGold)' : 'url(#aiArrowGreen)'}
                                />
                                <circle cx={x1} cy={y1} r={isSpecial ? '5.5' : '4'} fill={col} stroke="#0f172a" strokeWidth="1.2" />
                              </g>
                            );
                          })}

                          {/* On-Ball Dribbles / Carries */}
                          {pr.dribbles_events?.map((dev, idx) => {
                            const x1 = toX(dev.start_x);
                            const y1 = toY(dev.start_y);
                            const x2 = toX(dev.end_x);
                            const y2 = toY(dev.end_y);
                            return (
                              <g
                                key={`d-${idx}`}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(dev.timestamp_s)}
                              >
                                <line
                                  x1={x1}
                                  y1={y1}
                                  x2={x2}
                                  y2={y2}
                                  className="flowing-lane-stroke"
                                  stroke="#38bdf8"
                                  strokeWidth="2.8"
                                  strokeDasharray="6 4"
                                  markerEnd="url(#aiArrowCyan)"
                                />
                                <circle cx={x1} cy={y1} r="5" fill="#38bdf8" stroke="#0f172a" strokeWidth="1.5" />
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'duels_1v1' && pm.duel_data) {
                  const dd = pm.duel_data;
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#16a34a"
                      icon={Users}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#fde047', label: `${dd.attacker.name.split(' ').pop()} Got Past (Dribble Complete)` },
                        { color: '#ef4444', label: `${dd.defender.name.split(' ').pop()} Won Ball Back (Duel Won)` },
                        { color: '#38bdf8', label: `${dd.defender.name.split(' ').pop()} Contained (Recycled)` },
                      ]}
                      footerNote="Click any 1v1 marker or trajectory vector on the pitch to watch that exact duel in the video player."
                    >
                      {({ toX, toY }) => (
                        <g>
                          {dd.duel_episodes?.map((ep, idx) => {
                            const sx = toX(ep.start_x ?? ep.x_norm);
                            const sy = toY(ep.start_y ?? ep.y_norm);
                            const ex = toX(ep.end_x ?? ep.x_norm);
                            const ey = toY(ep.end_y ?? ep.y_norm);
                            const gotPast = ep.got_past || ep.winner_side === 'attacker';
                            const defWonBall = ep.def_won_ball || ep.winner_side === 'defender';
                            const col = gotPast ? '#fde047' : (defWonBall ? '#ef4444' : '#38bdf8');
                            const markerUri = gotPast ? 'url(#aiArrowGold)' : (defWonBall ? 'url(#aiArrowRed)' : 'url(#aiArrowCyan)');

                            return (
                              <g
                                key={idx}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(ep.timestamp_s)}
                              >
                                <line
                                  x1={sx}
                                  y1={sy}
                                  x2={ex}
                                  y2={ey}
                                  stroke={col}
                                  strokeWidth={gotPast ? '3.4' : '2.2'}
                                  strokeDasharray={gotPast ? 'none' : '5 3'}
                                  markerEnd={markerUri}
                                />
                                <circle cx={sx} cy={sy} r={gotPast ? '9' : '7'} fill={col} stroke="#0f172a" strokeWidth="2" />
                                <rect
                                  x={sx - 46}
                                  y={sy - 24}
                                  width="92"
                                  height="15"
                                  rx="4"
                                  fill="rgba(15, 23, 42, 0.88)"
                                  stroke={col}
                                  strokeWidth="1"
                                />
                                <text
                                  x={sx}
                                  y={sy - 13}
                                  fill={col}
                                  fontSize="9"
                                  fontWeight="800"
                                  fontFamily="monospace"
                                  textAnchor="middle"
                                >
                                  {ep.clock} • {ep.p1_speed_kmh}km/h
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'runs' && pm.runs) {
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#2563eb"
                      icon={Zap}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#fde047', label: 'Run Fed by Pass' },
                        { color: '#38bdf8', label: 'Off-Ball Sprint' },
                      ]}
                      footerNote="Click any run arrow to jump the video player to that sprint."
                    >
                      {({ toX, toY }) => (
                        <g>
                          {pm.runs.map((run, idx) => {
                            const x1 = toX(run.start_x);
                            const y1 = toY(run.start_y);
                            const x2 = toX(run.end_x);
                            const y2 = toY(run.end_y);
                            const hasPass = Boolean(run.pass_provider);
                            const col = hasPass ? '#fde047' : '#38bdf8';
                            return (
                              <g
                                key={idx}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(run.timestamp_s)}
                              >
                                <circle cx={x1} cy={y1} r="5.5" fill={col} stroke="#0f172a" strokeWidth="1.5" />
                                <line
                                  x1={x1}
                                  y1={y1}
                                  x2={x2}
                                  y2={y2}
                                  stroke={col}
                                  strokeWidth="3.2"
                                  strokeDasharray={hasPass ? 'none' : '8 4'}
                                  markerEnd={hasPass ? 'url(#aiArrowGold)' : 'url(#aiArrowCyan)'}
                                />
                                <text
                                  x={(x1 + x2) / 2}
                                  y={(y1 + y2) / 2 - 6}
                                  fill="#ffffff"
                                  fontSize="9.5"
                                  fontWeight="800"
                                  fontFamily="monospace"
                                  textAnchor="middle"
                                >
                                  {run.clock} ({run.peak_speed_kmh}km/h)
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'shots' && pm.shot_audit) {
                  const sa = pm.shot_audit;
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#ef4444"
                      icon={Target}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#22c55e', label: 'Optimal Shot / Open Pass' },
                        { color: '#ef4444', label: 'Sub-Optimal Shot' },
                      ]}
                      footerNote="Click any shot node to watch the shot and inspect open teammate lanes."
                    >
                      {({ toX, toY }) => (
                        <g>
                          {sa.shots?.map((sh, idx) => {
                            const sx = toX(sh.x_norm);
                            const sy = toY(sh.y_norm);
                            const gx = toX(sh.goal_x_norm ?? 1.0);
                            const gy = toY(sh.goal_y_norm ?? 0.5);
                            const col = sh.is_suboptimal ? '#ef4444' : '#22c55e';
                            return (
                              <g
                                key={idx}
                                style={{ cursor: 'pointer' }}
                                onClick={() => handleJumpAndScrollVideo(sh.timestamp_s)}
                              >
                                <line x1={sx} y1={sy} x2={gx} y2={gy} stroke={col} strokeWidth="2.4" />
                                {sh.is_suboptimal && sh.better_option && (
                                  <line
                                    x1={sx}
                                    y1={sy}
                                    x2={toX(sh.better_option.x_norm)}
                                    y2={toY(sh.better_option.y_norm)}
                                    stroke="#fde047"
                                    strokeWidth="2.8"
                                    strokeDasharray="6 3"
                                    markerEnd="url(#aiArrowGold)"
                                  />
                                )}
                                <circle cx={sx} cy={sy} r="9" fill={col} stroke="#ffffff" strokeWidth="2" />
                                <text x={sx} y={sy + 3.5} fill="#ffffff" fontSize="9" fontWeight="900" textAnchor="middle">
                                  #{sh.shooter_shirt}
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'team_shape') {
                  const t0 = pm.team_0;
                  const t1 = pm.team_1;
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#38bdf8"
                      icon={Shield}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#38bdf8', label: `${t0?.short_name || 'Home'} Units (${t0?.dominant_shape || 'Shape'})` },
                        { color: '#ef4444', label: `${t1?.short_name || 'Away'} Units (${t1?.dominant_shape || 'Shape'})` },
                      ]}
                    >
                      {({ toX, toY, pad, innerW, innerH }) => (
                        <g>
                          {[t0, t1].filter(Boolean).map((tm, tIdx) => {
                            const isHome = tIdx === 0;
                            const color = tm.color || (isHome ? '#38bdf8' : '#ef4444');

                            // Backline coords
                            const bx = toX(tm.backline.x_m / 105.0);
                            const by1 = toY(tm.backline.y_min_m / 68.0);
                            const by2 = toY(tm.backline.y_max_m / 68.0);

                            // Midfield coords
                            const mx = toX(tm.midfield_line.x_m / 105.0);
                            const my1 = toY(tm.midfield_line.y_min_m / 68.0);
                            const my2 = toY(tm.midfield_line.y_max_m / 68.0);

                            // Frontline coords
                            const fx = toX(tm.frontline.x_m / 105.0);
                            const fy1 = toY(tm.frontline.y_min_m / 68.0);
                            const fy2 = toY(tm.frontline.y_max_m / 68.0);

                            return (
                              <g key={tIdx}>
                                {/* Block Depth Polygon Hull */}
                                <polygon
                                  points={`${bx},${by1} ${fx},${fy1} ${fx},${fy2} ${bx},${by2}`}
                                  fill={color}
                                  fillOpacity="0.08"
                                  stroke={color}
                                  strokeWidth="1.2"
                                  strokeDasharray="4 4"
                                />

                                {/* Defensive Backline */}
                                <line x1={bx} y1={by1} x2={bx} y2={by2} stroke={color} strokeWidth="3.6" strokeDasharray="8 5" />
                                <text x={bx} y={Math.min(by1, by2) - 6} fill="#ffffff" fontSize="9.5" fontWeight="800" textAnchor="middle">
                                  {tm.short_name} Backline ({tm.backline.height_m}m)
                                </text>

                                {/* Midfield Unit Line */}
                                <line x1={mx} y1={my1} x2={mx} y2={my2} stroke={color} strokeWidth="2.8" opacity="0.85" />
                                <text x={mx} y={Math.max(my1, my2) + 14} fill={color} fontSize="8.5" fontWeight="700" textAnchor="middle">
                                  Midfield (+{tm.midfield_line.separation_to_backline_m}m)
                                </text>

                                {/* Attacking Frontline */}
                                <line x1={fx} y1={fy1} x2={fx} y2={fy2} stroke={color} strokeWidth="2.2" strokeDasharray="4 3" opacity="0.75" />
                                <text x={fx} y={Math.min(fy1, fy2) - 6} fill={color} fontSize="8.5" fontWeight="700" textAnchor="middle">
                                  Frontline (+{tm.frontline.separation_to_midfield_m}m)
                                </text>

                                {/* Block Depth HUD Pill */}
                                <rect
                                  x={(bx + fx) / 2 - 45}
                                  y={pad + innerH / 2 + (isHome ? -22 : 8)}
                                  width="90"
                                  height="18"
                                  rx="4"
                                  fill="rgba(15, 23, 42, 0.88)"
                                  stroke={color}
                                  strokeWidth="1"
                                />
                                <text
                                  x={(bx + fx) / 2}
                                  y={pad + innerH / 2 + (isHome ? -10 : 20)}
                                  fill="#ffffff"
                                  fontSize="8.5"
                                  fontWeight="700"
                                  textAnchor="middle"
                                >
                                  Depth: {tm.total_block_depth_m}m
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                if (pm.type === 'def_shape' && pm.defensive_shape) {
                  return (
                    <AIPitchCanvas
                      key={pm.id}
                      title={pm.title}
                      subtitle={pm.subtitle}
                      badgeText={pm.badge}
                      badgeColor="#2563eb"
                      icon={Shield}
                      isExpanded={expandedPitchId === pm.id}
                      onToggleExpand={() => handleToggleExpand(pm.id)}
                      legendItems={[
                        { color: '#38bdf8', label: 'Home Backline' },
                        { color: '#ef4444', label: 'Away Backline' },
                      ]}
                    >
                      {({ toX, pad, innerH }) => (
                        <g>
                          {Object.values(pm.defensive_shape).map((rep, idx) => {
                            const normH = (rep.avg_line_height_m || 40) / 105.0;
                            const xPos = toX(rep.team_id === 0 ? normH : 1.0 - normH);
                            const col = rep.team_id === 0 ? '#38bdf8' : '#ef4444';
                            return (
                              <g key={idx}>
                                <line x1={xPos} y1={pad + 20} x2={xPos} y2={pad + innerH - 20} stroke={col} strokeWidth="3" strokeDasharray="8 5" />
                                <text x={xPos} y={pad + 16} fill="#ffffff" fontSize="10" fontWeight="800" textAnchor="middle">
                                  {rep.team_short} ({rep.avg_line_height_m}m)
                                </text>
                              </g>
                            );
                          })}
                        </g>
                      )}
                    </AIPitchCanvas>
                  );
                }

                return null;
              })}
            </div>
          )}

          {/* D2. Team Shape & Line Analysis Table */}
          {coachAiReport?.teams_summary_table?.length > 0 && (
            <div className="ai-detail-panel-card">
              <div className="ai-detail-card-title">
                <Shield size={16} color="#38bdf8" />
                <span>
                  {coachAiReport?.is_all_games
                    ? 'Multi-Match Team Shape Architecture & Unit Lines (All 4 Games — 8 Teams Analyzed)'
                    : 'Team Shape & Spatial Unit Lines Analysis'}
                </span>
              </div>
              <div className="ai-speed-table-wrapper">
                <table className="ai-clean-table">
                  <thead>
                    <tr>
                      <th>Team</th>
                      <th>Dominant Tactical Archetype</th>
                      <th>Defensive Line (Backline)</th>
                      <th>Midfield Unit Line</th>
                      <th>Attacking Frontline</th>
                      <th>Total Block Depth</th>
                      <th>Shape Distribution Breakdown (6 Archetypes)</th>
                    </tr>
                  </thead>
                  <tbody>
                    {coachAiReport.teams_summary_table.map((tm, idx) => (
                      <tr key={idx}>
                        <td>
                          <strong>{tm.team_name}</strong>
                          {tm.match_name && <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>{tm.match_name}</div>}
                        </td>
                        <td>
                          <span className="badge-pill" style={{ color: '#38bdf8', borderColor: 'rgba(56, 189, 248, 0.4)' }}>
                            {tm.dominant_shape}
                          </span>
                        </td>
                        <td>
                          <strong>{tm.backline_height_m}m</strong> from goal
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Width: {tm.backline_width_m}m</div>
                        </td>
                        <td>
                          <strong>{tm.midfield_sep_m}m</strong> gap to backline
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Width: {tm.midfield_width_m}m</div>
                        </td>
                        <td>
                          <strong>{tm.attack_sep_m}m</strong> gap to midfield
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Width: {tm.attack_width_m}m</div>
                        </td>
                        <td>
                          <strong style={{ color: tm.total_block_depth_m < 20 ? '#10b981' : '#f59e0b' }}>
                            {tm.total_block_depth_m}m
                          </strong>
                          <div style={{ fontSize: 10, color: 'var(--text-muted)' }}>Radius: {tm.compactness_radius_m}m</div>
                        </td>
                        <td>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: 2, fontSize: 10 }}>
                            <span>Press: {tm.distribution?.high_press_front_aggression ?? 0}% • Mid: {tm.distribution?.compact_mid_block ?? 0}% • Low: {tm.distribution?.deep_low_block ?? 0}%</span>
                            <span style={{ color: 'var(--text-muted)' }}>Overload: {tm.distribution?.asymmetric_flank_overload ?? 0}% • Rest: {tm.distribution?.counter_attack_rest_defense ?? 0}% • Pos: {tm.distribution?.positional_possession_expansion ?? 0}%</span>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* E. Multi-Opponent On-Ball 1v1 & Speed Comparison Table */}
          {(coachAiReport?.duels_list?.length > 0 || speedComp) && (
            <div className="ai-detail-panel-card">
              <div className="ai-detail-card-title">
                <Gauge size={16} color="#2563eb" />
                <span>
                  Strict On-Ball 1v1 Duels & Speed Comparison Summary
                </span>
              </div>
              <div className="ai-speed-table-wrapper">
                <table className="ai-clean-table">
                  <thead>
                    <tr>
                      <th>Matchup (Attacker with Ball vs Defender)</th>
                      <th>On-Ball 1v1 Duels</th>
                      <th>Attacker Beat Man (Dribble Complete)</th>
                      <th>Defender Stops (Ball Won / Contained)</th>
                      <th>Peak Speed (90m)</th>
                      <th>1v1 Duel Avg Speed</th>
                    </tr>
                  </thead>
                  <tbody>
                    {(coachAiReport?.duels_list?.length > 0 ? coachAiReport.duels_list : [duelData]).filter(Boolean).map((dItem, idx) => {
                      const sc = dItem.speed_comparison || {};
                      return (
                        <tr key={idx}>
                          <td>
                            <strong>#{dItem.attacker.shirt} {dItem.attacker.name}</strong> vs <strong>#{dItem.defender.shirt} {dItem.defender.name}</strong>
                          </td>
                          <td><strong>{dItem.total_1v1_duels}</strong> on-ball duels</td>
                          <td style={{ color: '#16a34a', fontWeight: 700 }}>
                            {dItem.attacker_wins} Beat Man ({dItem.attacker_success_pct}%)
                          </td>
                          <td style={{ color: '#dc2626', fontWeight: 700 }}>
                            {dItem.defender_duels_won != null ? (
                              <span>
                                {dItem.defender_duels_won} Won Ball ({dItem.defender_duels_won_pct}%) • {dItem.defender_containments} Contained
                              </span>
                            ) : (
                              <span>{dItem.defender_containments} Lost ({dItem.defender_containment_pct}%)</span>
                            )}
                          </td>
                          <td>{sc.p1_top_speed_kmh} vs {sc.p2_top_speed_kmh} km/h</td>
                          <td>{sc.p1_h2h_avg_kmh} vs {sc.p2_h2h_avg_kmh} km/h</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* F. Shot Decision Audit Breakdown (Optimal vs Non-Optimal Shots) */}
          {coachAiReport?.shot_audit?.shots?.length > 0 && (
            <div className="ai-detail-panel-card">
              <div className="ai-detail-card-title">
                <Target size={16} color="#dc2626" />
                <span>
                  Shot & Box Strike Decision Audit — {coachAiReport.shot_audit.optimal_shots_count} Optimal vs {coachAiReport.shot_audit.suboptimal_shots_count} Non-Optimal
                </span>
              </div>
              <div className="ai-speed-table-wrapper">
                <table className="ai-clean-table">
                  <thead>
                    <tr>
                      <th>Match Clock</th>
                      <th>Player</th>
                      <th>Distance & Angle</th>
                      <th>Decision Verdict</th>
                      <th>Tactical Rationale & Better Option</th>
                    </tr>
                  </thead>
                  <tbody>
                    {coachAiReport.shot_audit.shots.map((sh, idx) => (
                      <tr key={idx}>
                        <td>
                          <button
                            type="button"
                            className="jump-time-chip"
                            onClick={() => handleJumpAndScrollVideo(sh.timestamp_s)}
                          >
                            <Play size={9} /> {sh.clock} ({sh.half})
                          </button>
                        </td>
                        <td><strong>#{sh.shooter_shirt} {sh.shooter_name}</strong></td>
                        <td>{sh.distance_m}m • {sh.angle_deg}° ({sh.blockers_in_cone} blockers)</td>
                        <td style={{ color: sh.is_suboptimal ? '#dc2626' : '#16a34a', fontWeight: 700 }}>
                          {sh.is_suboptimal ? 'Non-Optimal' : 'Optimal'}
                        </td>
                        <td>{sh.rationale}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* F. Single-Player Relational Breakdown (Only shown when single player queried and relevant) */}
          {!speedComp && primaryProfile && (intents.includes('passes') || intents.includes('overlaps') || intents.includes('defenders') || intents.includes('runs')) && (
            <div className="ai-deep-stats-columns">
              {(intents.includes('passes') || intents.includes('runs')) && primaryProfile.pass_providers_on_runs?.length > 0 && (
                <div className="ai-detail-panel-card">
                  <div className="ai-detail-card-title">
                    <Zap size={15} color="#2563eb" />
                    <span>Top Pass Providers on #{primaryProfile.player.shirt} {primaryProfile.player.name}'s Runs</span>
                  </div>
                  {primaryProfile.pass_providers_on_runs.map((pp, i) => (
                    <div key={i} className="ai-stat-row-item">
                      <div>
                        <strong>#{pp.shirt} {pp.name}</strong> <span className="muted-tag">({pp.pos})</span>
                      </div>
                      <div className="ai-stat-row-right">
                        <span className="badge-pill">{pp.passes_on_runs} passes</span>
                        {pp.timestamps?.map((ts, ti) => (
                          <button key={ti} type="button" className="jump-time-chip" onClick={() => handleJumpAndScrollVideo(ts)}>
                            <Play size={9} /> @{ts}s
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {intents.includes('defenders') && primaryProfile.primary_defenders?.length > 0 && (
                <div className="ai-detail-panel-card">
                  <div className="ai-detail-card-title">
                    <Shield size={15} color="#ef4444" />
                    <span>Primary Defenders Marking #{primaryProfile.player.shirt} {primaryProfile.player.name}</span>
                  </div>
                  {primaryProfile.primary_defenders.map((df, i) => (
                    <div key={i} className="ai-stat-row-item">
                      <div>
                        <strong>#{df.shirt} {df.name}</strong> <span className="muted-tag">({df.pos})</span>
                      </div>
                      <div className="ai-stat-row-right">
                        <span className="badge-pill">{df.marking_time_s}s ({df.avg_marking_dist_m}m avg)</span>
                        {df.timestamps?.map((ts, ti) => (
                          <button key={ti} type="button" className="jump-time-chip" onClick={() => handleJumpAndScrollVideo(ts)}>
                            <Play size={9} /> @{ts}s
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
}
