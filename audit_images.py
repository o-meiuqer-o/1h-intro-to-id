"""
Audit: find all image references in index.html and check which ones exist.
Then list all actual image files that aren't referenced.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = Path(r"D:\history of id course\index.html")
IMAGES_DIR = Path(r"D:\history of id course\images")
BASE_DIR = Path(r"D:\history of id course")

# 1) Extract all image references from index.html
html = HTML_FILE.read_text(encoding='utf-8')
# Match src="images/..." and url('images/...') patterns
refs_src = re.findall(r'src=["\']([^"\']+)["\']', html)
refs_url = re.findall(r"url\(['\"]?([^)\"']+)['\"]?\)", html)
refs_bg = re.findall(r'background-image:\s*url\(["\']?([^)"\']+)["\']?\)', html)

all_refs = set()
for r in refs_src + refs_url + refs_bg:
    if r.startswith('images/') or r.startswith('./images/'):
        all_refs.add(r.replace('./images/', 'images/'))

print(f"=== IMAGE REFERENCES IN index.html: {len(all_refs)} ===\n")

# 2) Check which refs exist / don't exist
missing = []
found = []
for ref in sorted(all_refs):
    full_path = BASE_DIR / ref
    if full_path.exists():
        found.append(ref)
    else:
        missing.append(ref)

print(f"Found (working): {len(found)}")
print(f"Missing (broken): {len(missing)}\n")

if missing:
    print("--- BROKEN REFERENCES ---")
    for m in sorted(missing):
        print(f"  BROKEN: {m}")

# 3) List actual files not referenced 
print(f"\n--- ACTUAL FILES NOT REFERENCED ---")
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
actual_files = set()
for f in IMAGES_DIR.rglob('*'):
    if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
        rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
        actual_files.add(rel)

unreferenced = actual_files - all_refs
print(f"Total actual image files: {len(actual_files)}")
print(f"Unreferenced files: {len(unreferenced)}\n")
for u in sorted(unreferenced):
    print(f"  UNUSED: {u}")
