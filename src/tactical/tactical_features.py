"""
tactical_features.py
====================
Compact tactical feature extraction from a TacticalSequence.

For each frame t, produces four feature groups:

  team_A_features     : (N_TEAM_FEATURES,)    = 17 features for Team A
  team_B_features     : (N_TEAM_FEATURES,)    = 17 features for Team B
  interaction_features: (N_INTER_FEATURES,)   = 10 team-vs-team features
  event_features      : (N_EVENT_FEATURES,)   = 16 windowed action counts

Total: 17 + 17 + 10 + 16 = 60 features per frame.

Design principles:
  - No future leakage: event window uses only past frames up to and including t.
  - No ball features: the FOOTPASS dataset has no ball tracking.
  - Fully documented formulas and thresholds.
  - Uses existing PlayerState + PlayerInteraction objects; does NOT re-read H5.

==============================================================================
FEATURE DEFINITIONS
==============================================================================

TEAM FEATURES (17 per team)  -- computed from PlayerState list for that team

  Index  Name             Formula / Definition
  -----  ---------------  ---------------------------------------------------
    0    centroid_x        mean(x_i)  for i in team
    1    centroid_y        mean(y_i)
    2    width             max(y_i) - min(y_i)  (spread across y-axis)
    3    length            max(x_i) - min(x_i)  (spread along x-axis)
    4    compactness       mean_i( sqrt((x_i-cx)^2 + (y_i-cy)^2) )
                          where (cx, cy) is the centroid.
                          Low value = tightly packed; high = spread out.
    5    avg_speed         mean( speed_i )  where speed = sqrt(vx^2+vy^2)
    6    avg_vx            mean( vx_i )  (positive = moving right)
    7    avg_vy            mean( vy_i )  (positive = moving to bottom touchline)
    8-16 zone_xi_yj        proportion of team in each zone of a 3x3 pitch grid.
                          Zones: x in {0,1,2} (left/center/right column)
                                 y in {0,1,2} (top/center/bottom row)
                          zone_x0_y0 = proportion in (x<1/3, y<1/3)
                          zone_x0_y1 = proportion in (x<1/3, 1/3<=y<2/3)
                          zone_x0_y2 = proportion in (x<1/3, y>=2/3)
                          ...flat row-major: xi*3 + yj
                          Proportions sum to 1 per team.

INTERACTION FEATURES (10)  -- team-vs-team

  Index  Name                      Definition
  -----  -------------------------  ------------------------------------------
    0    centroid_dist              Euclidean( centroid_A, centroid_B )
    1    centroid_dx                cx_B - cx_A  (positive: B is further right)
    2    centroid_dy                cy_B - cy_A  (positive: B is further down)
    3    teamA_mean_nearest_opp     For each A player, find nearest B.
                                   This is the mean of those min-distances.
    4    teamA_min_nearest_opp      Minimum of per-A-player nearest-B distances.
    5    teamA_med_nearest_opp      Median of per-A-player nearest-B distances.
    6    teamB_mean_nearest_opp     Symmetric: B players vs nearest A player.
    7    teamB_min_nearest_opp
    8    teamB_med_nearest_opp
    9    interaction_density        n_directed_pairs_within_threshold / 462.
                                   threshold=0.25 (configurable).
                                   Higher = players are generally closer.

EVENT FEATURES (16)  -- windowed action counts over [t - W + 1, t]

  Default window W = 25 frames = 1 second at 25 fps.
  Causal: only past and current frames used.

  Index  Name                  Count of action in window for the given team
  -----  --------------------  -----------------------------------------------
   0     teamA_drive_count      action_id = 1
   1     teamA_pass_count       action_id = 2
   2     teamA_cross_count      action_id = 3
   3     teamA_throw_in_count   action_id = 4
   4     teamA_shot_count       action_id = 5
   5     teamA_header_count     action_id = 6
   6     teamA_tackle_count     action_id = 7
   7     teamA_block_count      action_id = 8
   8-15  teamB_* (same order)

ZONE GRID:
  The pitch is divided into a 3x3 grid in absolute (non-team-relative) coords.

       y<1/3          1/3<=y<2/3        y>=2/3
  x<1/3    z(0,0)       z(0,1)          z(0,2)
  1/3<=x<2/3  z(1,0)   z(1,1)          z(1,2)
  x>=2/3   z(2,0)       z(2,1)          z(2,2)

  Flat index: xi * 3 + yj  (row-major, xi first)
"""

