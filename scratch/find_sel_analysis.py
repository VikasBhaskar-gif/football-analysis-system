import os
import re

for root, dirs, files in os.walk('.'):
    if '.git' in root or 'node_modules' in root or '.venv' in root or 'venv' in root:
        continue
    for file in files:
        if file.endswith(('.py', '.jsx', '.js', '.json')):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'selection_analysis' in content:
                    print(f"Match in {filepath}")
            except Exception:
                pass
