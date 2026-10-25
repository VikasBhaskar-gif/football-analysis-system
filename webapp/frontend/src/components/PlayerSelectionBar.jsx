import React from 'react';
import { Shield, Sparkles, X, Activity } from 'lucide-react';

export default function PlayerSelectionBar({
  players = [],
  selectedPlayerIds = [],
  onClearSelection,
  matchSummary,
  overlayData,
  currentMatch,
}) {
  const team0Players = players.filter((p) => p.team === 0);
  const team1Players = players.filter((p) => p.team === 1);

  const team0Name =
    currentMatch?.home_team ||
    team0Players[0]?.team_name ||
    matchSummary?.teams?.team_0?.name ||
    matchSummary?.home_team ||
    'Newcastle United';

  const team1Name =
    currentMatch?.away_team ||
    team1Players[0]?.team_name ||
    matchSummary?.teams?.team_1?.name ||
    matchSummary?.away_team ||
    'Paris Saint-Germain';

  const carrierPlayer =
    players.find((p) => p.is_carrier || p.player_id === overlayData?.ball_carrier) || null;

  const competition = currentMatch?.competition || 'UEFA Champions League';

  return (
    <div className="matchup-header-strip">
      {/* Left Wing: Home Team */}
      <div className="strip-team-block home-block">
        <span className="strip-team-dot home-dot" />
        <div className="strip-team-info">
          <span className="strip-team-name">{team0Name}</span>
          <span className="strip-team-tag">HOME</span>
        </div>
      </div>

      {/* Center Match Hub: Competition & Active Ball Carrier */}
      <div className="strip-center-hub">
        <div className="strip-match-meta">
          <span className="strip-comp-badge">
            <span className="live-radar-dot" />
            {competition.toUpperCase()}
          </span>
          <span className="strip-vs-text">VS</span>
        </div>

        {carrierPlayer ? (
          <div className="strip-carrier-pill" title="Tracked Ball Carrier on active frame">
            <span className="carrier-pulse-indicator" />
            <span className="carrier-title">BALL CARRIER:</span>
            <span className="carrier-player-name">
              #{carrierPlayer.shirt} {carrierPlayer.name || 'Carrier'}
            </span>
          </div>
        ) : (
          <div className="strip-sync-status">
            <Activity size={12} color="#00f0ff" />
            <span>25 FPS SPATIAL TRACKING</span>
          </div>
        )}

        {selectedPlayerIds.length > 0 && (
          <div className="strip-selected-pill">
            <span>{selectedPlayerIds.length} Selected</span>
            <button
              type="button"
              className="strip-clear-btn"
              onClick={onClearSelection}
              title="Clear Selection"
            >
              <X size={11} />
            </button>
          </div>
        )}
      </div>

      {/* Right Wing: Away Team */}
      <div className="strip-team-block away-block">
        <div className="strip-team-info right-align">
          <span className="strip-team-name">{team1Name}</span>
          <span className="strip-team-tag">AWAY</span>
        </div>
        <span className="strip-team-dot away-dot" />
      </div>
    </div>
  );
}