from __future__ import annotations

import json
import math
import os
from typing import Dict, List, Optional, Tuple

import numpy as np

from .tactical_state import (
    TacticalSequence,
    FrameTacticalState,
    PlayerState,
    build_tactical_sequence,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

N_ZONES_X = 3
N_ZONES_Y = 3
N_ZONES   = N_ZONES_X * N_ZONES_Y   # 9

N_TEAM_FEATURES  = 17
N_INTER_FEATURES = 10
N_EVENT_FEATURES = 16

DEFAULT_PROXIMITY_THRESHOLD = 0.25   # normalized pitch units
DEFAULT_EVENT_WINDOW_FRAMES = 25     # 1 second at 25 fps

# Action IDs (from FOOTPASS / TAAD_Dataset.py)
ACTION_EVENT_IDS   = [1, 2, 3, 4, 5, 6, 7, 8]
ACTION_EVENT_NAMES = [
    "drive", "pass", "cross", "throw_in",
    "shot", "header", "tackle", "block",
]

TEAM_FEATURE_NAMES: List[str] = [
    "centroid_x", "centroid_y",
    "width", "length", "compactness",
    "avg_speed", "avg_vx", "avg_vy",
    "zone_x0_y0", "zone_x0_y1", "zone_x0_y2",
    "zone_x1_y0", "zone_x1_y1", "zone_x1_y2",
    "zone_x2_y0", "zone_x2_y1", "zone_x2_y2",
]

# Canonical (direction-invariant) team features.
# For a team attacking right-to-left (left_to_right=1), canonical_x = 1-x
# so that x=0 always represents the team's OWN goal and x=1 the opponent's.
# canonical_vx is signed relative to the attacking direction.
# width/length/compactness/speed/vy are identical to absolute (distances
# are preserved under reflection; y is unchanged).
# Zones are recomputed on canonical_x so zone_x2 is always the attacking third.
CANONICAL_TEAM_FEATURE_NAMES: List[str] = [
    "can_centroid_x", "can_centroid_y",
    "can_width", "can_length", "can_compactness",
    "can_avg_speed", "can_avg_vx", "can_avg_vy",
    "can_zone_x0_y0", "can_zone_x0_y1", "can_zone_x0_y2",
    "can_zone_x1_y0", "can_zone_x1_y1", "can_zone_x1_y2",
    "can_zone_x2_y0", "can_zone_x2_y1", "can_zone_x2_y2",
]
N_CAN_TEAM_FEATURES = len(CANONICAL_TEAM_FEATURE_NAMES)  # 17 (same structure)

# Canonical interaction features (10, same as absolute but centroid_dx is
# the direction-invariant version: positive = opponents further in OWN goal
# direction; distances are invariant under reflection).
CANONICAL_INTER_FEATURE_NAMES: List[str] = [
    "can_centroid_dist",
    "can_centroid_dx",    # (canonical_cx_B - canonical_cx_A) from A's perspective
    "can_centroid_dy",
    "can_teamA_mean_nearest_opp",
    "can_teamA_min_nearest_opp",
    "can_teamA_med_nearest_opp",
    "can_teamB_mean_nearest_opp",
    "can_teamB_min_nearest_opp",
    "can_teamB_med_nearest_opp",
    "can_interaction_density",
]
N_CAN_INTER_FEATURES = len(CANONICAL_INTER_FEATURE_NAMES)  # 10

INTER_FEATURE_NAMES: List[str] = [
    "centroid_dist",
    "centroid_dx",
    "centroid_dy",
    "teamA_mean_nearest_opp",
    "teamA_min_nearest_opp",
    "teamA_med_nearest_opp",
    "teamB_mean_nearest_opp",
    "teamB_min_nearest_opp",
    "teamB_med_nearest_opp",
    "interaction_density",
]

EVENT_FEATURE_NAMES: List[str] = (
    [f"teamA_{n}_count" for n in ACTION_EVENT_NAMES] +
    [f"teamB_{n}_count" for n in ACTION_EVENT_NAMES]
)

assert len(TEAM_FEATURE_NAMES)            == N_TEAM_FEATURES,       "team feature count mismatch"
assert len(CANONICAL_TEAM_FEATURE_NAMES)  == N_CAN_TEAM_FEATURES,   "canonical team feature count mismatch"
assert len(INTER_FEATURE_NAMES)           == N_INTER_FEATURES,      "inter feature count mismatch"
assert len(CANONICAL_INTER_FEATURE_NAMES) == N_CAN_INTER_FEATURES,  "canonical inter feature count mismatch"
assert len(EVENT_FEATURE_NAMES)           == N_EVENT_FEATURES,      "event feature count mismatch"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_zone_idx(x: float, y: float) -> int:
    """
    Return flat zone index (0-8) for normalized (x, y).
    x-zone: 0=x<1/3, 1=1/3<=x<2/3, 2=x>=2/3
    y-zone: 0=y<1/3, 1=1/3<=y<2/3, 2=y>=2/3
    flat = xi * N_ZONES_Y + yj
    """
    xi = min(int(x * N_ZONES_X), N_ZONES_X - 1)
    yj = min(int(y * N_ZONES_Y), N_ZONES_Y - 1)
    return xi * N_ZONES_Y + yj


# ---------------------------------------------------------------------------
# Team features
# ---------------------------------------------------------------------------

def compute_team_features(players: List[PlayerState]) -> np.ndarray:
    """
    Compute 17 ABSOLUTE team-level features.

    Coordinates and velocities are in the original (absolute) pitch frame.
    Formula for compactness:
      mean_i( sqrt( (x_i - cx)^2 + (y_i - cy)^2 ) )

    Returns float32 array of shape (N_TEAM_FEATURES,) = (17,).
    Returns NaN-filled array if players list is empty.
    """
    if not players:
        return np.full(N_TEAM_FEATURES, np.nan, dtype=np.float32)

    xs = np.array([p.x for p in players], dtype=np.float64)
    ys = np.array([p.y for p in players], dtype=np.float64)

    cx, cy     = xs.mean(), ys.mean()
    width      = float(ys.max() - ys.min())
    length     = float(xs.max() - xs.min())
    compactness = float(np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2).mean())
    avg_speed  = float(np.mean([p.speed for p in players]))
    avg_vx     = float(np.mean([p.vx    for p in players]))
    avg_vy     = float(np.mean([p.vy    for p in players]))

    zone_counts = np.zeros(N_ZONES, dtype=np.float32)
    for p in players:
        zone_counts[get_zone_idx(p.x, p.y)] += 1
    zone_props = zone_counts / len(players)

    spatial = np.array(
        [cx, cy, width, length, compactness, avg_speed, avg_vx, avg_vy],
        dtype=np.float32,
    )
    return np.concatenate([spatial, zone_props])


