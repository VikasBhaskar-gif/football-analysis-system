"""
team_metadata.py
================
Authoritative team metadata, canonical rosters, kit colorways, and match-specific mapping system.

Covers all 4 supported matches in FOOTPASS:
  - game_39: Newcastle United (Home) vs. Paris Saint-Germain (Away) (St. James' Park, 4 Oct 2023, UCL)
  - game_27: Bayern Munich (Home) vs. Manchester United (Away) (Allianz Arena, 20 Sep 2023, UCL)
  - game_49: FC Barcelona (Home) vs. Real Betis (Away) (Estadi Olímpic Lluís Companys, 16 Sep 2023, LaLiga)
  - game_51: FC Barcelona (Home) vs. RC Celta de Vigo (Away) (Estadi Olímpic Lluís Companys, 23 Sep 2023, LaLiga)

FOOTPASS H5 DATASET REPRESENTATION:
-----------------------------------
- Column 0: FRAME (Absolute frame index in video)
- Column 1: PLAYER_ID (Stable player tracking ID)
- Column 2: LEFT_TO_RIGHT (Side / spatial attack direction):
    0 = Team defending the left goal (x ≈ 0.1), attacking left-to-right (+X)
    1 = Team defending the right goal (x ≈ 0.9), attacking right-to-left (-X)
  *IMPORTANT*: Teams switch sides at halftime! Column 2 flips between H1 and H2.
- Column 3: SHIRT_NUMBER (Official match jersey number)
- Column 4: ROLE_ID (Tactical position role 1..13)
- Columns 5, 6: X_POS, Y_POS (Normalized pitch coordinates in [0, 1])
- Columns 7, 8: X_SPEED, Y_SPEED (Raw H5 neural network features, NOT calibrated m/s)
- Columns 9..12: ROI_X, ROI_Y, ROI_WIDTH, ROI_HEIGHT (Broadcast video bounding boxes)

SEPARATE FIELDS MAINTAINED:
---------------------------
1. raw_side_id: Raw dataset side/direction label (0 or 1 from H5 column 2).
2. team_id: Normalized internal team index (0 = Home Team, 1 = Away Team) constant across halves.
3. real_world_team: Canonical club identity ("NEW", "PSG", etc., name, colors, roster).
4. attacking_dir: Pitch coordinate orientation (+1.0 for Left-to-Right, -1.0 for Right-to-Left).
"""

from typing import Dict, Any, Optional, Tuple, List
import numpy as np

# Standard pitch dimensions in meters (FIFA recommended)
PITCH_LENGTH_M = 105.0
PITCH_WIDTH_M = 68.0

