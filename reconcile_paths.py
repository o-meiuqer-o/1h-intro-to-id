"""
Build a reconciliation map from old flat image paths in index.html
to new subdirectory-based paths. Uses fuzzy matching on filenames.
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

# 1) Extract all image references from index.html
html = HTML_FILE.read_text(encoding='utf-8')
refs_src = re.findall(r'src=["\']([^"\']+)["\']', html)
refs_url = re.findall(r"url\(['\"]?([^)\"']+)['\"]?\)", html)

all_refs = set()
for r in refs_src + refs_url:
    if 'images/' in r:
        all_refs.add(r)

# 2) Build list of actual files
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg'}
actual_files = {}
for f in IMAGES_DIR.rglob('*'):
    if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
        rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
        # Key by just the filename (lowercase, no ext for matching)
        stem = f.stem.lower()
        if stem not in actual_files:
            actual_files[stem] = []
        actual_files[stem].append(rel)

# Also index by full filename with ext
actual_by_name = {}
for f in IMAGES_DIR.rglob('*'):
    if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
        rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
        actual_by_name[f.name.lower()] = rel
        # Also try without URL encoding
        import urllib.parse
        decoded = urllib.parse.unquote(f.name).lower()
        actual_by_name[decoded] = rel

# 3) Try to match each broken ref to an actual file
mapping = {}
unmatched = []

for ref in sorted(all_refs):
    full_path = BASE_DIR / ref
    if full_path.exists():
        mapping[ref] = ref  # Already correct
        continue

    # Extract filename from ref
    ref_filename = ref.split('/')[-1].lower()
    ref_stem = Path(ref_filename).stem

    # Try exact name match (with possible extension change)
    matched = False
    
    # Direct name match
    if ref_filename in actual_by_name:
        mapping[ref] = actual_by_name[ref_filename]
        matched = True
        continue
    
    # Try without extension (PNG->JPG conversion)
    for ext in ['.jpg', '.jpeg', '.png', '.webp']:
        candidate = ref_stem + ext
        if candidate in actual_by_name:
            mapping[ref] = actual_by_name[candidate]
            matched = True
            break
    
    if matched:
        continue

    # Try fuzzy matching on stem
    if ref_stem in actual_files:
        mapping[ref] = actual_files[ref_stem][0]
        continue

    # Try partial match - look for the ref_stem within actual stems
    best_match = None
    best_score = 0
    for stem, paths in actual_files.items():
        # Check if ref_stem is contained in stem or vice versa
        if ref_stem in stem or stem in ref_stem:
            score = SequenceMatcher(None, ref_stem, stem).ratio()
            if score > best_score:
                best_score = score
                best_match = paths[0]

    if best_match and best_score > 0.6:
        mapping[ref] = best_match
    else:
        unmatched.append(ref)

# 4) Output results
print(f"=== RECONCILIATION MAP ===")
print(f"Total refs: {len(all_refs)}")
print(f"Matched: {len(mapping)}")
print(f"Unmatched: {len(unmatched)}\n")

print("--- MATCHED ---")
for old, new in sorted(mapping.items()):
    if old != new:
        print(f"  {old}")
        print(f"    -> {new}")

print(f"\n--- UNMATCHED ({len(unmatched)}) ---")
for u in sorted(unmatched):
    print(f"  ?? {u}")

# 5) Save mapping as JSON
out = Path(r"D:\history of id course\path_mapping.json")
out.write_text(json.dumps(mapping, indent=2), encoding='utf-8')
print(f"\nMapping saved to {out}")
