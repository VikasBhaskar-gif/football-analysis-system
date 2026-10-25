"""
build_dbms_database.py
======================
Builds and populates the SQLite relational database for the DBMS Review 1 Case Study:
'Football Tactical Analytics Database' using authentic project data.
"""

import os
import sys
import sqlite3
import json
import csv

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from src.tactical.team_metadata import CANONICAL_TEAMS

def main():
    os.makedirs(os.path.join(PROJECT_ROOT, "dbms_review_1"), exist_ok=True)
    db_path = os.path.join(PROJECT_ROOT, "dbms_review_1", "football_tactical.db")
    
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. TEAMS table
    cur.execute('''
    CREATE TABLE teams (
        team_code VARCHAR(10) PRIMARY KEY,
        team_name VARCHAR(60) NOT NULL UNIQUE,
        country VARCHAR(30) NOT NULL,
        home_venue VARCHAR(80),
        primary_color VARCHAR(10) DEFAULT '#FFFFFF'
    );
    ''')

    # 2. MATCHES table
    cur.execute('''
    CREATE TABLE matches (
        match_id VARCHAR(20) PRIMARY KEY,
        competition VARCHAR(50) NOT NULL,
        season VARCHAR(10) DEFAULT '2023-2024',
        match_date DATE,
        home_team VARCHAR(10) NOT NULL REFERENCES teams(team_code),
        away_team VARCHAR(10) NOT NULL REFERENCES teams(team_code),
        total_frames INTEGER CHECK (total_frames > 0),
        duration_s NUMERIC(7,2) CHECK (duration_s > 0),
        fps NUMERIC(4,1) DEFAULT 25.0,
        CONSTRAINT chk_diff_teams CHECK (home_team <> away_team)
    );
    ''')

    # 3. PLAYERS table
    cur.execute('''
    CREATE TABLE players (
        player_id INTEGER PRIMARY KEY,
        team_code VARCHAR(10) NOT NULL REFERENCES teams(team_code),
        shirt_number INTEGER NOT NULL CHECK (shirt_number BETWEEN 1 AND 99),
        player_name VARCHAR(60) NOT NULL,
        position VARCHAR(10) NOT NULL,
        role_id INTEGER CHECK (role_id BETWEEN 1 AND 13),
        CONSTRAINT uq_team_shirt UNIQUE (team_code, shirt_number)
    );
    ''')

    # 4. MATCH_EVENTS table
    cur.execute('''
    CREATE TABLE match_events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id VARCHAR(20) NOT NULL REFERENCES matches(match_id),
        half INTEGER NOT NULL CHECK (half IN (1, 2)),
        frame_idx INTEGER NOT NULL CHECK (frame_idx >= 0),
        event_second NUMERIC(6,2),
        team_code VARCHAR(10) NOT NULL REFERENCES teams(team_code),
        jersey_number INTEGER NOT NULL,
        action_type VARCHAR(30) NOT NULL CHECK (action_type IN ('Pass', 'Drive', 'Cross', 'Shot', 'Header', 'Throw-in', 'Tackle', 'Block')),
        success_flag INTEGER DEFAULT 1 CHECK (success_flag IN (0, 1))
    );
    ''')

    # 5. TACTICAL_SNAPSHOTS table
    cur.execute('''
    CREATE TABLE tactical_snapshots (
        snapshot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id VARCHAR(20) NOT NULL REFERENCES matches(match_id),
        half INTEGER NOT NULL CHECK (half IN (1, 2)),
        frame_idx INTEGER NOT NULL,
        team_width_m NUMERIC(5,2) CHECK (team_width_m >= 0),
        team_length_m NUMERIC(5,2) CHECK (team_length_m >= 0),
        centroid_x NUMERIC(4,3) CHECK (centroid_x BETWEEN 0 AND 1),
        centroid_y NUMERIC(4,3) CHECK (centroid_y BETWEEN 0 AND 1),
        cluster_state VARCHAR(10),
        tactical_label VARCHAR(40)
    );
    ''')

    # 6. TACTICAL_RULES table
    cur.execute('''
    CREATE TABLE tactical_rules (
        rule_id VARCHAR(20) PRIMARY KEY,
        rule_name VARCHAR(50) NOT NULL UNIQUE,
        target_unit VARCHAR(30) NOT NULL,
        min_compactness NUMERIC(5,2),
        trigger_action VARCHAR(30),
        severity_level VARCHAR(15) DEFAULT 'MEDIUM' CHECK (severity_level IN ('LOW', 'MEDIUM', 'HIGH'))
    );
    ''')

    # Insert TEAMS
    teams_data = [
        ('NEW', 'Newcastle United', 'ENG', "St. James' Park", '#F8FAFC'),
        ('PAR', 'Paris Saint-Germain', 'FRA', 'Parc des Princes', '#1E293B'),
        ('BAY', 'Bayern Munich', 'GER', 'Allianz Arena', '#DC2626'),
        ('MUN', 'Manchester United', 'ENG', 'Old Trafford', '#991B1B'),
        ('BVB', 'Borussia Dortmund', 'GER', 'Signal Iduna Park', '#FACC15'),
        ('MIL', 'AC Milan', 'ITA', 'San Siro', '#B91C1C'),
        ('SAL', 'Red Bull Salzburg', 'AUT', 'Red Bull Arena', '#E2E8F0'),
        ('RSO', 'Real Sociedad', 'ESP', 'Reale Arena', '#2563EB'),
    ]
    cur.executemany('INSERT INTO teams VALUES (?, ?, ?, ?, ?)', teams_data)

    # Insert MATCHES
    matches_data = [
        ('game_39', 'UEFA Champions League', '2023-2024', '2023-10-04', 'NEW', 'PAR', 155054, 6202.16, 25.0),
        ('game_27', 'UEFA Champions League', '2023-2024', '2023-09-20', 'BAY', 'MUN', 145350, 5814.00, 25.0),
        ('game_49', 'UEFA Champions League', '2023-2024', '2023-10-04', 'BVB', 'MIL', 141200, 5648.00, 25.0),
        ('game_51', 'UEFA Champions League', '2023-2024', '2023-10-03', 'SAL', 'RSO', 148500, 5940.00, 25.0),
    ]
    cur.executemany('INSERT INTO matches VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', matches_data)

    # Insert PLAYERS from CANONICAL_TEAMS
    pid = 1
    for tcode, tmeta in CANONICAL_TEAMS.items():
        roster = tmeta.get('roster', {})
        for sn, pinfo in roster.items():
            cur.execute(
                'INSERT OR IGNORE INTO players (player_id, team_code, shirt_number, player_name, position, role_id) VALUES (?, ?, ?, ?, ?, ?)',
                (pid, tcode, int(sn), pinfo['name'], pinfo['pos'], int(pinfo['role']))
            )
            pid += 1

    # Insert real MATCH_EVENTS
    ACTION_MAP = {1: 'Drive', 2: 'Pass', 3: 'Cross', 4: 'Shot', 5: 'Header', 6: 'Throw-in', 7: 'Tackle', 8: 'Block'}
    TEAM_MAP = {
        'game_39_H1': {0: 'NEW', 1: 'PAR'},
        'game_27_H1': {0: 'BAY', 1: 'MUN'},
        'game_49_H1': {0: 'BVB', 1: 'MIL'},
        'game_51_H1': {0: 'SAL', 1: 'RSO'},
    }

    pbp_path = os.path.join(PROJECT_ROOT, 'football-ai', 'FOOTPASS', 'playbyplay_GT', 'playbyplay_train.json')
    with open(pbp_path, 'r', encoding='utf-8') as f:
        pbp = json.load(f)

    for gkey, tmap in TEAM_MAP.items():
        if gkey in pbp.get('events', {}):
            parts = gkey.split('_')
            mid = parts[0] + '_' + parts[1]
            half = 1 if '_H1' in gkey else 2
            for ev in pbp['events'][gkey][:250]:
                fr, t_side, sn, cls_id, succ = ev[0], ev[1], ev[2], ev[3], ev[4]
                tcode = tmap.get(t_side, 'NEW')
                act_name = ACTION_MAP.get(cls_id, 'Pass')
                cur.execute(
                    'INSERT INTO match_events (match_id, half, frame_idx, event_second, team_code, jersey_number, action_type, success_flag) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (mid, half, fr, round(fr / 25.0, 2), tcode, sn, act_name, succ)
                )

    # Insert TACTICAL_SNAPSHOTS
    k8_path = os.path.join(PROJECT_ROOT, 'outputs', 'k8_reference', 'k8_cluster_summary.csv')
    with open(k8_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row['cluster_id']
            rep_half = row['rep_half']
            parts = rep_half.split('_')
            mid = parts[0] + '_' + parts[1]
            half = 1 if '_H1' in rep_half else 2
            fr = int(row['rep_frame'])
            w = round(float(row['teamA_width']) * 68.0, 2)
            l = round(float(row['teamA_length']) * 105.0, 2)
            cx = round(float(row['teamA_centroid_x']), 3)
            cy = round(float(row['teamA_centroid_y']), 3)
            lbl = 'High Press Block' if cx > 0.55 else ('Deep Low Block' if cx < 0.35 else 'Midfield Structure')
            cur.execute(
                'INSERT INTO tactical_snapshots (match_id, half, frame_idx, team_width_m, team_length_m, centroid_x, centroid_y, cluster_state, tactical_label) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (mid, half, fr, w, l, cx, cy, cid, lbl)
            )

    # Insert TACTICAL_RULES
    rules = [
        ('RULE_01', 'High Press Compression', 'Defensive Unit', 25.0, 'Tackle', 'HIGH'),
        ('RULE_02', 'Flank Overload Isolation', 'Wide Attacking', 42.0, 'Cross', 'MEDIUM'),
        ('RULE_03', 'Central Penetration Block', 'Midfield Block', 18.5, 'Block', 'HIGH'),
        ('RULE_04', 'Deep Low Block Rest', 'Defensive Backline', 14.0, 'Shot', 'LOW'),
    ]
    cur.executemany('INSERT INTO tactical_rules VALUES (?, ?, ?, ?, ?, ?)', rules)

    conn.commit()

    n_teams = cur.execute('SELECT COUNT(*) FROM teams').fetchone()[0]
    n_matches = cur.execute('SELECT COUNT(*) FROM matches').fetchone()[0]
    n_players = cur.execute('SELECT COUNT(*) FROM players').fetchone()[0]
    n_events = cur.execute('SELECT COUNT(*) FROM match_events').fetchone()[0]
    n_snapshots = cur.execute('SELECT COUNT(*) FROM tactical_snapshots').fetchone()[0]
    n_rules = cur.execute('SELECT COUNT(*) FROM tactical_rules').fetchone()[0]

    print(f"Database created at: {db_path}")
    print(f"Records: {n_teams} teams, {n_matches} matches, {n_players} players, {n_events} match_events, {n_snapshots} tactical_snapshots, {n_rules} tactical_rules.")
    conn.close()

if __name__ == '__main__':
    main()
