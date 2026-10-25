"""
tactical_state.py
=================
Core tactical-state representation for the Football Tactical Predictor.

Sits ABOVE the FOOTPASS/TAAD foundation layer. Reads the same H5 files
but does NOT modify any FOOTPASS code.

COORDINATE SYSTEM
-----------------
X_POS in approx [0,1]: 0=left goal line, 1=right goal line
Y_POS in approx [0,1]: 0=top touchline,  1=bottom touchline
(small exceedances occur near boundaries)

ROLE ORIENTATION (ABSOLUTE PITCH)
----------------------------------
Left/Right in role names always refer to the ABSOLUTE PITCH perspective:
  "Left Back"  = player physically near top of pitch (low Y_POS)
  "Right Back" = player physically near bottom of pitch (high Y_POS)
This is consistent regardless of which team or attack direction.

FOOTPASS assigns role IDs from each team's OWN perspective. Verified:
  Team 0 (attacks ->): role 2 FOOTPASS-LB is at low Y  -> absolute LEFT  (correct)
  Team 1 (attacks <-): role 2 FOOTPASS-LB is at high Y -> absolute RIGHT (was wrong)
Fix: get_role_name() swaps left/right labels for Team 1 (LEFT_TO_RIGHT=1).
The underlying ROLE_ID in H5 is never changed.

TEAM ENCODING
-------------
LEFT_TO_RIGHT = 0: team attacks left->right (high X direction)
LEFT_TO_RIGHT = 1: team attacks right->left (low X direction)

H5 COLUMN MAPPING (from TAAD_Dataset.py / run_TAAD_on_matches.py)
------------------------------------------------------------------
0  FRAME         1  PLAYER_ID     2  LEFT_TO_RIGHT  3  SHIRT_NUMBER
4  ROLE_ID       5  X_POS         6  Y_POS          7  X_SPEED
8  Y_SPEED       9  ROI_X        10  ROI_Y          11  ROI_WIDTH
12 ROI_HEIGHT   13  CLS

ACTION CLASS MAPPING (from train_TAAD_Baseline.py)
--------------------------------------------------
0:background 1:drive 2:pass 3:cross 4:throw-in
5:shot 6:header 7:tackle 8:block

PLAYER INTERACTIONS
-------------------
For each frame, ALL directed ordered pairs (i,j) with i!=j are built.
With 22 players: 22*21=462 directed interactions per frame.
Relative features are from player_i's perspective toward player_j:
  relative_x = player_j.x - player_i.x  (same sign convention throughout)
  The reverse pair (j,i) has opposite signs.
"""

import os
import json
import math
from dataclasses import dataclass, asdict, field
from typing import List, Optional, Dict, Any

import h5py
import numpy as np


# -- Column indices (matches TAAD_Dataset.py exactly) --------------------------
FRAME         = 0
PLAYER_ID     = 1
LEFT_TO_RIGHT = 2
SHIRT_NUMBER  = 3
ROLE_ID       = 4
X_POS         = 5
Y_POS         = 6
X_SPEED       = 7
Y_SPEED       = 8
ROI_X         = 9
ROI_Y         = 10
ROI_WIDTH     = 11
ROI_HEIGHT    = 12
CLS           = 13

# -- Action class names (source: train_TAAD_Baseline.py line 181) --------------
ACTION_NAMES: Dict[int, str] = {
    0: "background",
    1: "drive",
    2: "pass",
    3: "cross",
    4: "throw-in",
    5: "shot",
    6: "header",
    7: "tackle",
    8: "block",
}