def compute_canonical_team_features(players: List[PlayerState]) -> np.ndarray:
    """
    Compute 17 CANONICAL (direction-invariant) team-level features.

    For each player, canonical_x is computed as:
      left_to_right == 0 (attacks ->):  canonical_x = x         (no change)
      left_to_right == 1 (attacks <-):  canonical_x = 1 - x     (reflect)

    In canonical space:
      canonical_x = 0  always represents the team's OWN goal side.
      canonical_x = 1  always represents the OPPONENT'S goal side.

    Velocity mapping:
      canonical_vx = vx  if left_to_right == 0  (positive = toward opp goal)
      canonical_vx = -vx if left_to_right == 1  (positive = toward opp goal)
      canonical_vy = vy  (unchanged; y-axis is symmetric)

    Features that CHANGE vs absolute:
      - can_centroid_x  (reflected for LTR=1 teams)
      - can_avg_vx      (sign-flipped for LTR=1 teams)
      - can_zone_*      (zones recomputed on canonical_x)

    Features IDENTICAL to absolute (geometrically invariant under x-reflection):
      - can_centroid_y, can_width, can_length, can_compactness,
        can_avg_speed, can_avg_vy

    Sanity guarantee:
      A player at (x=0.2, ltr=0) and a player at (x=0.8, ltr=1) are both
      at canonical_x=0.2 (same distance from own goal in same direction).

    Returns float32 array of shape (N_CAN_TEAM_FEATURES,) = (17,).
    Returns NaN-filled array if players list is empty.
    """
    if not players:
        return np.full(N_CAN_TEAM_FEATURES, np.nan, dtype=np.float32)

    ltr = players[0].left_to_right   # 0 or 1, same for all players in a team

    # Canonical x and vx
    if ltr == 0:
        cxs  = np.array([p.x  for p in players], dtype=np.float64)
        cvxs = np.array([p.vx for p in players], dtype=np.float64)
    else:
        cxs  = np.array([1.0 - p.x  for p in players], dtype=np.float64)
        cvxs = np.array([-p.vx       for p in players], dtype=np.float64)

    ys   = np.array([p.y  for p in players], dtype=np.float64)
    cvys = np.array([p.vy for p in players], dtype=np.float64)

    ccx, ccy  = cxs.mean(), ys.mean()
    width     = float(ys.max()  - ys.min())                            # unchanged
    length    = float(cxs.max() - cxs.min())                          # same as abs
    compactness = float(np.sqrt((cxs - ccx) ** 2 + (ys - ccy) ** 2).mean())
    avg_speed = float(np.mean([p.speed for p in players]))             # unchanged
    avg_cvx   = float(cvxs.mean())
    avg_cvy   = float(cvys.mean())                                     # same as abs

    zone_counts = np.zeros(N_ZONES, dtype=np.float32)
    for cx_i, y_i in zip(cxs, ys):
        zone_counts[get_zone_idx(cx_i, y_i)] += 1
    zone_props = zone_counts / len(players)

    spatial = np.array(
        [ccx, ccy, width, length, compactness, avg_speed, avg_cvx, avg_cvy],
        dtype=np.float32,
    )
    return np.concatenate([spatial, zone_props])


