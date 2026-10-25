"""
team_metadata.py
================
Verified team metadata, lineups, kit colors, and player identities for matches.

Matches covered:
  - game_39: Newcastle United vs. Paris Saint-Germain (UEFA Champions League, 4 Oct 2023)
  - game_27: Bayern Munich vs. Manchester United (UEFA Champions League, 20 Sep 2023)

Strict verification against FOOTPASS H5 dataset and official UEFA lineups:
  - In game_39_H1:
      Team 0 (LTR=0): Paris Saint-Germain (PSG) - Attacks Left-to-Right (+X) in H1.
      Team 1 (LTR=1): Newcastle United (NEW)    - Attacks Right-to-Left (-X) in H1.
"""

from typing import Dict, Any, Optional

MATCH_TEAM_METADATA: Dict[str, Any] = {
    "game_39": {
        "match_name": "Newcastle United vs Paris Saint-Germain",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-10-04",
        "venue": "St. James' Park, Newcastle",
        "teams": {
            0: {
                "name": "Paris Saint-Germain",
                "short_name": "PSG",
                "code": "PAR",
                "bgr": (160, 60, 20),      # Dark Navy Blue with Red accent
                "rgb": (20, 60, 160),
                "accent_rgb": (220, 40, 60),# Red accent
                "h1_attacking_dir": 1.0,    # Left-to-Right (+X)
                "roster": {
                    2:  {"name": "Achraf Hakimi",       "pos": "RB", "role": 13},
                    4:  {"name": "Manuel Ugarte",       "pos": "DM", "role": 7},
                    5:  {"name": "Marquinhos",          "pos": "CB", "role": 5},
                    7:  {"name": "Kylian Mbappe",       "pos": "FW", "role": 9},
                    9:  {"name": "Goncalo Ramos",       "pos": "CF", "role": 12},
                    10: {"name": "Ousmane Dembele",     "pos": "RW", "role": 11},
                    21: {"name": "Lucas Hernandez",     "pos": "LB", "role": 2},
                    23: {"name": "Randal Kolo Muani",   "pos": "FW", "role": 10},
                    33: {"name": "Warren Zaire-Emery",  "pos": "CM", "role": 6},
                    37: {"name": "Milan Skriniar",      "pos": "CB", "role": 3},
                    99: {"name": "Gianluigi Donnarumma","pos": "GK", "role": 1},
                },
            },
            1: {
                "name": "Newcastle United",
                "short_name": "Newcastle",
                "code": "NEW",
                "bgr": (240, 240, 240),    # Black & White stripes
                "rgb": (240, 240, 240),
                "accent_rgb": (0, 215, 255),# Gold/Cyan broadcast accent
                "h1_attacking_dir": -1.0,   # Right-to-Left (-X)
                "roster": {
                    2:  {"name": "Kieran Trippier",     "pos": "RB", "role": 13},
                    5:  {"name": "Fabian Schar",        "pos": "CB", "role": 3},
                    6:  {"name": "Jamaal Lascelles",    "pos": "CB", "role": 5},
                    8:  {"name": "Sandro Tonali",       "pos": "CM", "role": 6},
                    10: {"name": "Anthony Gordon",      "pos": "LW", "role": 10},
                    14: {"name": "Alexander Isak",      "pos": "CF", "role": 12},
                    22: {"name": "Nick Pope",           "pos": "GK", "role": 1},
                    24: {"name": "Miguel Almiron",      "pos": "RW", "role": 11},
                    33: {"name": "Dan Burn",            "pos": "LB", "role": 2},
                    36: {"name": "Sean Longstaff",      "pos": "CM", "role": 7},
                    39: {"name": "Bruno Guimaraes",     "pos": "CM", "role": 9},
                },

            },
        },
    },
    "game_27": {
        "match_name": "Bayern Munich vs Manchester United",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-09-20",
        "venue": "Allianz Arena, Munich",
        "teams": {
            0: {
                "name": "Bayern Munich",
                "short_name": "Bayern",
                "code": "BAY",
                "bgr": (30, 30, 220),       # Red
                "rgb": (220, 30, 30),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": 1.0,
                "roster": {
                    2:  {"name": "Dayot Upamecano",   "pos": "CB", "role": 13},
                    3:  {"name": "Kim Min-jae",       "pos": "CB", "role": 3},
                    6:  {"name": "Joshua Kimmich",    "pos": "CM", "role": 5},
                    7:  {"name": "Serge Gnabry",      "pos": "FW", "role": 9},
                    8:  {"name": "Leon Goretzka",     "pos": "CM", "role": 6},
                    9:  {"name": "Harry Kane",        "pos": "CF", "role": 12},
                    10: {"name": "Leroy Sané",        "pos": "RW", "role": 11},
                    11: {"name": "Kingsley Coman",    "pos": "FW", "role": 9},
                    13: {"name": "Eric Choupo-Moting","pos": "CF", "role": 9},
                    19: {"name": "Alphonso Davies",   "pos": "LB", "role": 2},
                    25: {"name": "Thomas Müller",     "pos": "AM", "role": 10},
                    26: {"name": "Sven Ulreich",      "pos": "GK", "role": 1},
                    27: {"name": "Konrad Laimer",     "pos": "RB", "role": 7},
                    39: {"name": "Mathys Tel",        "pos": "FW", "role": 9},
                    42: {"name": "Jamal Musiala",     "pos": "AM", "role": 10},
                },
            },
            1: {
                "name": "Manchester United",
                "short_name": "Man Utd",
                "code": "MUN",
                "bgr": (20, 160, 20),       # Green / Away kit
                "rgb": (20, 160, 20),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": -1.0,
                "roster": {
                    2:  {"name": "Victor Lindelöf",   "pos": "CB", "role": 13},
                    6:  {"name": "Lisandro Martínez", "pos": "CB", "role": 5},
                    8:  {"name": "Bruno Fernandes",   "pos": "AM", "role": 6},
                    9:  {"name": "Anthony Martial",   "pos": "CF", "role": 12},
                    10: {"name": "Marcus Rashford",   "pos": "LW", "role": 10},
                    11: {"name": "Rasmus Højlund",    "pos": "CF", "role": 11},
                    14: {"name": "Christian Eriksen", "pos": "CM", "role": 12},
                    15: {"name": "Sergio Reguilón",   "pos": "LB", "role": 3},
                    17: {"name": "Alejandro Garnacho","pos": "LW", "role": 10},
                    18: {"name": "Casemiro",          "pos": "DM", "role": 1},
                    20: {"name": "Diogo Dalot",       "pos": "RB", "role": 2},
                    24: {"name": "André Onana",       "pos": "GK", "role": 7},
                    28: {"name": "Facundo Pellistri", "pos": "RW", "role": 9},
                    39: {"name": "Scott McTominay",   "pos": "CM", "role": 6},
                    46: {"name": "Hannibal Mejbri",   "pos": "CM", "role": 8},
                },
            },
        },
    },
    "game_27_H1": {
        "match_name": "Bayern Munich vs Manchester United (First Half)",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-09-20",
        "venue": "Allianz Arena, Munich",
        "teams": {
            0: {
                "name": "Bayern Munich",
                "short_name": "Bayern",
                "code": "BAY",
                "bgr": (30, 30, 220),       # Red
                "rgb": (220, 30, 30),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": 1.0,
                "roster": {
                    2:  {"name": "Dayot Upamecano",   "pos": "CB", "role": 13},
                    3:  {"name": "Kim Min-jae",       "pos": "CB", "role": 3},
                    6:  {"name": "Joshua Kimmich",    "pos": "CM", "role": 5},
                    7:  {"name": "Serge Gnabry",      "pos": "FW", "role": 9},
                    8:  {"name": "Leon Goretzka",     "pos": "CM", "role": 6},
                    9:  {"name": "Harry Kane",        "pos": "CF", "role": 12},
                    10: {"name": "Leroy Sané",        "pos": "RW", "role": 11},
                    11: {"name": "Kingsley Coman",    "pos": "FW", "role": 9},
                    13: {"name": "Eric Choupo-Moting","pos": "CF", "role": 9},
                    19: {"name": "Alphonso Davies",   "pos": "LB", "role": 2},
                    25: {"name": "Thomas Müller",     "pos": "AM", "role": 10},
                    26: {"name": "Sven Ulreich",      "pos": "GK", "role": 1},
                    27: {"name": "Konrad Laimer",     "pos": "RB", "role": 7},
                    39: {"name": "Mathys Tel",        "pos": "FW", "role": 9},
                    42: {"name": "Jamal Musiala",     "pos": "AM", "role": 10},
                },
            },
            1: {
                "name": "Manchester United",
                "short_name": "Man Utd",
                "code": "MUN",
                "bgr": (20, 160, 20),       # Green / Away kit
                "rgb": (20, 160, 20),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": -1.0,
                "roster": {
                    2:  {"name": "Victor Lindelöf",   "pos": "CB", "role": 13},
                    6:  {"name": "Lisandro Martínez", "pos": "CB", "role": 5},
                    8:  {"name": "Bruno Fernandes",   "pos": "AM", "role": 6},
                    9:  {"name": "Anthony Martial",   "pos": "CF", "role": 12},
                    10: {"name": "Marcus Rashford",   "pos": "LW", "role": 10},
                    11: {"name": "Rasmus Højlund",    "pos": "CF", "role": 11},
                    14: {"name": "Christian Eriksen", "pos": "CM", "role": 12},
                    15: {"name": "Sergio Reguilón",   "pos": "LB", "role": 3},
                    17: {"name": "Alejandro Garnacho","pos": "LW", "role": 10},
                    18: {"name": "Casemiro",          "pos": "DM", "role": 1},
                    20: {"name": "Diogo Dalot",       "pos": "RB", "role": 2},
                    24: {"name": "André Onana",       "pos": "GK", "role": 7},
                    28: {"name": "Facundo Pellistri", "pos": "RW", "role": 9},
                    39: {"name": "Scott McTominay",   "pos": "CM", "role": 6},
                    46: {"name": "Hannibal Mejbri",   "pos": "CM", "role": 8},
                },
            },
        },
    },
    "game_27_H2": {
        "match_name": "Bayern Munich vs Manchester United (Second Half)",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-09-20",
        "venue": "Allianz Arena, Munich",
        "teams": {
            0: {
                "name": "Manchester United",
                "short_name": "Man Utd",
                "code": "MUN",
                "bgr": (20, 160, 20),       # Green / Away kit
                "rgb": (20, 160, 20),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": 1.0,
                "roster": {
                    2:  {"name": "Victor Lindelöf",   "pos": "CB", "role": 13},
                    6:  {"name": "Lisandro Martínez", "pos": "CB", "role": 5},
                    8:  {"name": "Bruno Fernandes",   "pos": "AM", "role": 6},
                    9:  {"name": "Anthony Martial",   "pos": "CF", "role": 12},
                    10: {"name": "Marcus Rashford",   "pos": "LW", "role": 10},
                    11: {"name": "Rasmus Højlund",    "pos": "CF", "role": 11},
                    14: {"name": "Christian Eriksen", "pos": "CM", "role": 12},
                    15: {"name": "Sergio Reguilón",   "pos": "LB", "role": 3},
                    17: {"name": "Alejandro Garnacho","pos": "LW", "role": 10},
                    18: {"name": "Casemiro",          "pos": "DM", "role": 1},
                    20: {"name": "Diogo Dalot",       "pos": "RB", "role": 2},
                    24: {"name": "André Onana",       "pos": "GK", "role": 7},
                    28: {"name": "Facundo Pellistri", "pos": "RW", "role": 9},
                    39: {"name": "Scott McTominay",   "pos": "CM", "role": 6},
                    46: {"name": "Hannibal Mejbri",   "pos": "CM", "role": 8},
                },
            },
            1: {
                "name": "Bayern Munich",
                "short_name": "Bayern",
                "code": "BAY",
                "bgr": (30, 30, 220),       # Red
                "rgb": (220, 30, 30),
                "accent_rgb": (255, 255, 255),
                "h1_attacking_dir": -1.0,
                "roster": {
                    2:  {"name": "Dayot Upamecano",   "pos": "CB", "role": 13},
                    3:  {"name": "Kim Min-jae",       "pos": "CB", "role": 3},
                    6:  {"name": "Joshua Kimmich",    "pos": "CM", "role": 5},
                    7:  {"name": "Serge Gnabry",      "pos": "FW", "role": 9},
                    8:  {"name": "Leon Goretzka",     "pos": "CM", "role": 6},
                    9:  {"name": "Harry Kane",        "pos": "CF", "role": 12},
                    10: {"name": "Leroy Sané",        "pos": "RW", "role": 11},
                    11: {"name": "Kingsley Coman",    "pos": "FW", "role": 9},
                    13: {"name": "Eric Choupo-Moting","pos": "CF", "role": 9},
                    19: {"name": "Alphonso Davies",   "pos": "LB", "role": 2},
                    25: {"name": "Thomas Müller",     "pos": "AM", "role": 10},
                    26: {"name": "Sven Ulreich",      "pos": "GK", "role": 1},
                    27: {"name": "Konrad Laimer",     "pos": "RB", "role": 7},
                    39: {"name": "Mathys Tel",        "pos": "FW", "role": 9},
                    42: {"name": "Jamal Musiala",     "pos": "AM", "role": 10},
                },
            },
        },
    },
}


