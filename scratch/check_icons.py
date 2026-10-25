import os
import re

src_dir = 'webapp/frontend/src'
for root, dirs, files in os.walk(src_dir):
    for file in files:
        if file.endswith('.jsx'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            import_matches = re.findall(r'import\s*\{(.*?)\}\s*from\s*[\'"]lucide-react[\'"]', content, re.DOTALL)
            imported = set()
            for m in import_matches:
                for item in m.split(','):
                    item = item.strip()
                    if item:
                        imported.add(item)
            
            # also local component imports or React components
            jsx_tags = set(re.findall(r'<([A-Z][A-Za-z0-9]+)', content))
            # filter out common components
            known = {
                'App', 'VideoPlayer', 'TacticalPitch2D', 'ContextualAnalysisPanel',
                'PlayerSelectionBar', 'MatchSelector', 'ErrorBoundary', 'React'
            }
            # check what looks like a Lucide icon (usually PascalCase, not standard HTML)
            # check against common lucide names
            for tag in jsx_tags:
                if tag not in known and tag not in imported:
                    # check if tag is defined in file (const Tag = ... or function Tag)
                    if not re.search(r'\b(const|function|class|let|var)\s+' + tag + r'\b', content) and not re.search(r'import\s+' + tag + r'\b', content) and not re.search(r'import\s*\{[^}]*\b' + tag + r'\b', content):
                        print(f"File {file}: Potential missing tag/icon: {tag}")