# ---------------------------------------------------------------------------
# Interaction features
# ---------------------------------------------------------------------------

def _nearest_opp_dists(state: FrameTacticalState, source_team: int) -> np.ndarray:
    """
    For each player in source_team, return distance to their nearest opponent.
    Uses pre-built interaction data via state.nearest_opponents().
    """
    players = state.team_A_players if source_team == 0 else state.team_B_players
    dists = []
    for p in players:
        nearest = state.nearest_opponents(p.player_id, k=1)
        if nearest:
            dists.append(nearest[0].distance)
    return np.array(dists, dtype=np.float64)


def compute_interaction_features(
    state: FrameTacticalState,
    proximity_threshold: float = DEFAULT_PROXIMITY_THRESHOLD,
) -> np.ndarray:
    """
    Compute 10 team-vs-team interaction features.

    proximity_threshold (default 0.25 normalized):
      A directed pair is "close" if distance < threshold.
      interaction_density = n_close / 462

    Returns float32 array of shape (N_INTER_FEATURES,) = (10,).
    """
    cx_A, cy_A = state.team_centroid(0)
    cx_B, cy_B = state.team_centroid(1)

    if None in (cx_A, cy_A, cx_B, cy_B):
        return np.full(N_INTER_FEATURES, np.nan, dtype=np.float32)

    centroid_dist = math.sqrt((cx_B - cx_A) ** 2 + (cy_B - cy_A) ** 2)
    centroid_dx   = cx_B - cx_A
    centroid_dy   = cy_B - cy_A

    da = _nearest_opp_dists(state, 0)
    db = _nearest_opp_dists(state, 1)

    def _stats(arr):
        if arr.size == 0:
            return float("nan"), float("nan"), float("nan")
        return float(arr.mean()), float(arr.min()), float(np.median(arr))

    a_mean, a_min, a_med = _stats(da)
    b_mean, b_min, b_med = _stats(db)

    n_total = len(state.interactions)
    n_close = sum(1 for ix in state.interactions if ix.distance < proximity_threshold)
    density = n_close / n_total if n_total > 0 else 0.0

    return np.array(
        [centroid_dist, centroid_dx, centroid_dy,
         a_mean, a_min, a_med,
         b_mean, b_min, b_med,
         density],
        dtype=np.float32,
    )


