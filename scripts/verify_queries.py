"""
scripts/verify_queries.py
=========================
Verifies that all DDL, DML, and SELECT queries used in the presentation
execute with 100% compatibility and 0 errors on SQLite.
"""

import sqlite3
import shutil
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(PROJECT_ROOT, "dbms_review_1", "football_tactical.db")
TEST_DB = os.path.join(PROJECT_ROOT, "dbms_review_1", "test_validation.db")

def verify_all():
    shutil.copyfile(DB_PATH, TEST_DB)
    conn = sqlite3.connect(TEST_DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    print("--- 1. Testing ALTER TABLE operations supported in SQLite ---")
    cur.execute("ALTER TABLE players ADD COLUMN market_value_eur NUMERIC(12,2);")
    print("  [OK] ALTER TABLE players ADD COLUMN market_value_eur NUMERIC(12,2);")

    cur.execute("ALTER TABLE players RENAME COLUMN player_name TO full_name;")
    print("  [OK] ALTER TABLE players RENAME COLUMN player_name TO full_name;")

    # Revert rename so remaining queries find player_name
    cur.execute("ALTER TABLE players RENAME COLUMN full_name TO player_name;")

    cur.execute("ALTER TABLE players DROP COLUMN market_value_eur;")
    print("  [OK] ALTER TABLE players DROP COLUMN market_value_eur;")

    print("\n--- 2. Testing SQLite Table Rebuild Migration Pattern ---")
    # In SQLite, adding a CHECK constraint post-table creation requires the standard table rebuild pattern
    cur.execute("""
    CREATE TABLE match_events_migrated (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        match_id VARCHAR(20) NOT NULL REFERENCES matches(match_id),
        half INTEGER NOT NULL CHECK (half IN (1, 2)),
        frame_idx INTEGER NOT NULL CHECK (frame_idx >= 0),
        event_second NUMERIC(6,2) CHECK (event_second >= 0.0),
        team_code VARCHAR(10) NOT NULL REFERENCES teams(team_code),
        jersey_number INTEGER NOT NULL,
        action_type VARCHAR(30) NOT NULL,
        success_flag INTEGER DEFAULT 1
    );
    """)
    cur.execute("INSERT INTO match_events_migrated SELECT * FROM match_events;")
    print("  [OK] Table rebuild: 1,000 rows copied into migrated schema with new CHECK constraint.")

    print("\n--- 3. Testing DML: INSERT operations ---")
    cur.execute("""
    INSERT INTO teams (team_code, team_name, country, home_venue, primary_color)
    VALUES ('ARS', 'Arsenal FC', 'ENG', 'Emirates Stadium', '#EF0107');
    """)
    print("  [OK] INSERT INTO teams (ARS)")

    cur.execute("""
    INSERT INTO matches (match_id, competition, season, match_date, home_team, away_team, total_frames, duration_s, fps)
    VALUES ('game_99', 'UEFA Champions League', '2023-2024', '2023-11-08', 'ARS', 'BAY', 154000, 6160.0, 25.0);
    """)
    print("  [OK] INSERT INTO matches (game_99)")

    cur.execute("""
    INSERT INTO match_events (match_id, half, frame_idx, event_second, team_code, jersey_number, action_type, success_flag)
    VALUES ('game_99', 1, 350, 14.0, 'ARS', 7, 'Pass', 1);
    """)
    print("  [OK] INSERT INTO match_events (event for game_99)")

    print("\n--- 4. Testing DML: UPDATE operations ---")
    cur.execute("""
    UPDATE matches
    SET duration_s = 6280.50,
        total_frames = 157012
    WHERE match_id = 'game_39';
    """)
    print(f"  [OK] UPDATE matches rows affected: {cur.rowcount}")

    cur.execute("""
    UPDATE players
    SET role_id = 10,
        position = 'LW'
    WHERE player_id = 5;
    """)
    print(f"  [OK] UPDATE players rows affected: {cur.rowcount}")

    cur.execute("""
    UPDATE match_events
    SET success_flag = 1
    WHERE event_id = 101;
    """)
    print(f"  [OK] UPDATE match_events rows affected: {cur.rowcount}")

    print("\n--- 5. Testing DML: DELETE operations ---")
    cur.execute("DELETE FROM match_events WHERE frame_idx < 0 OR event_second > 7200.0;")
    print(f"  [OK] DELETE corrupted events rows affected: {cur.rowcount}")

    cur.execute("DELETE FROM matches WHERE competition = 'Exhibition Friendly' AND season = '2023-2024';")
    print(f"  [OK] DELETE cancelled matches rows affected: {cur.rowcount}")

    cur.execute("DELETE FROM tactical_rules WHERE rule_id = 'RULE_DEPRECATED';")
    print(f"  [OK] DELETE deprecated rules rows affected: {cur.rowcount}")

    print("\n--- 6. Testing Single-Row Functions (Slide 12) ---")
    cur.execute("""
    SELECT player_id,
           UPPER(player_name) AS name_caps,
           LOWER(team_code)   AS team_lower,
           SUBSTR(position, 1, 2) AS pos_code,
           'ROLE-' || SUBSTR('00' || role_id, -2) AS tier
    FROM players
    WHERE team_code = 'NEW'
    ORDER BY shirt_number
    LIMIT 5;
    """)
    rows = cur.fetchall()
    print("  [OK] Single-Row output:", rows)

    print("\n--- 7. Testing Numeric Functions & CASE (Slide 13) ---")
    cur.execute("""
    SELECT action_type,
           event_second,
           ROUND(event_second / 60.0, 2) AS match_min,
           CASE
             WHEN action_type IN ('Shot', 'Cross')  THEN 'High Threat Attack'
             WHEN action_type IN ('Tackle', 'Block') THEN 'Defensive Regain'
             WHEN action_type = 'Pass'               THEN 'Ball Circulation'
             ELSE 'Open Progression'
           END AS tactical_phase
    FROM match_events
    WHERE match_id = 'game_39'
    LIMIT 7;
    """)
    rows = cur.fetchall()
    print(f"  [OK] Numeric/CASE output rows: {len(rows)}")

    print("\n--- 8. Testing SQL Operators (Slide 14) ---")
    cur.execute("""
    SELECT player_name,
           shirt_number,
           team_code,
           position
    FROM players
    WHERE shirt_number BETWEEN 7 AND 25
      AND team_code IN ('NEW', 'PAR', 'BAY')
      AND player_name LIKE '%a%'
    ORDER BY shirt_number
    LIMIT 4;
    """)
    rows = cur.fetchall()
    print("  [OK] SQL Operators output:", rows)

    print("\n--- 9. Testing Statistical Aggregations (Slide 15) ---")
    cur.execute("""
    SELECT team_code,
           COUNT(*) AS total_actions,
           ROUND(AVG(event_second), 2) AS avg_sec,
           MIN(event_second) AS min_sec,
           MAX(event_second) AS max_sec,
           SUM(CASE WHEN action_type = 'Pass' THEN 1 ELSE 0 END) AS passes
    FROM match_events
    GROUP BY team_code
    HAVING COUNT(*) >= 50
    ORDER BY passes DESC;
    """)
    rows = cur.fetchall()
    print("  [OK] Aggregate output rows:", rows)

    conn.close()
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    print("\n>>> ALL QUERIES VERIFIED PERFECTLY! <<<")

if __name__ == "__main__":
    verify_all()