# ---------------------------------------------------------------------------
# Role names -- FOOTPASS TEAM-RELATIVE convention
#
# FOOTPASS assigns role IDs from each team's own attacking-direction
# perspective (team-relative). "Left Back" means the player on the
# team's left flank as they face their attack direction.
#
#   Team A (LEFT_TO_RIGHT=0, attacks ->):
#     role 2  = Left Back  -> y ≈ 0.212 (near y=0, top touchline)
#     role 13 = Right Back -> y ≈ 0.741 (near y=1, bottom touchline)
#
#   Team B (LEFT_TO_RIGHT=1, attacks <-):
#     role 2  = Left Back  -> y ≈ 0.784 (near y=1, bottom touchline)
#                             (their left when facing LEFT = bottom touchline side)
#     role 13 = Right Back -> y ≈ 0.363 (near y=0, top touchline)
#                             (their right when facing LEFT = top touchline side)
#
# VISUALIZATION CONVENTION:
#   The pitch visualization INVERTS the y-axis (y=0 at top, y=1 at bottom).
#   This ensures the image matches the standard football diagram orientation
#   where y=0 (top touchline) appears at the TOP of the image.
#
#   With y-axis inversion + FOOTPASS team-relative labels:
#     Team A: LB (y≈0.212, low y) -> TOP of image  [their left, facing ->]  ✓
#             RB (y≈0.741, high y) -> BOTTOM of image [their right, facing ->] ✓
#     Team B: RB (y≈0.363, low y) -> TOP of image  [their right, facing <-]  ✓
#             LB (y≈0.784, high y) -> BOTTOM of image [their left, facing <-]  ✓
#
# NOTE: Both teams use the same ROLE_NAMES dict (FOOTPASS team-relative).
#       Do NOT swap left/right for Team B here -- the y-axis inversion
#       in the visualization handles the correct visual positioning.
# The underlying ROLE_ID in the H5 is never modified.
# ---------------------------------------------------------------------------
ROLE_NAMES: Dict[int, str] = {
    1:  "Goalkeeper",
    2:  "Left Back",
    3:  "Left Central Back",
    4:  "Mid Central Back",
    5:  "Right Central Back",
    6:  "Left Midfielder",
    7:  "Right Midfielder",
    8:  "Defensive Midfielder",
    9:  "Attacking Midfielder",
    10: "Left Winger",
    11: "Right Winger",
    12: "Central Forward",
    13: "Right Back",
}

ROLE_ABBREV: Dict[int, str] = {
    1:"GK", 2:"LB", 3:"LCB", 4:"MCB", 5:"RCB",
    6:"LM", 7:"RM", 8:"DM", 9:"AM", 10:"LW",
    11:"RW", 12:"CF", 13:"RB",
}

# Kept for backward-compat import only -- not used in logic
ROLE_NAMES_LTR0 = ROLE_NAMES
ROLE_NAMES_LTR1 = ROLE_NAMES
ROLE_ABBREV_LTR0 = ROLE_ABBREV
ROLE_ABBREV_LTR1 = ROLE_ABBREV


def get_role_name(role_id: int, left_to_right: int = 0) -> str:
    """
    Return the FOOTPASS team-relative role name for a player.

    Both teams use the same ROLE_NAMES dict (FOOTPASS convention).
    left/right labels are team-relative (from each team's own attacking
    perspective). The visualization inverts the y-axis to ensure the
    correct visual layout for both teams.

    left_to_right parameter is accepted but not used (kept for
    backward compatibility with call sites).
    """
    return ROLE_NAMES.get(role_id, f"Role{role_id}")


def get_role_abbrev(role_id: int, left_to_right: int = 0) -> str:
    """
    Short abbreviation for a role.
    left_to_right accepted for backward compatibility but not used.
    """
    return ROLE_ABBREV.get(role_id, "?")


# -- Data structures -----------------------------------------------------------


@dataclass
class PlayerState:
    """
    Spatiotemporal state of one player at one frame.

    role_name and role_abbrev use FOOTPASS TEAM-RELATIVE convention:
      "Left Back" = player on the team's left flank from their own
      attacking perspective. For Team A (attacks ->): LB is near y=0
      (top touchline). For Team B (attacks <-): LB is near y=1
      (bottom touchline). The visualization inverts the y-axis so both
      display correctly: LB appears at top-left for both teams.
    role_id is the original FOOTPASS H5 value (unchanged).

    x, y in approx [0,1] (normalized pitch coords from FOOTPASS H5)
    vx, vy are normalized frame-to-frame velocity components.
    speed = sqrt(vx^2 + vy^2)

    left_to_right: attacking direction of this player's team.
      0 = team attacks left→right (+x direction, high x = opponent goal)
      1 = team attacks right→left (-x direction, low  x = opponent goal)
    This is the raw LEFT_TO_RIGHT column value from the FOOTPASS H5.
    Used by canonical feature computation to produce direction-invariant
    representations without modifying x/y/vx/vy.
    """
    player_id:      int
    team:           int          # 0 or 1  (LEFT_TO_RIGHT from H5)
    left_to_right:  int          # 0=attacks→, 1=attacks←  (same as team)
    role_id:        int          # 1-13 (original FOOTPASS role ID)
    role_name:      str          # FOOTPASS team-relative label e.g. "Left Back"
    role_abbrev:    str          # short abbreviation e.g. "LB", "RB"
    shirt_number:   int
    x:              float        # normalized pitch x
    y:              float        # normalized pitch y
    vx:             float        # normalized velocity x
    vy:             float        # normalized velocity y
    speed:          float        # sqrt(vx^2 + vy^2)
    action:         int          # 0-8
    action_name:    str
    frame:          int
    has_roi:        bool         # True if broadcast bounding box is visible