def compute_canonical_interaction_features(
    state: FrameTacticalState,
    proximity_threshold: float = DEFAULT_PROXIMITY_THRESHOLD,
) -> np.ndarray:
    """
    Compute 10 CANONICAL team-vs-team interaction features.

    Distances (centroid_dist, nearest-opp, density) are Euclidean and
    therefore IDENTICAL to the absolute versions.

    centroid_dx is recomputed as:
      (canonical_cx_B - canonical_cx_A)
    where each team's canonical_cx is their x-reflected centroid.
    This makes positive dx mean "opponent's centroid is deeper in their
    own half" from Team A's attacking perspective.

    Teams A and B attacking directions are read from player left_to_right fields.
    If either team has no players, returns NaN-filled array.
    """
    A_players = state.team_A_players
    B_players = state.team_B_players

    if not A_players or not B_players:
        return np.full(N_CAN_INTER_FEATURES, np.nan, dtype=np.float32)

    ltr_A = A_players[0].left_to_right
    ltr_B = B_players[0].left_to_right

    # Canonical centroids
    axs = np.array([p.x for p in A_players], dtype=np.float64)
    bxs = np.array([p.x for p in B_players], dtype=np.float64)
    ays = np.array([p.y for p in A_players], dtype=np.float64)
    bys = np.array([p.y for p in B_players], dtype=np.float64)

    can_cx_A = (1.0 - axs.mean()) if ltr_A == 1 else axs.mean()
    can_cx_B = (1.0 - bxs.mean()) if ltr_B == 1 else bxs.mean()
    can_cy_A = ays.mean()
    can_cy_B = bys.mean()

    # Distances are Euclidean (invariant under reflection)
    centroid_dist = math.sqrt((can_cx_B - can_cx_A) ** 2 + (can_cy_B - can_cy_A) ** 2)
    centroid_dx   = can_cx_B - can_cx_A
    centroid_dy   = can_cy_B - can_cy_A

    da = _nearest_opp_dists(state, 0)   # distances, invariant
    db = _nearest_opp_dists(state, 1)

    def _stats(arr):
        if arr.size == 0:
            return float("nan"), float("nan"), float("nan")
        return float(arr.mean()), float(arr.min()), float(np.median(arr))

    a_mean, a_min, a_med = _stats(da)
    b_mean, b_min, b_med = _stats(db)

    n_total = len(state.interactions)
    n_close = sum(1 for ix in state.interactions if ix.distance < proximity_threshold)
    density = n_close / n_total if n_total > 0 else 0.0

    return np.array(
        [centroid_dist, centroid_dx, centroid_dy,
         a_mean, a_min, a_med,
         b_mean, b_min, b_med,
         density],
        dtype=np.float32,
    )


# ---------------------------------------------------------------------------
# Main extractor class
# ---------------------------------------------------------------------------