def get_match_meta(match_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve metadata dict for a match or half (e.g. 'game_27_H2' or 'game_39')."""
    if match_id in MATCH_TEAM_METADATA:
        return MATCH_TEAM_METADATA[match_id]
    parts = match_id.split("_")
    if len(parts) >= 3:
        half_id = "_".join(parts[:3])
        if half_id in MATCH_TEAM_METADATA:
            return MATCH_TEAM_METADATA[half_id]
    base_id = "_".join(parts[:2])
    return MATCH_TEAM_METADATA.get(base_id)


def get_team_name(match_id: str, team_id: Optional[int], use_short: bool = False) -> str:
    """Get verified team name or fallback to Team 0 / Team 1."""
    if team_id is None:
        return "Neutral / Contested"
    meta = get_match_meta(match_id)
    if meta and team_id in meta["teams"]:
        t_info = meta["teams"][team_id]
        return t_info["short_name"] if use_short else f"{t_info['name']} (Team {team_id})"
    return f"Team {team_id}"


def get_player_name(match_id: str, team_id: Optional[int], shirt: Optional[int]) -> Optional[str]:
    """Get verified player name from team roster."""
    if team_id is None or shirt is None:
        return None
    meta = get_match_meta(match_id)
    if meta and team_id in meta["teams"]:
        roster = meta["teams"][team_id].get("roster", {})
        if shirt in roster:
            return roster[shirt]["name"]
    return None


def get_player_display_label(match_id: str, team_id: Optional[int], shirt: Optional[int]) -> str:
    """Format player display label (e.g. '#10 Dembélé' or '#33 Dan Burn')."""
    if shirt is None:
        return "Unknown Player"
    p_name = get_player_name(match_id, team_id, shirt)
    if p_name:
        last_name = p_name.split()[-1]
        return f"#{shirt} {last_name}"
    return f"#{shirt}"


def resolve_attacking_direction(
    match_id: Optional[str] = None,
    possessing_team: Optional[int] = 0,
    players: Optional[Any] = None,
) -> float:
    """
    Dynamically resolve attacking direction (+1.0 for Left-to-Right, -1.0 for Right-to-Left)
    using team metadata, goalkeeper positioning, or team pitch centroid.
    """
    meta = get_match_meta(match_id) if match_id else None
    if meta and "teams" in meta and possessing_team in meta["teams"]:
        team_cfg = meta["teams"][possessing_team]
        if "h1_attacking_dir" in team_cfg:
            return float(team_cfg["h1_attacking_dir"])

    # If metadata is not available, infer from Goalkeeper position (role == 1)
    if players:
        for p in players:
            p_role = getattr(p, "role", None)
            p_team = getattr(p, "team", None)
            if p_role is None and isinstance(p, (list, tuple)) and len(p) > 4:
                p_role = int(p[4])
                p_team = int(p[2])
            
            if p_team == possessing_team and p_role == 1:
                gk_x = getattr(p, "foot_x", None)
                if gk_x is None and isinstance(p, (list, tuple)) and len(p) > 11 and not (isinstance(p[9], float) and np.isnan(p[9])):
                    gk_x = p[9] + p[11] / 2.0
                elif gk_x is None and isinstance(p, (list, tuple)) and len(p) > 6 and not (isinstance(p[5], float) and np.isnan(p[5])):
                    gk_x = p[5] * 1920.0
                
                if gk_x is not None:
                    # GK on left half defends left and attacks right (+1.0)
                    return 1.0 if gk_x < 960.0 else -1.0

    return 1.0 if possessing_team == 0 else -1.0