@dataclass
class PlayerInteraction:
    """
    Directed pairwise relationship from player_i toward player_j.

    Directed: relative_x = player_j.x - player_i.x
    The reverse pair (j->i) has opposite signs on relative_* features.

    With 22 players per frame: 22*21 = 462 directed pairs per frame.
    same_team=True for both players on the same team.

    Coordinates in same normalized pitch space as PlayerState.
    """
    frame:         int
    player_i_id:   int
    player_j_id:   int
    player_i_team: int
    player_j_team: int
    same_team:     bool
    distance:      float    # ||pos_j - pos_i||, always >= 0
    relative_x:    float    # player_j.x - player_i.x
    relative_y:    float    # player_j.y - player_i.y
    relative_vx:   float    # player_j.vx - player_i.vx
    relative_vy:   float    # player_j.vy - player_i.vy

    def to_dict(self) -> dict:
        return {
            "frame":         self.frame,
            "player_i_id":   self.player_i_id,
            "player_j_id":   self.player_j_id,
            "player_i_team": self.player_i_team,
            "player_j_team": self.player_j_team,
            "same_team":     self.same_team,
            "distance":      round(self.distance, 6),
            "relative_x":    round(self.relative_x, 6),
            "relative_y":    round(self.relative_y, 6),
            "relative_vx":   round(self.relative_vx, 6),
            "relative_vy":   round(self.relative_vy, 6),
        }


@dataclass
class FrameTacticalState:
    """
    Tactical state of the match at a single frame.

    team_A_players: LEFT_TO_RIGHT=0 (attacks left->right)
    team_B_players: LEFT_TO_RIGHT=1 (attacks right->left)
    interactions:   directed pairwise PlayerInteractions (all N*(N-1) pairs)
    """
    frame:           int
    time_seconds:    float
    game_key:        str
    fps:             float
    team_A_players:  List[PlayerState]
    team_B_players:  List[PlayerState]
    interactions:    List[PlayerInteraction] = field(default_factory=list)

    @property
    def n_team_A(self) -> int:
        return len(self.team_A_players)

    @property
    def n_team_B(self) -> int:
        return len(self.team_B_players)

    @property
    def n_players(self) -> int:
        return self.n_team_A + self.n_team_B

    @property
    def n_interactions(self) -> int:
        return len(self.interactions)

    @property
    def all_players(self) -> List[PlayerState]:
        return self.team_A_players + self.team_B_players

    @property
    def active_events(self) -> List[PlayerState]:
        return [p for p in self.all_players if p.action != 0]

    def team_centroid(self, team: int):
        players = self.team_A_players if team == 0 else self.team_B_players
        if not players:
            return None, None
        xs = [p.x for p in players]
        ys = [p.y for p in players]
        return float(np.mean(xs)), float(np.mean(ys))

    def get_interactions_for_player(self, player_id: int) -> List[PlayerInteraction]:
        """All directed interactions where player_id is the source (player_i)."""
        return [ix for ix in self.interactions if ix.player_i_id == player_id]

    def nearest_teammates(self, player_id: int, k: int = 3) -> List[PlayerInteraction]:
        """k nearest same-team interactions for this player (ascending distance)."""
        cands = [ix for ix in self.interactions
                 if ix.player_i_id == player_id and ix.same_team]
        return sorted(cands, key=lambda ix: ix.distance)[:k]

    def nearest_opponents(self, player_id: int, k: int = 3) -> List[PlayerInteraction]:
        """k nearest opponent interactions for this player (ascending distance)."""
        cands = [ix for ix in self.interactions
                 if ix.player_i_id == player_id and not ix.same_team]
        return sorted(cands, key=lambda ix: ix.distance)[:k]

    def to_dict(self) -> dict:
        return {
            "frame":        self.frame,
            "time_seconds": round(self.time_seconds, 3),
            "game_key":     self.game_key,
            "fps":          self.fps,
            "team_A":       [asdict(p) for p in self.team_A_players],
            "team_B":       [asdict(p) for p in self.team_B_players],
            "interactions": [ix.to_dict() for ix in self.interactions],
        }


