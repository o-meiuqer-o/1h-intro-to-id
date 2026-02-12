"""
Remap all DESIGN_WORKS image paths to actual files.
Strategy: use designer key + work keywords to fuzzy-match actual files.
Output: a JS snippet to replace the DESIGN_WORKS image paths.
"""
import re
import sys
import json
from pathlib import Path
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = Path(r"D:\history of id course\index.html")
IMAGES_DIR = Path(r"D:\history of id course\images")
BASE_DIR = Path(r"D:\history of id course")

# 1) Build actual file index per designer
actual = {}
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
for d in IMAGES_DIR.iterdir():
    if d.is_dir() and not d.name.startswith('_'):
        key = d.name
        actual[key] = []
        for f in sorted(d.rglob('*')):
            if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
                rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
                actual[key].append(rel)

# 2) Extract DESIGN_WORKS entries from HTML
html = HTML_FILE.read_text(encoding='utf-8')

# Find each entry like: 'keyname': { title: 'Title', image: 'images/path', ... }
pattern = r"'([^']+)':\s*\{\s*title:\s*'([^']*)',\s*image:\s*'([^']*)',\s*context:\s*'([^']*)',\s*influence:\s*'([^']*)',\s*analysis:\s*'([^']*)'"
entries = re.findall(pattern, html)
print(f"Found {len(entries)} DESIGN_WORKS entries")

# 3) Map designer prefix to folder key
designer_folder_map = {
    'christopher_dresser': 'dresser',
    'dresser': 'dresser',
    'peter_behrens': 'behrens',
    'behrens': 'behrens',
    'walter_gropius': 'gropius',
    'gropius': 'gropius',
    'marianne_brandt': 'brandt',
    'brandt': 'brandt',
    'max_bill': 'bill',
    'bill': 'bill',
    'dieter_rams': 'rams',
    'rams': 'rams',
    'raymond_loewy': 'loewy',
    'loewy': 'loewy',
    'henry_dreyfuss': 'dreyfuss',
    'dreyfuss': 'dreyfuss',
    'charles_and_ray_eames': 'eames',
    'eames': 'eames',
    'ettore_sottsass': 'sottsass',
    'sottsass': 'sottsass',
    'jonathan_ive': 'ive',
    'ive': 'ive',
    'william_morris': 'morris',
    'morris': 'morris',
}

# 4) For each entry, find best matching actual file
replacements = {}
unmatched = []

for key, title, image_path, context, influence, analysis in entries:
    # Determine which designer folder to look in
    # Extract from the image path
    img_name = image_path.split('/')[-1].lower().replace('.jpg', '').replace('.png', '').replace('.webp', '')
    
    folder_key = None
    for prefix, folder in sorted(designer_folder_map.items(), key=lambda x: len(x[0]), reverse=True):
        if img_name.startswith(prefix):
            folder_key = folder
            break
    
    if not folder_key:
        # Try from key name
        for prefix, folder in sorted(designer_folder_map.items(), key=lambda x: len(x[0]), reverse=True):
            if key.startswith(prefix.split('_')[-1]) or key in ['teapot', 'factory', 'sk4', 't3', '606', 'imac', 'iphone', 'macbook']:
                folder_key = folder
                break
    
    if not folder_key or folder_key not in actual:
        unmatched.append((key, image_path, "no folder"))
        continue
    
    # Extract work keywords from image filename
    work_words = img_name
    for prefix in designer_folder_map:
        work_words = work_words.replace(prefix + '_', '')
    work_words = work_words.strip('_')
    
    # Also use title for matching
    title_lower = title.lower().replace(' ', '_').replace('-', '_')
    
    # Find best match in actual files
    best_match = None
    best_score = 0
    
    for actual_path in actual[folder_key]:
        actual_name = actual_path.split('/')[-1].lower().replace('.jpg', '').replace('.png', '').replace('.webp', '').replace('.jpeg', '')
        
        # Score: combination of keyword overlap and sequence matching
        score1 = SequenceMatcher(None, work_words, actual_name).ratio()
        score2 = SequenceMatcher(None, title_lower, actual_name).ratio()
        
        # Bonus for keyword containment
        bonus = 0
        for word in work_words.split('_'):
            if len(word) > 2 and word in actual_name:
                bonus += 0.15
        for word in title_lower.split('_'):
            if len(word) > 2 and word in actual_name:
                bonus += 0.1
        
        # Check for portrait match
        if 'portrait' in work_words and 'portrait' in actual_name:
            bonus += 0.5
        
        total = max(score1, score2) + bonus
        if total > best_score:
            best_score = total
            best_match = actual_path
    
    if best_match and best_score > 0.3:
        replacements[image_path] = best_match
    else:
        unmatched.append((key, image_path, f"score={best_score:.2f}"))

# 5) Output results
print(f"\nMatched: {len(replacements)}")
print(f"Unmatched: {len(unmatched)}")

print("\n--- MATCHES ---")
for old, new in sorted(replacements.items()):
    print(f"  {old}")
    print(f"    -> {new}")

print("\n--- UNMATCHED ---")
for key, path, reason in unmatched:
    print(f"  {key}: {path} ({reason})")

# 6) Save as JSON
out = Path(r"D:\history of id course\works_path_mapping.json")
out.write_text(json.dumps(replacements, indent=2), encoding='utf-8')
print(f"\nSaved to {out}")

# 7) Also apply the replacements to index.html
for old_path, new_path in replacements.items():
    html = html.replace(old_path, new_path)

HTML_FILE.write_text(html, encoding='utf-8')
print(f"Applied {len(replacements)} replacements to index.html")