class TacticalFeatureExtractor:
    """
    Extracts compact tactical features from a TacticalSequence.

    Parameters
    ----------
    proximity_threshold : float
        Normalized distance threshold for interaction_density. Default 0.25.
    event_window_frames : int
        Number of frames in the causal event window. Default 25 (=1s @25fps).
    """

    def __init__(
        self,
        proximity_threshold: float = DEFAULT_PROXIMITY_THRESHOLD,
        event_window_frames: int   = DEFAULT_EVENT_WINDOW_FRAMES,
    ):
        self.proximity_threshold = proximity_threshold
        self.event_window_frames = event_window_frames

    def extract(self, seq: TacticalSequence) -> Dict:
        """
        Extract features for all frames in the sequence.

        Returns a dict:
          frames                     (T,)      int32
          times                      (T,)      float32

          -- Absolute (original pitch coordinates) --
          team_A_features            (T, 17)   float32
          team_B_features            (T, 17)   float32
          interaction_features       (T, 10)   float32
          event_features             (T, 16)   float32  (windowed counts)

          -- Canonical (direction-invariant) --
          canonical_A_features       (T, 17)   float32   # can_centroid_x, can_avg_vx, can_zones differ
          canonical_B_features       (T, 17)   float32
          canonical_inter_features   (T, 10)   float32   # only can_centroid_dx differs

          feature_names_team         (17,)     object   (str)
          feature_names_canonical    (17,)     object
          feature_names_inter        (10,)     object
          feature_names_canonical_inter (10,)  object
          feature_names_event        (16,)     object
          metadata                   dict
        """
        T = seq.n_frames
        W = self.event_window_frames

        frames_arr  = np.zeros(T, dtype=np.int32)
        times_arr   = np.zeros(T, dtype=np.float32)
        team_A_feat = np.full((T, N_TEAM_FEATURES),      np.nan, dtype=np.float32)
        team_B_feat = np.full((T, N_TEAM_FEATURES),      np.nan, dtype=np.float32)
        inter_feat  = np.full((T, N_INTER_FEATURES),     np.nan, dtype=np.float32)
        can_A_feat  = np.full((T, N_CAN_TEAM_FEATURES),  np.nan, dtype=np.float32)
        can_B_feat  = np.full((T, N_CAN_TEAM_FEATURES),  np.nan, dtype=np.float32)
        can_ix_feat = np.full((T, N_CAN_INTER_FEATURES), np.nan, dtype=np.float32)
        event_raw   = np.zeros((T, N_EVENT_FEATURES), dtype=np.int32)

        # Pass 1: record frame indices + raw per-frame event counts
        for t_idx, state in enumerate(seq.states):
            frames_arr[t_idx] = state.frame
            times_arr[t_idx]  = state.time_seconds
            for p in state.team_A_players:
                if p.action in ACTION_EVENT_IDS:
                    event_raw[t_idx, ACTION_EVENT_IDS.index(p.action)] += 1
            for p in state.team_B_players:
                if p.action in ACTION_EVENT_IDS:
                    event_raw[t_idx, 8 + ACTION_EVENT_IDS.index(p.action)] += 1

        # Pass 2: all spatial/interaction/canonical features + windowed event sum
        event_windowed = np.zeros((T, N_EVENT_FEATURES), dtype=np.float32)
        for t_idx, state in enumerate(seq.states):
            team_A_feat[t_idx] = compute_team_features(state.team_A_players)
            team_B_feat[t_idx] = compute_team_features(state.team_B_players)
            inter_feat[t_idx]  = compute_interaction_features(
                state, self.proximity_threshold
            )
            can_A_feat[t_idx]  = compute_canonical_team_features(state.team_A_players)
            can_B_feat[t_idx]  = compute_canonical_team_features(state.team_B_players)
            can_ix_feat[t_idx] = compute_canonical_interaction_features(
                state, self.proximity_threshold
            )
            # Causal window [max(0, t-W+1), t] -- no future frames
            start = max(0, t_idx - W + 1)
            event_windowed[t_idx] = event_raw[start : t_idx + 1].sum(axis=0)

        # Record attacking directions for documentation
        ltr_A = int(seq.states[0].team_A_players[0].left_to_right) if seq.states and seq.states[0].team_A_players else 0
        ltr_B = int(seq.states[0].team_B_players[0].left_to_right) if seq.states and seq.states[0].team_B_players else 1

        metadata = {
            "game_key":             seq.game_key,
            "fps":                  seq.fps,
            "start_frame":          int(frames_arr[0]),
            "end_frame":            int(frames_arr[-1]),
            "n_frames":             T,
            "proximity_threshold":  self.proximity_threshold,
            "event_window_frames":  W,
            "event_window_seconds": round(W / seq.fps, 3),
            "n_team_features":      N_TEAM_FEATURES,
            "n_inter_features":     N_INTER_FEATURES,
            "n_event_features":     N_EVENT_FEATURES,
            "n_can_team_features":  N_CAN_TEAM_FEATURES,
            "n_can_inter_features": N_CAN_INTER_FEATURES,
            "n_total_features":     N_TEAM_FEATURES * 2 + N_INTER_FEATURES + N_EVENT_FEATURES,
            "n_structural_features": N_TEAM_FEATURES * 2 + N_INTER_FEATURES,
            "n_canonical_features": N_CAN_TEAM_FEATURES * 2 + N_CAN_INTER_FEATURES,
            "team_A_left_to_right": ltr_A,
            "team_B_left_to_right": ltr_B,
            "team_A_attacks":       "left->right" if ltr_A == 0 else "right->left",
            "team_B_attacks":       "left->right" if ltr_B == 0 else "right->left",
            "canonical_note":       "canonical_x=x for ltr=0, canonical_x=1-x for ltr=1; canonical_vx=-vx for ltr=1",
            "zone_grid":            "3x3 absolute pitch; x-zones [0,1/3,2/3,1], y-zones same",
            "canonical_zone_grid":  "3x3 canonical pitch; zone_x2 is always the attacking third",
            "compactness_formula":  "mean_i( sqrt( (xi-cx)^2 + (yi-cy)^2 ) )",
            "density_formula":      "n_directed_pairs_within_threshold / 462",
            "density_threshold":    self.proximity_threshold,
            "event_window_note":    "causal: uses frames [t-W+1, t], no future leakage",
            "no_ball_note":         "FOOTPASS has no ball tracking; ball features omitted",
        }

        return {
            "frames":                  frames_arr,
            "times":                   times_arr,
            "team_A_features":         team_A_feat,
            "team_B_features":         team_B_feat,
            "interaction_features":    inter_feat,
            "canonical_A_features":    can_A_feat,
            "canonical_B_features":    can_B_feat,
            "canonical_inter_features":can_ix_feat,
            "event_features":          event_windowed,
            "feature_names_team":      np.array(TEAM_FEATURE_NAMES,             dtype=object),
            "feature_names_canonical": np.array(CANONICAL_TEAM_FEATURE_NAMES,   dtype=object),
            "feature_names_inter":     np.array(INTER_FEATURE_NAMES,            dtype=object),
            "feature_names_canonical_inter": np.array(CANONICAL_INTER_FEATURE_NAMES, dtype=object),
            "feature_names_event":     np.array(EVENT_FEATURE_NAMES,            dtype=object),
            "metadata":                metadata,
        }