@dataclass
class TacticalSequence:
    """
    Ordered sequence of FrameTacticalStates over a temporal window.

    This is the top-level container for a short segment of match.
    Future tactical models will consume this as input.
    """
    game_key:     str
    fps:          float
    start_frame:  int
    end_frame:    int
    frame_step:   int          # sampling stride (1 = every frame)
    states:       List[FrameTacticalState] = field(default_factory=list)

    @property
    def n_frames(self) -> int:
        return len(self.states)

    @property
    def duration_seconds(self) -> float:
        if self.n_frames < 2:
            return 0.0
        return (self.end_frame - self.start_frame) / self.fps

    def to_dict(self) -> dict:
        return {
            "game_key":    self.game_key,
            "fps":         self.fps,
            "start_frame": self.start_frame,
            "end_frame":   self.end_frame,
            "frame_step":  self.frame_step,
            "n_frames":    self.n_frames,
            "duration_sec": round(self.duration_seconds, 3),
            "states":      [s.to_dict() for s in self.states],
        }


# ── Builder ──────────────────────────────────────────────────────────────────

def build_player_state(row: np.ndarray, frame: int) -> PlayerState:
    """
    Construct a PlayerState from one H5 row.
    role_name and role_abbrev use ABSOLUTE PITCH convention (see module docstring).
    left_to_right is stored directly from the H5 LEFT_TO_RIGHT column so that
    canonical feature extraction can use it without re-reading the H5.
    """
    role = int(row[ROLE_ID])
    team = int(row[LEFT_TO_RIGHT])   # 0=attacks→, 1=attacks←
    act  = int(row[CLS])
    vx   = float(row[X_SPEED])
    vy   = float(row[Y_SPEED])

    return PlayerState(
        player_id     = int(row[PLAYER_ID]),
        team          = team,
        left_to_right = team,         # LEFT_TO_RIGHT == team encoding in FOOTPASS
        role_id       = role,
        role_name     = get_role_name(role, team),    # absolute-pitch label
        role_abbrev   = get_role_abbrev(role, team),  # absolute-pitch abbreviation
        shirt_number  = int(row[SHIRT_NUMBER]),
        x             = float(row[X_POS]),
        y             = float(row[Y_POS]),
        vx            = vx,
        vy            = vy,
        speed         = math.sqrt(vx * vx + vy * vy),
        action        = act,
        action_name   = ACTION_NAMES.get(act, f"cls{act}"),
        frame         = frame,
        has_roi       = not np.isnan(row[ROI_X]),
    )


def build_frame_state(
    data:     np.ndarray,
    frame:    int,
    game_key: str,
    fps:      float = 25.0,
) -> Optional[FrameTacticalState]:
    """
    Build a FrameTacticalState from all H5 rows belonging to one frame.

    Parameters
    ----------
    data     : full H5 array for this half (shape: [N, 14])
    frame    : target frame index
    game_key : e.g. "game_27_H1"
    fps      : frames per second (used to convert frame → time)

    Returns
    -------
    FrameTacticalState or None if no data exists for this frame.
    """
    frame_rows = data[data[:, FRAME] == frame]
    if len(frame_rows) == 0:
        return None

    team_A_players = []
    team_B_players = []

    for row in frame_rows:
        ps = build_player_state(row, frame)
        if ps.team == 0:
            team_A_players.append(ps)
        else:
            team_B_players.append(ps)

    # Sort each team by role_id for consistent ordering
    team_A_players.sort(key=lambda p: p.role_id)
    team_B_players.sort(key=lambda p: p.role_id)

    return FrameTacticalState(
        frame          = frame,
        time_seconds   = frame / fps,
        game_key       = game_key,
        fps            = fps,
        team_A_players = team_A_players,
        team_B_players = team_B_players,
        interactions   = [],
    )