# Canonical Club Definitions
CANONICAL_TEAMS: Dict[str, Dict[str, Any]] = {
    "NEW": {
        "code": "NEW",
        "name": "Newcastle United",
        "short_name": "Newcastle",
        "country": "ENG",
        "primary_color": "#f8fafc",     # White & Black stripes
        "accent_color": "#00e5ff",      # Electric Cyan broadcast accent
        "border_color": "#0f172a",      # Black stripe edge
        "rgb": (248, 250, 252),
        "accent_rgb": (0, 229, 255),
        "bgr": (240, 240, 240),
        "roster": {
            2:  {"name": "Kieran Trippier",     "pos": "RB", "role": 13},
            5:  {"name": "Fabian Schär",        "pos": "CB", "role": 3},
            6:  {"name": "Jamaal Lascelles",    "pos": "CB", "role": 5},
            8:  {"name": "Sandro Tonali",       "pos": "CM", "role": 6},
            10: {"name": "Anthony Gordon",      "pos": "LW", "role": 10},
            13: {"name": "Matt Targett",        "pos": "LB", "role": 2},
            14: {"name": "Alexander Isak",      "pos": "CF", "role": 12},
            22: {"name": "Nick Pope",           "pos": "GK", "role": 1},
            23: {"name": "Jacob Murphy",        "pos": "RW", "role": 11},
            24: {"name": "Miguel Almirón",      "pos": "RW", "role": 11},
            32: {"name": "Elliot Anderson",     "pos": "CM", "role": 8},
            33: {"name": "Dan Burn",            "pos": "LB", "role": 2},
            36: {"name": "Sean Longstaff",      "pos": "CM", "role": 7},
            39: {"name": "Bruno Guimarães",     "pos": "CM", "role": 9},
        },
    },
    "PSG": {
        "code": "PAR",
        "name": "Paris Saint-Germain",
        "short_name": "PSG",
        "country": "FRA",
        "primary_color": "#1e293b",     # Dark Navy
        "accent_color": "#ef4444",      # Crimson Red stripe
        "border_color": "#3b82f6",      # Royal Blue edge
        "rgb": (30, 41, 59),
        "accent_rgb": (239, 68, 68),
        "bgr": (160, 60, 20),
        "roster": {
            2:  {"name": "Achraf Hakimi",       "pos": "RB", "role": 13},
            4:  {"name": "Manuel Ugarte",       "pos": "DM", "role": 7},
            5:  {"name": "Marquinhos",          "pos": "CB", "role": 5},
            7:  {"name": "Kylian Mbappé",       "pos": "FW", "role": 9},
            9:  {"name": "Gonçalo Ramos",       "pos": "CF", "role": 12},
            10: {"name": "Ousmane Dembélé",     "pos": "RW", "role": 11},
            17: {"name": "Vitinha",             "pos": "CM", "role": 8},
            21: {"name": "Lucas Hernández",     "pos": "LB", "role": 2},
            23: {"name": "Randal Kolo Muani",   "pos": "FW", "role": 10},
            29: {"name": "Bradley Barcola",     "pos": "LW", "role": 10},
            33: {"name": "Warren Zaïre-Emery",  "pos": "CM", "role": 6},
            37: {"name": "Milan Škriniar",      "pos": "CB", "role": 3},
            99: {"name": "Gianluigi Donnarumma","pos": "GK", "role": 1},
        },
    },
    "BAY": {
        "code": "BAY",
        "name": "Bayern Munich",
        "short_name": "Bayern",
        "country": "GER",
        "primary_color": "#dc2626",     # Crimson Red
        "accent_color": "#ffffff",      # White trim
        "border_color": "#991b1b",
        "rgb": (220, 38, 38),
        "accent_rgb": (255, 255, 255),
        "bgr": (30, 30, 220),
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
    "MUN": {
        "code": "MUN",
        "name": "Manchester United",
        "short_name": "Man Utd",
        "country": "ENG",
        "primary_color": "#15803d",     # Green Away kit
        "accent_color": "#ffffff",
        "border_color": "#14532d",
        "rgb": (21, 128, 61),
        "accent_rgb": (255, 255, 255),
        "bgr": (20, 160, 20),
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
    "BVB": {
        "code": "BVB",
        "name": "Borussia Dortmund",
        "short_name": "Dortmund",
        "country": "GER",
        "primary_color": "#eab308",     # Signal Yellow
        "accent_color": "#0f172a",      # Black trim
        "border_color": "#ca8a04",
        "rgb": (234, 179, 8),
        "accent_rgb": (15, 23, 42),
        "bgr": (20, 220, 255),
        "roster": {
            1:  {"name": "Gregor Kobel",        "pos": "GK", "role": 1},
            2:  {"name": "Julian Ryerson",      "pos": "RB", "role": 13},
            3:  {"name": "Nico Schlotterbeck",  "pos": "LB", "role": 2},
            5:  {"name": "Ramy Bensebaini",     "pos": "LB", "role": 2},
            6:  {"name": "Salih Özcan",         "pos": "CM", "role": 7},
            7:  {"name": "Gio Reyna",           "pos": "RW", "role": 11},
            9:  {"name": "Sébastien Haller",    "pos": "CF", "role": 12},
            11: {"name": "Marco Reus",          "pos": "AM", "role": 9},
            14: {"name": "Niclas Füllkrug",     "pos": "FW", "role": 10},
            15: {"name": "Mats Hummels",        "pos": "CB", "role": 3},
            17: {"name": "Marius Wolf",         "pos": "RB", "role": 13},
            18: {"name": "Felix Nmecha",        "pos": "AM", "role": 9},
            21: {"name": "Donyell Malen",       "pos": "RW", "role": 6},
            23: {"name": "Emre Can",            "pos": "DM", "role": 5},
        },
    },
    "MIL": {
        "code": "MIL",
        "name": "AC Milan",
        "short_name": "AC Milan",
        "country": "ITA",
        "primary_color": "#b91c1c",     # Rossoneri Red
        "accent_color": "#0f172a",      # Black stripes
        "border_color": "#ffffff",
        "rgb": (185, 28, 28),
        "accent_rgb": (15, 23, 42),
        "bgr": (20, 20, 220),
        "roster": {
            2:  {"name": "Davide Calabria",     "pos": "RB", "role": 13},
            3:  {"name": "Malick Thiaw",        "pos": "LB", "role": 2},
            5:  {"name": "Pierre Kalulu",       "pos": "CB", "role": 5},
            7:  {"name": "Yacine Adli",         "pos": "CM", "role": 7},
            10: {"name": "Rafael Leão",         "pos": "LW", "role": 10},
            11: {"name": "Christian Pulisic",   "pos": "RW", "role": 11},
            12: {"name": "Olivier Giroud",      "pos": "CF", "role": 12},
            13: {"name": "Antonio Mirante",     "pos": "GK", "role": 1},
            15: {"name": "Luka Jović",          "pos": "CF", "role": 12},
            16: {"name": "Mike Maignan",        "pos": "GK", "role": 1},
            17: {"name": "Noah Okafor",         "pos": "LW", "role": 10},
            19: {"name": "Theo Hernández",      "pos": "LB", "role": 2},
            21: {"name": "Samuel Chukwueze",    "pos": "RM", "role": 6},
            22: {"name": "Tommaso Pobega",      "pos": "AM", "role": 9},
            27: {"name": "Yacine Adli",         "pos": "CM", "role": 7},
            28: {"name": "Fikayo Tomori",       "pos": "CB", "role": 3},
            30: {"name": "Marco Sportiello",    "pos": "GK", "role": 1},
        },
    },
    "RBS": {
        "code": "RBS",
        "name": "Red Bull Salzburg",
        "short_name": "Salzburg",
        "country": "AUT",
        "primary_color": "#f1f5f9",     # White
        "accent_color": "#dc2626",      # Red
        "border_color": "#94a3b8",
        "rgb": (241, 245, 249),
        "accent_rgb": (220, 38, 38),
        "bgr": (240, 240, 240),
        "roster": {
            2:  {"name": "Lucas Gourna-Douath", "pos": "DM", "role": 8},
            3:  {"name": "Aleksa Terzić",       "pos": "RB", "role": 13},
            4:  {"name": "Kamil Piątkowski",    "pos": "CB", "role": 5},
            6:  {"name": "Samson Baidoo",       "pos": "CB", "role": 3},
            8:  {"name": "Roko Šimić",          "pos": "CF", "role": 12},
            10: {"name": "Luka Sučić",          "pos": "RW", "role": 11},
            12: {"name": "Fernando",            "pos": "FW", "role": 9},
            13: {"name": "Alexander Schlager",  "pos": "GK", "role": 1},
            14: {"name": "Maurits Kjaergaard",  "pos": "LM", "role": 6},
            17: {"name": "Andreas Ulmer",       "pos": "RM", "role": 7},
            18: {"name": "Mads Bidstrup",       "pos": "LW", "role": 10},
            19: {"name": "Karim Konaté",        "pos": "CF", "role": 12},
            21: {"name": "Amar Dedić",          "pos": "LB", "role": 2},
            28: {"name": "Samson Baidoo",       "pos": "CB", "role": 3},
        },
    },
    "RSO": {
        "code": "RSO",
        "name": "Real Sociedad",
        "short_name": "Real Sociedad",
        "country": "ESP",
        "primary_color": "#2563eb",     # Royal Blue
        "accent_color": "#ffffff",      # White trim
        "border_color": "#1d4ed8",
        "rgb": (37, 99, 235),
        "accent_rgb": (255, 255, 255),
        "bgr": (220, 100, 20),
        "roster": {
            1:  {"name": "Álex Remiro",         "pos": "GK", "role": 1},
            2:  {"name": "Hamari Traoré",       "pos": "RB", "role": 13},
            3:  {"name": "Aihen Muñoz",         "pos": "LB", "role": 2},
            4:  {"name": "Martín Zubimendi",    "pos": "DM", "role": 8},
            6:  {"name": "Aritz Elustondo",     "pos": "LM", "role": 6},
            7:  {"name": "Ander Barrenetxea",   "pos": "RW", "role": 11},
            8:  {"name": "Mikel Merino",        "pos": "CM", "role": 6},
            9:  {"name": "Carlos Fernández",    "pos": "CF", "role": 12},
            10: {"name": "Mikel Oyarzabal",     "pos": "LW", "role": 10},
            11: {"name": "Mohamed-Ali Cho",     "pos": "RW", "role": 11},
            14: {"name": "Takefusa Kubo",       "pos": "LW", "role": 10},
            15: {"name": "Robin Le Normand",    "pos": "CB", "role": 3},
            17: {"name": "Kieran Tierney",      "pos": "LB", "role": 2},
            18: {"name": "Jon Ander Olasagasti","pos": "AM", "role": 9},
            21: {"name": "André Silva",         "pos": "CM", "role": 6},
            22: {"name": "Beñat Turrientes",    "pos": "RM", "role": 7},
            23: {"name": "Brais Méndez",        "pos": "DM", "role": 5},
        },
    },
    "FCB": {
        "code": "FCB",
        "name": "FC Barcelona",
        "short_name": "Barcelona",
        "country": "ESP",
        "primary_color": "#004d98",     # Blaugrana Deep Navy
        "accent_color": "#a50044",      # Blaugrana Deep Carmine/Garnet
        "border_color": "#edbb00",      # Catalan Gold
        "rgb": (0, 77, 152),
        "accent_rgb": (165, 0, 68),
        "bgr": (152, 77, 0),
        "roster": {
            1:  {"name": "Marc-André ter Stegen", "pos": "GK", "role": 1},
            2:  {"name": "João Cancelo",          "pos": "RB", "role": 13},
            3:  {"name": "Alejandro Balde",       "pos": "LB", "role": 2},
            4:  {"name": "Ronald Araújo",         "pos": "CB", "role": 5},
            5:  {"name": "Iñigo Martínez",        "pos": "CB", "role": 3},
            6:  {"name": "Gavi",                  "pos": "CM", "role": 7},
            7:  {"name": "Ferran Torres",         "pos": "RW", "role": 11},
            9:  {"name": "Robert Lewandowski",    "pos": "CF", "role": 12},
            11: {"name": "Raphinha",              "pos": "RW", "role": 11},
            14: {"name": "João Félix",            "pos": "LW", "role": 10},
            15: {"name": "Andreas Christensen",   "pos": "CB", "role": 3},
            17: {"name": "Marcos Alonso",         "pos": "LB", "role": 2},
            18: {"name": "Oriol Romeu",           "pos": "DM", "role": 8},
            21: {"name": "Frenkie de Jong",       "pos": "CM", "role": 6},
            22: {"name": "İlkay Gündoğan",        "pos": "CM", "role": 7},
            23: {"name": "Jules Koundé",          "pos": "CB", "role": 5},
            27: {"name": "Lamine Yamal",          "pos": "RW", "role": 11},
        },
    },
    "BET": {
        "code": "BET",
        "name": "Real Betis",
        "short_name": "Real Betis",
        "country": "ESP",
        "primary_color": "#0bb364",     # Verdiblanco Emerald Green
        "accent_color": "#ffffff",      # White stripes
        "border_color": "#0f172a",      # Black trim
        "rgb": (11, 179, 100),
        "accent_rgb": (255, 255, 255),
        "bgr": (100, 179, 11),
        "roster": {
            2:  {"name": "Héctor Bellerín",      "pos": "RB", "role": 13},
            3:  {"name": "Juan Miranda",         "pos": "LB", "role": 2},
            5:  {"name": "Guido Rodríguez",      "pos": "DM", "role": 8},
            6:  {"name": "Germán Pezzella",      "pos": "CB", "role": 5},
            7:  {"name": "Abde Ezzalzouli",      "pos": "LW", "role": 11},
            9:  {"name": "Borja Iglesias",       "pos": "CF", "role": 12},
            10: {"name": "Ayoze Pérez",          "pos": "LW", "role": 10},
            11: {"name": "Luiz Henrique",        "pos": "RW", "role": 11},
            12: {"name": "Willian José",         "pos": "CF", "role": 12},
            13: {"name": "Rui Silva",            "pos": "GK", "role": 1},
            15: {"name": "Marc Bartra",          "pos": "CB", "role": 5},
            17: {"name": "Rodri Sánchez",        "pos": "AM", "role": 9},
            20: {"name": "Abner Vinícius",       "pos": "LB", "role": 2},
            21: {"name": "Marc Roca",            "pos": "DM", "role": 6},
            22: {"name": "Isco",                 "pos": "AM", "role": 9},
            24: {"name": "Aitor Ruibal",         "pos": "RB", "role": 13},
            27: {"name": "Sergi Altimira",       "pos": "CM", "role": 7},
            28: {"name": "Chadi Riad",           "pos": "CB", "role": 3},
            30: {"name": "Fran Vieites",         "pos": "GK", "role": 1},
        },
    },
    "CEL": {
        "code": "CEL",
        "name": "RC Celta de Vigo",
        "short_name": "Celta Vigo",
        "country": "ESP",
        "primary_color": "#8ac3ee",     # Celeste Sky Blue
        "accent_color": "#ffffff",      # White trim
        "border_color": "#c0001a",      # Crimson Cross of Saint James
        "rgb": (138, 195, 238),
        "accent_rgb": (255, 255, 255),
        "bgr": (238, 195, 138),
        "roster": {
            2:  {"name": "Carl Starfelt",        "pos": "CB", "role": 5},
            3:  {"name": "Óscar Mingueza",       "pos": "RB", "role": 13},
            4:  {"name": "Unai Núñez",           "pos": "CB", "role": 5},
            8:  {"name": "Fran Beltrán",         "pos": "CM", "role": 8},
            10: {"name": "Iago Aspas",           "pos": "CF", "role": 11},
            13: {"name": "Iván Villar",          "pos": "GK", "role": 1},
            14: {"name": "Luca de la Torre",     "pos": "CM", "role": 6},
            17: {"name": "Jonathan Bamba",       "pos": "LW", "role": 10},
            18: {"name": "Jørgen Strand Larsen", "pos": "CF", "role": 12},
            21: {"name": "Mihailo Ristić",       "pos": "LB", "role": 2},
            28: {"name": "Carlos Domínguez",     "pos": "CB", "role": 3},
        },
    },
}

# Authoritative match configuration: Home and Away clubs
MATCH_CONFIG: Dict[str, Dict[str, Any]] = {
    "game_27": {
        "match_id": "game_27",
        "match_name": "Bayern Munich vs Manchester United",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-09-20",
        "venue": "Allianz Arena, Munich",
        "home": "BAY",
        "away": "MUN",
        "h2_split_frame": 69250,
    },
    "game_39": {
        "match_id": "game_39",
        "match_name": "Newcastle United vs Paris Saint-Germain",
        "competition": "UEFA Champions League (Group Stage)",
        "date": "2023-10-04",
        "venue": "St. James' Park, Newcastle",
        "home": "NEW",
        "away": "PSG",
        "h2_split_frame": 78380,
    },
    "game_49": {
        "match_id": "game_49",
        "match_name": "FC Barcelona vs Real Betis",
        "competition": "LaLiga EA Sports (Matchday 5)",
        "date": "2023-09-16",
        "venue": "Estadi Olímpic Lluís Companys, Barcelona",
        "home": "FCB",
        "away": "BET",
        "h2_split_frame": 73000,
    },
    "game_51": {
        "match_id": "game_51",
        "match_name": "FC Barcelona vs Celta Vigo",
        "competition": "LaLiga EA Sports (Matchday 6)",
        "date": "2023-09-23",
        "venue": "Estadi Olímpic Lluís Companys, Barcelona",
        "home": "FCB",
        "away": "CEL",
        "h2_split_frame": 72500,
    },
}

# Authoritative mapping from H5 dataset column 2 (side_id 0 or 1) to Canonical Team Code
MATCH_HALF_SIDE_MAPPING: Dict[str, Dict[int, str]] = {
    "game_27_H1": {0: "BAY", 1: "MUN"},
    "game_27_H2": {0: "MUN", 1: "BAY"},
    "game_39_H1": {0: "PSG", 1: "NEW"},
    "game_39_H2": {0: "NEW", 1: "PSG"},
    "game_49_H1": {0: "FCB", 1: "BET"},
    "game_49_H2": {0: "BET", 1: "FCB"},
    "game_51_H1": {0: "CEL", 1: "FCB"},
    "game_51_H2": {0: "FCB", 1: "CEL"},
}


def parse_match_and_half(key_or_id: str, abs_frame: Optional[int] = None) -> Tuple[str, str]:
    """
    Extract base match ID (e.g. 'game_39') and effective half key (e.g. 'game_39_H1').
    """
    clean = key_or_id.strip()
    base = "game_39"
    for m in ("game_27", "game_39", "game_49", "game_51"):
        if m in clean:
            base = m
            break

    if "_H1" in clean:
        return base, f"{base}_H1"
    if "_H2" in clean:
        return base, f"{base}_H2"

    # Infer from frame number if available
    cfg = MATCH_CONFIG.get(base)
    split_fr = cfg["h2_split_frame"] if cfg else 75000
    if abs_frame is not None and abs_frame >= split_fr:
        return base, f"{base}_H2"

    return base, f"{base}_H1"


def resolve_player_identity(
    match_key_or_half: str,
    raw_side_id: int,
    shirt_num: int,
    player_id: Optional[int] = None,
    abs_frame: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Authoritative resolution of player identity, team membership, colors, and roles.

    Returns:
      {
        "raw_side_id": int,              # 0 or 1 from H5 column 2
        "team_id": int,                  # 0 = Home, 1 = Away (STABLE across halves)
        "team_code": str,                # Canonical club code ('NEW', 'PSG', etc.)
        "team_name": str,                # 'Newcastle United', 'Paris Saint-Germain', etc.
        "team_short": str,               # 'Newcastle', 'PSG', etc.
        "is_home": bool,                 # True if Home team
        "name": str,                     # Full player name e.g. 'Fabian Schär'
        "display_label": str,            # '#5 Schär'
        "shirt": int,                    # Shirt number
        "pos": str,                      # 'CB', 'FW', 'GK', etc.
        "role": int,                     # Tactical role ID (1..13)
        "is_goalkeeper": bool,
        "kit_color": str,                # Primary hex color
        "accent_color": str,             # Accent hex color
        "border_color": str,             # Border hex color
        "attacking_dir": float,          # +1.0 (left-to-right) or -1.0 (right-to-left)
        "identity_confidence": str,      # 'verified' or 'unknown'
      }
    """
    base_match, half_key = parse_match_and_half(match_key_or_half, abs_frame)
    cfg = MATCH_CONFIG.get(base_match, MATCH_CONFIG["game_39"])
    home_code = cfg["home"]

    # Resolve canonical team code from side mapping
    side_map = MATCH_HALF_SIDE_MAPPING.get(half_key, MATCH_HALF_SIDE_MAPPING.get(f"{base_match}_H1", {}))
    team_code = side_map.get(raw_side_id, home_code if raw_side_id == 0 else cfg["away"])

    is_home = (team_code == home_code)
    norm_team_id = 0 if is_home else 1

    team_data = CANONICAL_TEAMS.get(team_code, CANONICAL_TEAMS["NEW"])
    roster = team_data.get("roster", {})

    # In FOOTPASS H5:
    # side_id == 0 defends left goal (x ≈ 0.1), attacks right (+X direction -> +1.0)
    # side_id == 1 defends right goal (x ≈ 0.9), attacks left (-X direction -> -1.0)
    attacking_dir = 1.0 if raw_side_id == 0 else -1.0

    p_info = roster.get(shirt_num)
    if p_info:
        full_name = p_info["name"]
        last_name = full_name.split()[-1]
        display_label = f"#{shirt_num} {last_name}"
        position = p_info["pos"]
        role = p_info["role"]
        confidence = "verified"
    else:
        # Fallback if player not in starter/sub roster
        full_name = f"#{shirt_num}" if (shirt_num and shirt_num > 0) else (f"ID {player_id}" if player_id is not None else "Unknown")
        display_label = full_name
        position = "MF"
        role = 6
        confidence = "unknown"

    is_gk = (role == 1 or shirt_num in (1, 13, 16, 22, 24, 26, 30, 99) and position == "GK")

    return {
        "raw_side_id": int(raw_side_id),
        "team_id": norm_team_id,
        "team_code": team_code,
        "team_name": team_data["name"],
        "team_short": team_data["short_name"],
        "is_home": is_home,
        "name": full_name,
        "display_label": display_label,
        "shirt": int(shirt_num),
        "pos": position,
        "role": int(role),
        "is_goalkeeper": is_gk,
        "kit_color": team_data["primary_color"],
        "accent_color": team_data["accent_color"],
        "border_color": team_data["border_color"],
        "rgb": team_data["rgb"],
        "accent_rgb": team_data["accent_rgb"],
        "bgr": team_data["bgr"],
        "attacking_dir": attacking_dir,
        "identity_confidence": confidence,
    }


def get_match_meta(match_id: str) -> Optional[Dict[str, Any]]:
    """
    Backward-compatible match metadata dictionary formatted for legacy consumers.
    Exposes:
      - teams: { 0: HomeTeamDict, 1: AwayTeamDict }
    """
    base_match, half_key = parse_match_and_half(match_id)
    cfg = MATCH_CONFIG.get(base_match)
    if not cfg:
        return None

    home_code = cfg["home"]
    away_code = cfg["away"]
    home_t = CANONICAL_TEAMS[home_code]
    away_t = CANONICAL_TEAMS[away_code]

    # Resolve attacking direction for this half
    side_map = MATCH_HALF_SIDE_MAPPING.get(half_key, {0: home_code, 1: away_code})
    home_side = 0 if side_map.get(0) == home_code else 1
    away_side = 1 - home_side

    return {
        "match_id": base_match,
        "half_key": half_key,
        "match_name": cfg["match_name"],
        "competition": cfg["competition"],
        "date": cfg["date"],
        "venue": cfg["venue"],
        "home_code": home_code,
        "away_code": away_code,
        "teams": {
            0: {
                "name": home_t["name"],
                "short_name": home_t["short_name"],
                "code": home_t["code"],
                "bgr": home_t["bgr"],
                "rgb": home_t["rgb"],
                "accent_rgb": home_t["accent_rgb"],
                "primary_color": home_t["primary_color"],
                "accent_color": home_t["accent_color"],
                "is_home": True,
                "attacking_dir": 1.0 if home_side == 0 else -1.0,
                "roster": home_t["roster"],
            },
            1: {
                "name": away_t["name"],
                "short_name": away_t["short_name"],
                "code": away_t["code"],
                "bgr": away_t["bgr"],
                "rgb": away_t["rgb"],
                "accent_rgb": away_t["accent_rgb"],
                "primary_color": away_t["primary_color"],
                "accent_color": away_t["accent_color"],
                "is_home": False,
                "attacking_dir": 1.0 if away_side == 0 else -1.0,
                "roster": away_t["roster"],
            },
        },
    }


def get_team_name(match_id: str, team_id: Optional[int], use_short: bool = False) -> str:
    """Get verified team name (team_id: 0 = Home, 1 = Away)."""
    if team_id is None:
        return "Neutral / Contested"
    meta = get_match_meta(match_id)
    if meta and team_id in meta["teams"]:
        t = meta["teams"][team_id]
        return t["short_name"] if use_short else t["name"]
    return f"Team {team_id}"


def get_player_name(match_id: str, team_id: Optional[int], shirt: Optional[int]) -> Optional[str]:
    """Retrieve verified player name by normalized team_id and shirt number."""
    if team_id is None or shirt is None:
        return None
    meta = get_match_meta(match_id)
    if meta and team_id in meta["teams"]:
        roster = meta["teams"][team_id].get("roster", {})
        if shirt in roster:
            return roster[shirt]["name"]
    return None


def get_player_display_label(match_id: str, team_id: Optional[int], shirt: Optional[int]) -> str:
    """Format player display label (e.g. '#5 Schär')."""
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
    Resolve attacking direction (+1.0 for Left-to-Right, -1.0 for Right-to-Left).
    team_id: 0 = Home, 1 = Away.
    """
    if match_id:
        meta = get_match_meta(match_id)
        if meta and possessing_team in meta["teams"]:
            return float(meta["teams"][possessing_team]["attacking_dir"])

    # Fallback to Goalkeeper position (role == 1)
    if players:
        for p in players:
            p_role = getattr(p, "role", None)
            p_team = getattr(p, "team_id", getattr(p, "team", None))
            if p_role is None and isinstance(p, (list, tuple)) and len(p) > 4:
                p_role = int(p[4])
                p_team = int(p[2])
            
            if p_team == possessing_team and p_role == 1:
                gx = getattr(p, "pitch_x", None)
                if gx is not None:
                    return 1.0 if gx < 0.5 else -1.0

    return 1.0 if possessing_team == 0 else -1.0


# Legacy dict exposing get_match_meta results for backwards compatibility
MATCH_TEAM_METADATA: Dict[str, Any] = {
    m: get_match_meta(m)
    for m in (
        "game_27", "game_39", "game_49", "game_51",
        "game_27_H1", "game_27_H2", "game_39_H1", "game_39_H2",
        "game_49_H1", "game_49_H2", "game_51_H1", "game_51_H2"
    )
}