# ---------------------------------------------------------------------------
# Convenience function
# ---------------------------------------------------------------------------

def extract_from_h5(
    h5_path:             str,
    game_key:            str,
    start_frame:         int   = 0,
    end_frame:           int   = 99999,
    frame_step:          int   = 1,
    fps:                 float = 25.0,
    proximity_threshold: float = DEFAULT_PROXIMITY_THRESHOLD,
    event_window_frames: int   = DEFAULT_EVENT_WINDOW_FRAMES,
) -> Dict:
    """Build TacticalSequence from H5 and extract features in one call."""
    seq = build_tactical_sequence(
        h5_path              = h5_path,
        game_key             = game_key,
        start_frame          = start_frame,
        end_frame            = end_frame,
        frame_step           = frame_step,
        fps                  = fps,
        include_interactions = True,
    )
    return TacticalFeatureExtractor(
        proximity_threshold = proximity_threshold,
        event_window_frames = event_window_frames,
    ).extract(seq)


# ---------------------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------------------

def check_features_sanity(result: Dict, verbose: bool = True) -> bool:
    """Run sanity checks on extracted feature dict. Returns True if all pass."""
    ok     = True
    errors: List[str] = []

    tA = result["team_A_features"]
    tB = result["team_B_features"]
    ix = result["interaction_features"]
    ev = result["event_features"]
    fr = result["frames"]

    if not np.all(fr[1:] > fr[:-1]):
        errors.append("FAIL: frames not strictly ascending")

    for lbl, arr in [("team_A", tA), ("team_B", tB)]:
        if np.any(np.isnan(arr)):
            errors.append(f"FAIL: NaN in {lbl} features")
        if np.any(np.isinf(arr)):
            errors.append(f"FAIL: inf in {lbl} features")

    if np.any(np.isnan(ix)):
        errors.append("FAIL: NaN in interaction features")
    if np.any(np.isinf(ix)):
        errors.append("FAIL: inf in interaction features")
    if np.any(np.isnan(ev)):
        errors.append("FAIL: NaN in event features")

    # width/length/compactness >= 0
    for feat_name in ("width", "length", "compactness"):
        idx = TEAM_FEATURE_NAMES.index(feat_name)
        for lbl, arr in [("team_A", tA), ("team_B", tB)]:
            if np.any(arr[:, idx] < -1e-6):
                errors.append(f"FAIL: {lbl}.{feat_name} < 0")

    # distances >= 0
    for i, name in enumerate(INTER_FEATURE_NAMES):
        if "dist" in name or "nearest" in name:
            if np.any(ix[:, i] < -1e-6):
                errors.append(f"FAIL: interaction.{name} < 0")

    # density in [0, 1]
    d_idx = INTER_FEATURE_NAMES.index("interaction_density")
    if np.any(ix[:, d_idx] < -1e-6) or np.any(ix[:, d_idx] > 1 + 1e-6):
        errors.append("FAIL: interaction_density outside [0, 1]")

    # zone proportions sum to 1
    z_start = TEAM_FEATURE_NAMES.index("zone_x0_y0")
    for lbl, arr in [("team_A", tA), ("team_B", tB)]:
        zone_sums = arr[:, z_start : z_start + N_ZONES].sum(axis=1)
        if not np.allclose(zone_sums, 1.0, atol=1e-4):
            errors.append(f"FAIL: {lbl} zone proportions do not sum to 1")

    # event counts >= 0
    if np.any(ev < -1e-6):
        errors.append("FAIL: event counts < 0")

    ok = len(errors) == 0
    if verbose:
        if ok:
            print("[sanity] All feature checks passed.")
        else:
            for e in errors:
                print(e)
            print(f"[sanity] {len(errors)} check(s) failed.")
    return ok