def build_frame_interactions(state: FrameTacticalState) -> List[PlayerInteraction]:
    """
    Build ALL directed pairwise interactions for one frame.

    For N players produces N*(N-1) directed interactions (both directions).
    With 22 players: 22*21 = 462 per frame.
    All coordinates in normalized pitch space (same as PlayerState).
    """
    all_players = state.all_players
    interactions = []

    for pi in all_players:
        for pj in all_players:
            if pi.player_id == pj.player_id:
                continue
            dx  = pj.x  - pi.x
            dy  = pj.y  - pi.y
            dvx = pj.vx - pi.vx
            dvy = pj.vy - pi.vy
            dist = math.sqrt(dx * dx + dy * dy)

            interactions.append(PlayerInteraction(
                frame         = state.frame,
                player_i_id   = pi.player_id,
                player_j_id   = pj.player_id,
                player_i_team = pi.team,
                player_j_team = pj.team,
                same_team     = (pi.team == pj.team),
                distance      = dist,
                relative_x    = dx,
                relative_y    = dy,
                relative_vx   = dvx,
                relative_vy   = dvy,
            ))

    return interactions


def build_tactical_sequence(
    h5_path:              str,
    game_key:             str,
    start_frame:          int,
    end_frame:            int,
    frame_step:           int   = 1,
    fps:                  float = 25.0,
    include_interactions: bool  = True,
) -> TacticalSequence:
    """
    Build a TacticalSequence from a frame range in the H5 file.

    include_interactions: if True, build pairwise interactions for each frame.
    """
    print(f"[tactical_state] Loading {game_key} from {os.path.basename(h5_path)} ...")

    with h5py.File(h5_path, "r") as f:
        if game_key not in f:
            raise KeyError(
                f"Game key '{game_key}' not found. Available: {list(f.keys())[:10]}"
            )
        data_full = f[game_key][:].astype(np.float64)

    mask = (data_full[:, FRAME] >= start_frame) & (data_full[:, FRAME] <= end_frame)
    data = data_full[mask]
    print(f"[tactical_state] Rows in frame range [{start_frame}, {end_frame}]: {len(data)}")

    sequence = TacticalSequence(
        game_key    = game_key,
        fps         = fps,
        start_frame = start_frame,
        end_frame   = end_frame,
        frame_step  = frame_step,
    )

    skipped = 0
    for frame in range(start_frame, end_frame + 1, frame_step):
        state = build_frame_state(data, frame, game_key, fps)
        if state is None:
            skipped += 1
            continue
        if include_interactions:
            state.interactions = build_frame_interactions(state)
        sequence.states.append(state)

    if skipped > 0:
        print(f"[tactical_state] Skipped {skipped} frames with no H5 data.")

    return sequence


def check_sequence_sanity(seq: TacticalSequence) -> bool:
    """
    Run basic sanity checks on a TacticalSequence.
    Returns True if all checks pass.
    """
    ok = True
    errors = []

    for state in seq.states:
        if state.n_team_A == 0:
            errors.append(f"Frame {state.frame}: Team A has 0 players")
            ok = False
        if state.n_team_B == 0:
            errors.append(f"Frame {state.frame}: Team B has 0 players")
            ok = False

        all_ids = [p.player_id for p in state.all_players]
        if len(all_ids) != len(set(all_ids)):
            errors.append(f"Frame {state.frame}: duplicate player IDs")
            ok = False

        for p in state.team_A_players:
            if p.team != 0:
                errors.append(f"Frame {state.frame}: player {p.player_id} in team_A but team={p.team}")
                ok = False
        for p in state.team_B_players:
            if p.team != 1:
                errors.append(f"Frame {state.frame}: player {p.player_id} in team_B but team={p.team}")
                ok = False

        for ix in state.interactions:
            if ix.distance < 0:
                errors.append(f"Frame {state.frame}: negative distance")
                ok = False
            if ix.same_team != (ix.player_i_team == ix.player_j_team):
                errors.append(f"Frame {state.frame}: same_team flag mismatch")
                ok = False
            if ix.player_i_id == ix.player_j_id:
                errors.append(f"Frame {state.frame}: self-interaction")
                ok = False

        expected_time = state.frame / seq.fps
        if abs(state.time_seconds - expected_time) > 0.001:
            errors.append(f"Frame {state.frame}: time mismatch")
            ok = False

    frames = [s.frame for s in seq.states]
    if frames != sorted(frames):
        errors.append("Frames are not in ascending order")
        ok = False

    n_pl = seq.states[0].n_players if seq.states else 0
    if ok:
        print(f"[sanity] All checks passed ({seq.n_frames} frames, {n_pl} players/frame, "
              f"{seq.states[0].n_interactions if seq.states else 0} interactions/frame)")
    else:
        print(f"[sanity] FAILED {len(errors)} check(s):")
        for e in errors[:10]:
            print(f"  ERROR: {e}")

    return ok


