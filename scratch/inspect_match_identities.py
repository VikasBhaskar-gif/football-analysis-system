import os
import json
import h5py

print("Checking JSON files...")
for fname in [
    'football-ai/FOOTPASS/data/TAAD_sample_list.json',
    'football-ai/FOOTPASS/playbyplay_GT/playbyplay_train.json',
    'football-ai/FOOTPASS/playbyplay_GT/playbyplay_val.json'
]:
    if os.path.exists(fname):
        with open(fname, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"\n--- {fname} ---")
            if isinstance(data, dict):
                print(f"Total keys: {len(data)}")
                for target in ['game_27', 'game_39', 'game_49', 'game_51', '27', '39', '49', '51']:
                    matches = [k for k in data.keys() if target in k]
                    if matches:
                        print(f"  Target '{target}' in keys: {matches[:5]}")
                        # print first matched content
                        print(f"  Sample data for {matches[0]}: {str(data[matches[0]])[:200]}")
            elif isinstance(data, list):
                print(f"Total items: {len(data)}")
                for target in ['game_27', 'game_39', 'game_49', 'game_51']:
                    matches = [x for x in data if isinstance(x, str) and target in x or (isinstance(x, dict) and target in str(x))]
                    if matches:
                        print(f"  Found in list '{target}': {str(matches[0])[:200]}")

print("\nChecking H5 files...")
for h5_path in ['football-ai/FOOTPASS/data/train_tactical_data.h5', 'football-ai/FOOTPASS/data/val_tactical_data.h5']:
    if os.path.exists(h5_path):
        with h5py.File(h5_path, 'r') as hf:
            print(f"\n--- {h5_path} ---")
            print("Keys:", list(hf.keys())[:10])
            for target in ['game_27', 'game_39', 'game_49', 'game_51']:
                matches = [k for k in hf.keys() if target in k]
                if matches:
                    print(f"  Found '{target}': {matches}")
                    grp = hf[matches[0]]
                    print(f"    Sub-items in {matches[0]}:", list(grp.keys()) if hasattr(grp, 'keys') else grp.shape)
                    if hasattr(grp, 'attrs'):
                        print(f"    Attrs in {matches[0]}:", dict(grp.attrs))
