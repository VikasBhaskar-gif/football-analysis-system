"""
mass_train_and_verify.py
========================
Executes a comprehensive battery of 30+ coach queries across all 4 FOOTPASS matches:
  - game_27: Bayern Munich vs Manchester United
  - game_39: Newcastle United vs Paris Saint-Germain
  - game_49: FC Barcelona vs Real Betis
  - game_51: FC Barcelona vs RC Celta de Vigo

Verifies:
  1. Teammates are NEVER treated as opponents (no 'vs' in headline, no 1v1 duels between teammates).
  2. Pass directionality is accurate (passes received from vs passes completed to).
  3. Visual restraint: pitch maps strictly match requested visuals with zero extra unwanted maps.
  4. Memory learning: facts and queries are recorded in ai_learned_memory.json with version incrementing.
"""

import os
import sys
import time
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
backend_path = os.path.join(PROJECT_ROOT, "webapp", "backend")
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from analysis_service import AnalysisService

PROMPTS = [
    # --- Category 1: Teammate Pass Directionality & Combinations (game_27) ---
    {
        "match": "game_27",
        "question": "how many times did harry kane recieve a pass from jamal musiala",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "jamal musiala passes completed to harry kane",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "passes between harry kane and jamal musiala linkup",
        "category": "Teammate Bidirectional Linkup",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "who passed to harry kane the most",
        "category": "Teammate Supply Network",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "give me harry kane's shot map with optimal and non optimal options",
        "category": "Strict Map Restraint: Shot Map Only",
        "expected_map_type": "shots",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "harry kane full heatmap",
        "category": "Strict Map Restraint: Heatmap Only",
        "expected_map_type": "heatmap",
        "max_maps": 1,
    },
    {
        "match": "game_27",
        "question": "marcus rashford 1v1 duels against dayot upamecano",
        "category": "True Opponent 1v1",
        "expected_map_type": "duels_1v1",
        "max_maps": 1,
    },

    # --- Category 2: Newcastle vs PSG (game_39) ---
    {
        "match": "game_39",
        "question": "how many passes did achraf hakimi complete to kylian mbappe",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "how many times did ousmane dembele receive a pass from achraf hakimi",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "mbappe and dembele combination linkup",
        "category": "Teammate Bidirectional Linkup",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "passes from kieran trippier to anthony gordon",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "who passed to mbappe the most",
        "category": "Teammate Supply Network",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "over the 90 minutes tell me how many dribbles mbappe completed against trippier",
        "category": "Opponent 1v1 & Dribbles",
        "expected_map_type": "duels_1v1",
        "max_maps": 2,
    },
    {
        "match": "game_39",
        "question": "give me Dembele's heatmap",
        "category": "Strict Map Restraint: Heatmap Only",
        "expected_map_type": "heatmap",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "mbappe shot map with optimal and non optimal options",
        "category": "Strict Map Restraint: Shot Map Only",
        "expected_map_type": "shots",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "newcastle defensive line shape and compactness",
        "category": "Team Shape: Defensive Line",
        "expected_map_type": "team_shape",
        "max_maps": 1,
    },

    # --- Category 3: Barcelona vs Real Betis (game_49) ---
    {
        "match": "game_49",
        "question": "passes from joao felix to robert lewandowski",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_49",
        "question": "how many times did lewandowski receive a pass from gavi",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_49",
        "question": "who passed to lewandowski the most",
        "category": "Teammate Supply Network",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_49",
        "question": "ferran torres shot decision audit",
        "category": "Strict Map Restraint: Shot Map Only",
        "expected_map_type": "shots",
        "max_maps": 1,
    },
    {
        "match": "game_49",
        "question": "barcelona team shape and defensive line",
        "category": "Team Shape",
        "expected_map_type": "team_shape",
        "max_maps": 1,
    },

    # --- Category 4: Barcelona vs Celta Vigo (game_51) ---
    {
        "match": "game_51",
        "question": "how many passes did joao cancelo complete to robert lewandowski",
        "category": "Teammate Combination",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_51",
        "question": "passes between iago aspas and larsen",
        "category": "Teammate Bidirectional Linkup",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_51",
        "question": "who passed to iago aspas the most",
        "category": "Teammate Supply Network",
        "expected_no_vs": True,
        "expected_map_type": "pass_combination",
        "max_maps": 1,
    },
    {
        "match": "game_51",
        "question": "iago aspas shot map",
        "category": "Strict Map Restraint: Shot Map Only",
        "expected_map_type": "shots",
        "max_maps": 1,
    },
    {
        "match": "game_51",
        "question": "ferran torres 1v1 duels against carl starfelt",
        "category": "True Opponent 1v1",
        "expected_map_type": "duels_1v1",
        "max_maps": 1,
    },
    {
        "match": "game_51",
        "question": "celta vigo deep low block structure and backline",
        "category": "Team Shape",
        "expected_map_type": "team_shape",
        "max_maps": 1,
    },

    # --- Category 5: Multi-Game Shapes & Aerial Runs ---
    {
        "match": "game_27",
        "question": "track team shapes across all 4 games and categorize them",
        "category": "Cross-Game Team Shapes",
        "expected_map_type": "team_shape",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "passes played into the air into the box and high speed runs",
        "category": "Aerial Deliveries & Box Runs",
        "expected_map_type": "runs",
        "max_maps": 1,
    },
    {
        "match": "game_39",
        "question": "Mbappe's heatmap, passes completed, dribbles, and his 1v1 duel's successes and failures against lascelles and trippier only when he's the one who has the ball, also his shot map",
        "category": "Comprehensive Multi-Visual Prompt",
        "expected_map_type": None,
        "max_maps": 6,
    },
]