def print_sequence_summary(seq: TacticalSequence) -> None:
    """Print a concise summary of a TacticalSequence."""
    print()
    print("=" * 65)
    print(f"  TACTICAL SEQUENCE SUMMARY")
    print("=" * 65)
    print(f"  Game        : {seq.game_key}")
    print(f"  Frames      : {seq.start_frame} -> {seq.end_frame} (step={seq.frame_step})")
    print(f"  States      : {seq.n_frames}")
    print(f"  Duration    : {seq.duration_seconds:.2f} s  @ {seq.fps} fps")

    if seq.n_frames == 0:
        print("  (empty sequence)")
        return

    n_A  = [s.n_team_A for s in seq.states]
    n_B  = [s.n_team_B for s in seq.states]
    n_ix = [s.n_interactions for s in seq.states]

    print(f"  Team A/frame: {np.mean(n_A):.1f}  (min={min(n_A)}, max={max(n_A)})")
    print(f"  Team B/frame: {np.mean(n_B):.1f}  (min={min(n_B)}, max={max(n_B)})")
    print(f"  Player features : player_id, team, role_id, role_name, role_abbrev,")
    print(f"                    shirt_number, x, y, vx, vy, speed, action,")
    print(f"                    action_name, has_roi")
    if any(n > 0 for n in n_ix):
        n_pl = seq.states[0].n_players
        print(f"  Interactions    : {int(np.mean(n_ix))}/frame  (directed, "
              f"{n_pl}*{n_pl-1}={n_pl*(n_pl-1)})")
        print(f"  Interact feats  : distance, relative_x, relative_y,")
        print(f"                    relative_vx, relative_vy, same_team")

    event_counts = {}
    for s in seq.states:
        for p in s.active_events:
            event_counts[p.action_name] = event_counts.get(p.action_name, 0) + 1
    if event_counts:
        print(f"  Action events   : {dict(sorted(event_counts.items()))}")
    else:
        print(f"  Action events   : none in this window")

    mid = seq.states[len(seq.states) // 2]
    print()
    print(f"  EXAMPLE STATE @ frame {mid.frame} ({mid.time_seconds:.2f} s):")
    cx_A, cy_A = mid.team_centroid(0)
    cx_B, cy_B = mid.team_centroid(1)
    print(f"    Team A centroid: x={cx_A:.3f}, y={cy_A:.3f}")
    print(f"    Team B centroid: x={cx_B:.3f}, y={cy_B:.3f}")
    print(f"    Team A ({mid.n_team_A} players):")
    for p in mid.team_A_players:
        evt = f" [{p.action_name}]" if p.action != 0 else ""
        roi = "vis" if p.has_roi else "---"
        print(f"      [{roi}] {p.role_name:<24} #{p.shirt_number:<2}  "
              f"x={p.x:.3f} y={p.y:.3f}  v=({p.vx:+.3f},{p.vy:+.3f}){evt}")
    print(f"    Team B ({mid.n_team_B} players):")
    for p in mid.team_B_players:
        evt = f" [{p.action_name}]" if p.action != 0 else ""
        roi = "vis" if p.has_roi else "---"
        print(f"      [{roi}] {p.role_name:<24} #{p.shirt_number:<2}  "
              f"x={p.x:.3f} y={p.y:.3f}  v=({p.vx:+.3f},{p.vy:+.3f}){evt}")
    print("=" * 65)
