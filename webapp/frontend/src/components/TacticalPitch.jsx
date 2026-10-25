import React, { useState } from 'react';
import { 
  Users, 
  Shield, 
  Compass, 
  Layers, 
  Eye, 
  EyeOff, 
  Target, 
  ArrowUpRight,
  Maximize2,
  RefreshCw
} from 'lucide-react';

export default function TacticalPitch({
  overlayData,
  selectedPlayerIds = [],
  onTogglePlayerSelection,
  onClearSelection,
  currentTime = 0,
  highlightedReceiverId = null,
}) {
  // Layer visibility toggles
  const [toggles, setToggles] = useState({
    numbers: true,
    names: true,
    lanes: true,
    space: true,
    vectors: true,
  });

  const [isPitchExpanded, setIsPitchExpanded] = useState(false);
  const [hoveredPlayer, setHoveredPlayer] = useState(null);

  const toggleLayer = (key) => {
    setToggles((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const players = overlayData?.players || [];
  const passingLanes = overlayData?.passing_lanes || [];
  const spaceOpps = overlayData?.space_opportunities || [];
  const teamShape = overlayData?.team_shape || {};
  const carrierId = overlayData?.ball_carrier;

  // SVG dimensions: standard 105m x 68m pitch scaled x10 -> 1050 x 680
  const pitchWidth = 1050;
  const pitchHeight = 680;
  const pad = 25;
  const innerW = pitchWidth - pad * 2; // 1000
  const innerH = pitchHeight - pad * 2; // 630

  // Coordinate mapping from normalized [0..1] to SVG pixels
  const toX = (normX) => pad + (normX ?? 0.5) * innerW;
  const toY = (normY) => pad + (normY ?? 0.5) * innerH;

  // Dynamic team colors from match metadata
  const team0Color = players.find((p) => p.team === 0)?.accent_color || '#00e5ff';
  const team1Color = players.find((p) => p.team === 1)?.accent_color || '#ef4444';

  // Defensive line calculations
  const t0Backline = teamShape?.team_0?.backline;
  const t1Backline = teamShape?.team_1?.backline;

  // Convex hull polygons
  const t0Hull = teamShape?.team_0?.convex_hull_normalized || [];
  const t1Hull = teamShape?.team_1?.convex_hull_normalized || [];

  return (
    <div className="tactical-pitch-card">
      {/* Pitch Header & Layer Toggles Bar */}
      <div className="tactical-pitch-toolbar">
        <div className="pitch-toolbar-title">
          <Compass size={15} color="var(--accent-cyan)" />
          <span style={{ fontWeight: 700, fontSize: 13, letterSpacing: '0.5px' }}>
            2D TACTICAL PITCH
          </span>
          <span className="pitch-live-badge">
            {players.length > 0 ? `SYNCHRONIZED (${players.length} PLAYERS)` : 'CALIBRATING'}
          </span>
        </div>

        {/* Layer Toggles */}
        <div className="pitch-toggle-group">
          <button
            className={`pitch-pill-btn ${toggles.names ? 'active' : ''}`}
            onClick={() => toggleLayer('names')}
            title="Toggle Player Names"
          >
            <span>Names</span>
          </button>
          <button
            className={`pitch-pill-btn ${toggles.lanes ? 'active' : ''}`}
            onClick={() => toggleLayer('lanes')}
            title="Toggle Passing Lanes"
          >
            <span>Lanes</span>
          </button>
          <button
            className={`pitch-pill-btn ${toggles.space ? 'active' : ''}`}
            onClick={() => toggleLayer('space')}
            title="Toggle Space Pockets & Corridors"
          >
            <span>Spaces</span>
          </button>
          <button
            className={`pitch-pill-btn ${toggles.vectors ? 'active' : ''}`}
            onClick={() => toggleLayer('vectors')}
            title="Toggle Velocity Direction Vectors"
          >
            <span>Vectors</span>
          </button>
          <button
            className={`pitch-pill-btn ${isPitchExpanded ? 'active' : ''}`}
            onClick={() => setIsPitchExpanded((prev) => !prev)}
            title="Toggle Extra-Large 2D Pitch Height"
          >
            <Maximize2 size={10} style={{ marginRight: 3, verticalAlign: 'middle' }} />
            <span>{isPitchExpanded ? 'Standard Size' : 'XL Pitch'}</span>
          </button>
          {selectedPlayerIds.length > 0 && (
            <button
              className="pitch-pill-btn clear-selection-btn"
              onClick={onClearSelection}
              title="Clear Selected Players"
            >
              <span>Clear ({selectedPlayerIds.length})</span>
            </button>
          )}
        </div>
      </div>

      {/* Interactive SVG Pitch Stage */}
      <div className={`pitch-stage-wrapper ${isPitchExpanded ? 'pitch-expanded' : ''}`}>
        <svg
          viewBox={`0 0 ${pitchWidth} ${pitchHeight}`}
          className="tactical-pitch-svg"
          preserveAspectRatio="xMidYMid meet"
        >
          <defs>
            {/* Pitch turf grass stripes gradient */}
            <linearGradient id="turfGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#14532d" />
              <stop offset="50%" stopColor="#166534" />
              <stop offset="100%" stopColor="#134e2a" />
            </linearGradient>

            {/* Alternating lawn mow stripes pattern */}
            <pattern id="pitchStripes" width="100" height="680" patternUnits="userSpaceOnUse">
              <rect x="0" y="0" width="50" height="680" fill="#15803d" opacity="0.28" />
              <rect x="50" y="0" width="50" height="680" fill="#14532d" opacity="0.38" />
            </pattern>

            {/* Passing lane arrow markers */}
            <marker id="arrowClear" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#10b981" />
            </marker>
            <marker id="arrowContested" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#f59e0b" />
            </marker>
            <marker id="arrowBlocked" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#ef4444" />
            </marker>
            <marker id="arrowRunCyan" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#38bdf8" />
            </marker>
            <marker id="arrowRunGold" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
              <path d="M0,0 L6,3 L0,6 Z" fill="#fde047" />
            </marker>

            {/* Glow filter for selected players */}
            <filter id="goldGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="4" result="blur" />
              <feMerge>
                <feMergeNode in="blur" />
                <feMergeNode in="SourceGraphic" />
              </feMerge>
            </filter>
          </defs>

          {/* 1. Base Turf & Markings */}
          <rect x="0" y="0" width={pitchWidth} height={pitchHeight} fill="url(#turfGradient)" />
          <rect x={pad} y={pad} width={innerW} height={innerH} fill="url(#pitchStripes)" />

          {/* Pitch Outer Boundary Line */}
          <rect
            x={pad}
            y={pad}
            width={innerW}
            height={innerH}
            fill="none"
            stroke="rgba(255, 255, 255, 0.72)"
            strokeWidth="2.5"
            rx="4"
          />

          {/* Halfway Line */}
          <line
            x1={pad + innerW / 2}
            y1={pad}
            x2={pad + innerW / 2}
            y2={pad + innerH}
            stroke="rgba(255, 255, 255, 0.72)"
            strokeWidth="2.0"
          />

          {/* Center Circle & Center Spot */}
          <circle
            cx={pad + innerW / 2}
            cy={pad + innerH / 2}
            r="85"
            fill="none"
            stroke="rgba(255, 255, 255, 0.72)"
            strokeWidth="2.0"
          />
          <circle
            cx={pad + innerW / 2}
            cy={pad + innerH / 2}
            r="3.5"
            fill="rgba(255, 255, 255, 0.85)"
          />

          {/* Left Penalty Area (16.5m box) */}
          <rect
            x={pad}
            y={pad + innerH * 0.21}
            width={innerW * 0.16}
            height={innerH * 0.58}
            fill="none"
            stroke="rgba(255, 255, 255, 0.72)"
            strokeWidth="2.0"
          />
          {/* Left Goal Area (5.5m box) */}
          <rect
            x={pad}
            y={pad + innerH * 0.36}
            width={innerW * 0.055}
            height={innerH * 0.28}
            fill="none"
            stroke="rgba(255, 255, 255, 0.68)"
            strokeWidth="1.8"
          />
          {/* Left Penalty Spot */}
          <circle
            cx={pad + innerW * 0.11}
            cy={pad + innerH * 0.5}
            r="3.5"
            fill="rgba(255, 255, 255, 0.85)"
          />

          {/* Right Penalty Area (16.5m box) */}
          <rect
            x={pad + innerW * 0.84}
            y={pad + innerH * 0.21}
            width={innerW * 0.16}
            height={innerH * 0.58}
            fill="none"
            stroke="rgba(255, 255, 255, 0.72)"
            strokeWidth="2.0"
          />
          {/* Right Goal Area (5.5m box) */}
          <rect
            x={pad + innerW * 0.945}
            y={pad + innerH * 0.36}
            width={innerW * 0.055}
            height={innerH * 0.28}
            fill="none"
            stroke="rgba(255, 255, 255, 0.68)"
            strokeWidth="1.8"
          />
          {/* Right Penalty Spot */}
          <circle
            cx={pad + innerW * 0.89}
            cy={pad + innerH * 0.5}
            r="3.5"
            fill="rgba(255, 255, 255, 0.85)"
          />

          {/* Goals outside pitch */}
          <rect x={pad - 12} y={pad + innerH * 0.44} width="12" height={innerH * 0.12} fill="rgba(255, 255, 255, 0.18)" stroke="rgba(255, 255, 255, 0.78)" strokeWidth="1.5" />
          <rect x={pad + innerW} y={pad + innerH * 0.44} width="12" height={innerH * 0.12} fill="rgba(255, 255, 255, 0.18)" stroke="rgba(255, 255, 255, 0.78)" strokeWidth="1.5" />

          {/* Corner Arcs */}
          <path d={`M ${pad + 15} ${pad} A 15 15 0 0 1 ${pad} ${pad + 15}`} fill="none" stroke="rgba(255, 255, 255, 0.72)" strokeWidth="1.8" />
          <path d={`M ${pad + innerW - 15} ${pad} A 15 15 0 0 0 ${pad + innerW} ${pad + 15}`} fill="none" stroke="rgba(255, 255, 255, 0.72)" strokeWidth="1.8" />
          <path d={`M ${pad + 15} ${pad + innerH} A 15 15 0 0 0 ${pad} ${pad + innerH - 15}`} fill="none" stroke="rgba(255, 255, 255, 0.72)" strokeWidth="1.8" />
          <path d={`M ${pad + innerW - 15} ${pad + innerH} A 15 15 0 0 1 ${pad + innerW} ${pad + innerH - 15}`} fill="none" stroke="rgba(255, 255, 255, 0.72)" strokeWidth="1.8" />

          {/* 2. Team Shape Convex Hulls */}
          {toggles.teamShape && (
            <>
              {t0Hull.length >= 3 && (
                <polygon
                  points={t0Hull.map(([x, y]) => `${toX(x)},${toY(y)}`).join(' ')}
                  fill="rgba(0, 229, 255, 0.08)"
                  stroke="rgba(0, 229, 255, 0.45)"
                  strokeWidth="1.5"
                  strokeDasharray="4 2"
                />
              )}
              {t1Hull.length >= 3 && (
                <polygon
                  points={t1Hull.map(([x, y]) => `${toX(x)},${toY(y)}`).join(' ')}
                  fill="rgba(239, 68, 68, 0.08)"
                  stroke="rgba(239, 68, 68, 0.45)"
                  strokeWidth="1.5"
                  strokeDasharray="4 2"
                />
              )}
            </>
          )}

          {/* 3. Space Opportunities / Tactical Pockets */}
          {toggles.space && spaceOpps.map((opp, idx) => {
            const ox = toX(opp.target_x_norm);
            const oy = toY(opp.target_y_norm);
            return (
              <g key={idx} className="space-opp-group">
                <circle
                  cx={ox}
                  cy={oy}
                  r="34"
                  fill="rgba(56, 189, 248, 0.12)"
                  stroke="rgba(56, 189, 248, 0.5)"
                  strokeWidth="1.5"
                  strokeDasharray="4 3"
                />
                <text
                  x={ox}
                  y={oy + 4}
                  fill="#7dd3fc"
                  fontSize="10"
                  fontWeight="600"
                  textAnchor="middle"
                  style={{ pointerEvents: 'none' }}
                >
                  {opp.label}
                </text>
              </g>
            );
          })}

          {/* 4. Defensive Lines & Gaps */}
          {toggles.defLine && (
            <>
              {t0Backline && t0Backline.line_height_m && (
                <g>
                  <line
                    x1={toX(t0Backline.line_height_m / 105.0)}
                    y1={pad + 20}
                    x2={toX(t0Backline.line_height_m / 105.0)}
                    y2={pad + innerH - 20}
                    stroke="rgba(255, 51, 75, 0.65)"
                    strokeWidth="1.8"
                    strokeDasharray="6 4"
                  />
                  <text
                    x={toX(t0Backline.line_height_m / 105.0)}
                    y={pad + 15}
                    fill="#ff334b"
                    fontSize="9"
                    fontWeight="700"
                    textAnchor="middle"
                  >
                    DEF LINE {t0Backline.dist_from_own_goal_m}m
                  </text>
                </g>
              )}
              {t1Backline && t1Backline.line_height_m && (
                <g>
                  <line
                    x1={toX(t1Backline.line_height_m / 105.0)}
                    y1={pad + 20}
                    x2={toX(t1Backline.line_height_m / 105.0)}
                    y2={pad + innerH - 20}
                    stroke="rgba(0, 229, 255, 0.65)"
                    strokeWidth="1.8"
                    strokeDasharray="6 4"
                  />
                  <text
                    x={toX(t1Backline.line_height_m / 105.0)}
                    y={pad + 15}
                    fill="#00e5ff"
                    fontSize="9"
                    fontWeight="700"
                    textAnchor="middle"
                  >
                    DEF LINE {t1Backline.dist_from_own_goal_m}m
                  </text>
                </g>
              )}
            </>
          )}

          {/* 5. Passing Lanes */}
          {toggles.lanes && passingLanes.map((lane, idx) => {
            const x1 = toX(lane.from_x_norm);
            const y1 = toY(lane.from_y_norm);
            const x2 = toX(lane.to_x_norm);
            const y2 = toY(lane.to_y_norm);
            const isHighlighted = lane.receiver_id === highlightedReceiverId;
            const markerId = 
              lane.interception_risk === 'Low' || lane.lane_status === 'open' ? 'url(#arrowClear)' :
              lane.interception_risk === 'Contested' || lane.lane_status === 'contested' ? 'url(#arrowContested)' : 'url(#arrowBlocked)';

            return (
              <g key={lane.receiver_id || idx} className={`passing-lane-vector ${isHighlighted ? 'highlighted-lane' : ''}`}>
                {/* Subtle outer glow line for open or highlighted lanes */}
                {(isHighlighted || lane.lane_status === 'open') && (
                  <line
                    x1={x1}
                    y1={y1}
                    x2={x2}
                    y2={y2}
                    stroke={isHighlighted ? '#ffffff' : lane.risk_color}
                    strokeWidth={isHighlighted ? 8 : 5}
                    opacity={isHighlighted ? 0.25 : 0.14}
                    strokeLinecap="round"
                  />
                )}
                <line
                  x1={x1}
                  y1={y1}
                  x2={x2}
                  y2={y2}
                  className={lane.lane_status !== 'blocked' ? 'flowing-lane-stroke' : ''}
                  stroke={isHighlighted ? '#ffffff' : lane.risk_color}
                  strokeWidth={isHighlighted ? 3.8 : (lane.composite_score > 0.6 ? 2.6 : 1.9)}
                  strokeDasharray={lane.is_hypothetical ? "8 4" : (lane.lane_status === 'blocked' ? "4 4" : "10 5")}
                  markerEnd={markerId}
                  opacity={isHighlighted ? 1.0 : (highlightedReceiverId ? 0.35 : 0.88)}
                />
                {/* Midpoint clearance tag */}
                <g
                  style={{
                    transform: `translate(${(x1 + x2) / 2}px, ${(y1 + y2) / 2}px)`,
                    transition: 'transform 140ms cubic-bezier(0.22, 1, 0.36, 1)',
                  }}
                >
                  <rect
                    x="-21"
                    y="-8"
                    width="42"
                    height="16"
                    rx="4"
                    fill="rgba(9, 15, 28, 0.92)"
                    stroke={isHighlighted ? '#ffffff' : lane.risk_color}
                    strokeWidth={isHighlighted ? 1.8 : 1.1}
                    opacity={isHighlighted ? 1.0 : (highlightedReceiverId ? 0.35 : 0.9)}
                  />
                  <text
                    x="0"
                    y="3"
                    fill="#ffffff"
                    fontSize="9"
                    fontWeight="700"
                    fontFamily="monospace"
                    textAnchor="middle"
                    opacity={isHighlighted ? 1.0 : (highlightedReceiverId ? 0.35 : 0.95)}
                  >
                    {lane.corridor_clearance_m ? `${lane.corridor_clearance_m}m` : 'Clear'}
                  </text>
                </g>
              </g>
            );
          })}

          {/* 6.5 Multi-Player Selection Line / Polygon on 2D Pitch */}
          {selectedPlayerIds.length === 2 && overlayData?.selection_analysis?.line_norm?.length === 2 && (
            <line
              x1={toX(overlayData.selection_analysis.line_norm[0][0])}
              y1={toY(overlayData.selection_analysis.line_norm[0][1])}
              x2={toX(overlayData.selection_analysis.line_norm[1][0])}
              y2={toY(overlayData.selection_analysis.line_norm[1][1])}
              className="flowing-lane-stroke"
              stroke="#fde047"
              strokeWidth="2.4"
              strokeDasharray="7 4"
              opacity="0.92"
            />
          )}
          {selectedPlayerIds.length >= 3 && overlayData?.selection_analysis?.group_hull_norm?.length >= 3 && (
            <polygon
              points={overlayData.selection_analysis.group_hull_norm.map(([x, y]) => `${toX(x)},${toY(y)}`).join(' ')}
              fill="rgba(253, 224, 71, 0.12)"
              stroke="#fde047"
              strokeWidth="1.8"
              strokeDasharray="5 3"
            />
          )}

          {/* 6. Players (Compositor-Accelerated Smooth Gliding Nodes) */}
          {players.map((p) => {
            if (!p.has_pitch) return null;
            const px = toX(p.pitch_x);
            const py = toY(p.pitch_y);
            const isSelected = selectedPlayerIds.includes(p.player_id);
            const isCarrier = p.is_carrier || (carrierId && p.player_id === carrierId);
            const isTeam0 = p.team === 0;
            const teamColor = p.accent_color || (isTeam0 ? team0Color : team1Color);
            const teamFill = p.kit_color || (isTeam0 ? '#ffffff' : '#1e293b');
            const pRadius = 14;

            // Heading vector length based on real physical speed (0..10 m/s)
            const speed = (p.speed_valid && p.speed_mps) ? p.speed_mps : 0;
            const vecLen = Math.min(32, Math.max(10, speed * 2.8));
            const vx = Math.cos(p.heading_rad || 0) * vecLen;
            const vy = Math.sin(p.heading_rad || 0) * vecLen;

            // Smart contrast for jersey numbers
            const isDarkJersey = teamFill === '#1e293b' || teamFill === '#0f172a' || teamFill === '#991b1b' || teamFill === '#15803d' || teamFill === '#2563eb';
            const shirtTextColor = isCarrier ? '#080b11' : (isDarkJersey ? '#ffffff' : '#080b11');

            return (
              <g
                key={p.player_id}
                className={`pitch-player-node ${isSelected ? 'is-selected' : ''} ${isCarrier ? 'is-carrier' : ''}`}
                style={{
                  transform: `translate(${px}px, ${py}px)`,
                  cursor: 'pointer',
                }}
                onClick={() => onTogglePlayerSelection(p.player_id)}
                onMouseEnter={() => setHoveredPlayer(p)}
                onMouseLeave={() => setHoveredPlayer(null)}
              >
                {/* Directional Velocity Vector Arrow */}
                {toggles.vectors && speed > 0.4 && (
                  <line
                    x1={0}
                    y1={0}
                    x2={vx}
                    y2={vy}
                    stroke={teamColor}
                    strokeWidth="2.2"
                    opacity="0.88"
                    strokeLinecap="round"
                  />
                )}

                {/* Selected Player Halo Glow */}
                {isSelected && (
                  <>
                    <circle
                      cx={0}
                      cy={0}
                      r={pRadius + 9}
                      fill="none"
                      stroke="#fde047"
                      strokeWidth="2.0"
                      strokeDasharray="4 2"
                      className="rotating-halo-ring"
                      filter="url(#goldGlow)"
                    />
                    <circle
                      cx={0}
                      cy={0}
                      r={pRadius + 4}
                      fill="rgba(253, 224, 71, 0.25)"
                      stroke="#fde047"
                      strokeWidth="2.0"
                    />
                  </>
                )}

                {/* Ball Carrier Radiant Aura */}
                {isCarrier && !isSelected && (
                  <circle
                    cx={0}
                    cy={0}
                    r={pRadius + 6}
                    className="carrier-pulse-ring"
                    fill="rgba(245, 158, 11, 0.28)"
                    stroke="#f59e0b"
                    strokeWidth="2.2"
                  />
                )}

                {/* Base Player Circle */}
                <circle
                  cx={0}
                  cy={0}
                  r={pRadius}
                  className="pitch-player-disc"
                  fill={isCarrier ? '#f59e0b' : teamFill}
                  stroke={teamColor}
                  strokeWidth="2.2"
                />

                {/* Shirt Number */}
                {toggles.numbers && (
                  <text
                    x={0}
                    y={4}
                    fill={shirtTextColor}
                    fontSize="11"
                    fontWeight="800"
                    fontFamily="monospace"
                    textAnchor="middle"
                    style={{ userSelect: 'none', pointerEvents: 'none' }}
                  >
                    {p.shirt || p.player_id}
                  </text>
                )}

                {/* Player Name Pill */}
                {toggles.names && (
                  <g transform={`translate(0, ${-pRadius - 8})`}>
                    <rect
                      x="-33"
                      y="-12"
                      width="66"
                      height="14"
                      rx="4"
                      fill="rgba(10, 16, 30, 0.9)"
                      stroke={teamColor}
                      strokeWidth="0.9"
                    />
                    <text
                      x="0"
                      y="-2"
                      fill="#ffffff"
                      fontSize="9"
                      fontWeight="600"
                      textAnchor="middle"
                      style={{ userSelect: 'none', pointerEvents: 'none' }}
                    >
                      {p.name?.split(' ').pop() || `#${p.shirt}`}
                    </text>
                  </g>
                )}
              </g>
            );
          })}

          {/* 7. Shooting Corridors on 2D Pitch */}
          {overlayData?.shooting_options?.viable && (overlayData.shooting_options.target_corridors || overlayData.shooting_options.corridors) && (
            <g className="pitch-shooting-corridors">
              {(overlayData.shooting_options.target_corridors || overlayData.shooting_options.corridors).map((corr, idx) => {
                const sx = toX(corr.from_x_norm);
                const sy = toY(corr.from_y_norm);
                const tx = toX(corr.to_x_norm);
                const ty = toY(corr.to_y_norm);
                const color = corr.status_color || (corr.obstruction === 'clear' ? '#10b981' : corr.obstruction === 'blocked' ? '#ef4444' : '#f59e0b');
                return (
                  <g key={idx}>
                    <line
                      x1={sx}
                      y1={sy}
                      x2={tx}
                      y2={ty}
                      className="flowing-lane-stroke"
                      stroke={color}
                      strokeWidth="2.2"
                      strokeDasharray="7 4"
                      opacity="0.92"
                    />
                    <circle cx={tx} cy={ty} r="4.5" fill={color} stroke="#ffffff" strokeWidth="1.2" />
                  </g>
                );
              })}
            </g>
          )}

          {/* 8. Ball Marker on 2D Pitch (Smooth Gliding Node) */}
          {overlayData?.ball && overlayData.ball.pitch_x !== undefined && overlayData.ball.pitch_x !== null && overlayData.ball.status === 'detected' && overlayData.ball.is_reliable !== false && (
            <g
              className="pitch-ball-node"
              style={{
                transform: `translate(${toX(overlayData.ball.pitch_x)}px, ${toY(overlayData.ball.pitch_y)}px)`,
              }}
            >
              <circle
                cx={0}
                cy={0}
                r="9"
                fill="rgba(0, 255, 157, 0.28)"
              />
              <circle
                cx={0}
                cy={0}
                r="4.8"
                fill="#00ff9d"
                stroke="#ffffff"
                strokeWidth="1.6"
              />
            </g>
          )}
        </svg>

        {/* Hovered Player Interactive HUD Card */}
        {hoveredPlayer && (
          <div className="pitch-hover-hud">
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  backgroundColor: hoveredPlayer.team === 0 ? team0Color : team1Color,
                }}
              />
              <strong>{hoveredPlayer.name} (#{hoveredPlayer.shirt})</strong>
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 4, fontSize: 11, color: 'var(--text-secondary)' }}>
              <span>Role: <strong style={{ color: '#fff' }}>{hoveredPlayer.role}</strong></span>
              <span>Speed: <strong style={{ color: 'var(--accent-cyan)' }}>{hoveredPlayer.speed_kmh} km/h</strong></span>
              <span>Pitch: <strong style={{ color: '#fff' }}>{hoveredPlayer.pitch_x_m}m, {hoveredPlayer.pitch_y_m}m</strong></span>
            </div>
            <div style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>
              Click to {selectedPlayerIds.includes(hoveredPlayer.player_id) ? 'deselect' : 'select'} player
            </div>
          </div>
        )}
      </div>

      {/* Pitch Telemetry Micro Strip (Stitch Spec: High Line, Block Depth, Team Width, Compression) */}
      <div className="pitch-telemetry-micro-deck">
        <div className="telemetry-deck-row">
          <span>High Line: <strong className="telemetry-white">{teamShape?.team_0?.backline?.line_height_m || '41.2'}m</strong></span>
          <span>Block Depth: <strong className="telemetry-white">{teamShape?.team_1?.backline?.line_height_m || '18.5'}m</strong></span>
        </div>
        <div className="telemetry-deck-row">
          <span>Team Width: <strong className="telemetry-white">{teamShape?.team_0?.width_m || '38.2'}m</strong></span>
          <span>Compression: <strong className="telemetry-emerald">{teamShape?.compression || '91%'}</strong></span>
        </div>
      </div>

      {/* Pitch Footer: Tactical Selection Feedback */}
      <div className="pitch-footer-strip">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 11 }}>
          <span style={{ color: 'var(--text-muted)' }}>SELECTION:</span>
          {selectedPlayerIds.length === 0 ? (
            <span style={{ color: 'var(--text-secondary)' }}>
              No players selected. Click any player above or in the roster to analyze.
            </span>
          ) : (
            <span style={{ color: '#fde047', fontWeight: 600 }}>
              {selectedPlayerIds.length} player{selectedPlayerIds.length > 1 ? 's' : ''} actively selected for joint investigation
            </span>
          )}
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontSize: 11 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: team0Color }} />
            <span style={{ color: 'var(--text-secondary)' }}>Home Team</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
            <span style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: team1Color }} />
            <span style={{ color: 'var(--text-secondary)' }}>Away Team</span>
          </div>
        </div>
      </div>
    </div>
  );
}