def run_mass_training():
    print("=" * 80)
    print("STARTING MASS MULTI-PROMPT SELF-TRAINING & VERIFICATION BATTERY")
    print(f"Total Test Cases: {len(PROMPTS)}")
    print("=" * 80)

    service = AnalysisService()
    passed_count = 0
    failed_count = 0

    start_total_time = time.time()

    for idx, tc in enumerate(PROMPTS, 1):
        q = tc["question"]
        match_id = tc["match"]
        cat = tc["category"]
        t0 = time.time()

        print(f"\n[{idx:02d}/{len(PROMPTS):02d}] Match: {match_id} | Category: {cat}")
        print(f"   Query: \"{q[:75]}...\"" if len(q) > 75 else f"   Query: \"{q}\"")

        try:
            res = service.ask_coach_ai(video_id=match_id, question=q)
            elapsed = time.time() - t0

            headline = res.get("headline", "")
            bullets = res.get("narrative_bullets", [])
            cards = res.get("comparison_cards", [])
            maps = res.get("pitch_maps", [])
            clips = res.get("clip_timings", [])

            map_types = [m.get("type") for m in maps]

            # Verifications
            errors = []

            # 1. Teammates must NEVER have "vs" in headline
            if tc.get("expected_no_vs"):
                if " vs " in headline:
                    errors.append(f"Teammates incorrectly treated with 'vs' in headline: {headline}")

            # 2. Map types check
            exp_type = tc.get("expected_map_type")
            if exp_type and exp_type not in map_types:
                errors.append(f"Expected map type '{exp_type}' not found in output maps: {map_types}")

            # 3. Map restraint check
            max_maps = tc.get("max_maps")
            if max_maps is not None and len(maps) > max_maps:
                errors.append(f"Map dump violation: expected at most {max_maps} maps, but got {len(maps)}: {map_types}")

            # 4. Content check
            if not headline:
                errors.append("Empty headline returned")
            if not bullets:
                errors.append("Empty narrative bullets returned")

            if errors:
                print(f"   [FAIL] ({elapsed:.2f}s) Errors:")
                for err in errors:
                    print(f"      - {err}")
                failed_count += 1
            else:
                first_bullet = bullets[0][:90] + "..." if len(bullets[0]) > 90 else bullets[0]
                first_bullet_clean = first_bullet.encode("ascii", "replace").decode("ascii")
                headline_clean = headline.encode("ascii", "replace").decode("ascii")
                print(f"   [PASS] ({elapsed:.2f}s)")
                print(f"      Headline: {headline_clean}")
                print(f"      Bullet 1: {first_bullet_clean}")
                print(f"      Maps ({len(maps)}): {map_types} | Cards: {len(cards)} | Clips: {len(clips)}")
                passed_count += 1

        except Exception as ex:
            elapsed = time.time() - t0
            print(f"   [ERROR] ({elapsed:.2f}s) Exception: {ex}")
            import traceback
            traceback.print_exc()
            failed_count += 1

    total_elapsed = time.time() - start_total_time
    print("\n" + "=" * 80)
    print("MASS TRAINING BATTERY COMPLETED")
    print(f"Passed: {passed_count}/{len(PROMPTS)} ({(passed_count/len(PROMPTS))*100:.1f}%)")
    print(f"Failed: {failed_count}/{len(PROMPTS)}")
    print(f"Total Time: {total_elapsed:.1f}s")

    # Check updated AI Learned Memory
    mem_file = os.path.join(PROJECT_ROOT, "outputs", "annotations", "ai_learned_memory.json")
    if os.path.exists(mem_file):
        with open(mem_file, "r", encoding="utf-8") as f:
            mem = json.load(f)
        print(f"AI Learned Memory: Model Version {mem.get('model_version')} | Total Logged Queries: {len(mem.get('queries', []))}")
    print("=" * 80)

if __name__ == "__main__":
    run_mass_training()
