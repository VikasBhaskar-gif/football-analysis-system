"""
src/tactical/__init__.py
========================
Foundational tactical spatial representation and metadata layer for
the Coach-Directed Football Tactical Analysis Platform.
"""

from .tactical_state import (
    PlayerState,
    PlayerInteraction,
    FrameTacticalState,
    TacticalSequence,
    build_player_state,
    build_frame_state,
    build_frame_interactions,
    build_tactical_sequence,
)
from .team_metadata import (
    MATCH_TEAM_METADATA,
    get_match_meta,
    get_team_name,
    get_player_name,
    get_player_display_label,
    resolve_attacking_direction,
)
from .tactical_features import (
    compute_team_features,
    compute_canonical_team_features,
    compute_interaction_features,
    extract_from_h5,
)

__all__ = [
    "PlayerState",
    "PlayerInteraction",
    "FrameTacticalState",
    "TacticalSequence",
    "build_player_state",
    "build_frame_state",
    "build_frame_interactions",
    "build_tactical_sequence",
    "MATCH_TEAM_METADATA",
    "get_match_meta",
    "get_team_name",
    "get_player_name",
    "get_player_display_label",
    "resolve_attacking_direction",
    "compute_team_features",
    "compute_canonical_team_features",
    "compute_interaction_features",
    "extract_from_h5",
]
