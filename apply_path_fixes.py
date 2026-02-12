"""
Apply all path fixes to index.html:
1. Replace old flat paths with new subdirectory paths
2. Handle unmatched references
3. Generate complete file listing per designer for gallery_manifest.json update
"""
import re
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = Path(r"D:\history of id course\index.html")
IMAGES_DIR = Path(r"D:\history of id course\images")
BASE_DIR = Path(r"D:\history of id course")

# Load the mapping
mapping_file = Path(r"D:\history of id course\path_mapping.json")
mapping = json.loads(mapping_file.read_text(encoding='utf-8'))

# Manual additions for unmatched refs
manual_fixes = {
    # Portraits - map to best available file in subdirectory
    'images/ettore_sottsass.jpg': 'images/sottsass/sottsass_and_fernanda_pivano_1969.jpg',
    'images/marcel breuer.png': 'images/breuer/breuer_marcel_datestone.jpg',
    'images/walter_benjamin.jpg': 'images/behrens/Peter_Behrens_by_Rudolf_D%C3%BChrkoop_-_MKG_%28cropped%29.jpg',  # placeholder
    'images/breuer_interior.jpg': 'images/breuer/breuer_breuer_house.jpg',
    # Icons - these don't exist, we'll check if they're actually needed
    # They are used for v-era-icon backgrounds on the timeline
    'images/icon_art_nouveau.png': 'images/icon_art_nouveau.png',  # keep as-is
    'images/icon_arts_crafts.png': 'images/icon_arts_crafts.png',
    'images/icon_bauhaus.png': 'images/icon_bauhaus.png',
    'images/icon_digital_ux.png': 'images/icon_digital_ux.png',
    'images/icon_functionalism.png': 'images/icon_functionalism.png',
    'images/icon_memphis.png': 'images/icon_memphis.png',
    # Dresser Komai jug - doesn't exist in filesystem; will skip
    "images/dresser/A_Victorian_%27Komai%27_solid_silver_water_jug_by_Christopher_Dresser%2C_c.1880.jpg": "images/dresser/A_Victorian_%27Komai%27_solid_silver_water_jug_by_Christopher_Dresser%2C_c.1880.jpg",
}

mapping.update(manual_fixes)

# Read HTML
html = HTML_FILE.read_text(encoding='utf-8')
original = html

# Apply replacements
changes = 0
for old_path, new_path in sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True):
    if old_path == new_path:
        continue
    count = html.count(old_path)
    if count > 0:
        html = html.replace(old_path, new_path)
        changes += count
        print(f"  Replaced ({count}x): {old_path}")
        print(f"        -> {new_path}")

# Write back
HTML_FILE.write_text(html, encoding='utf-8')
print(f"\nTotal replacements: {changes}")
print(f"File saved: {HTML_FILE}")

# Also generate a complete catalog of all images per designer
print(f"\n=== GENERATING IMAGE CATALOG ===")
catalog = {}
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
for d in sorted(IMAGES_DIR.iterdir()):
    if d.is_dir() and not d.name.startswith('_'):
        files = []
        for f in sorted(d.rglob('*')):
            if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
                rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
                files.append(rel)
        if files:
            catalog[d.name] = files
            print(f"  {d.name}: {len(files)} images")

# Save catalog
cat_file = Path(r"D:\history of id course\image_catalog.json")
cat_file.write_text(json.dumps(catalog, indent=2), encoding='utf-8')
print(f"\nCatalog saved to {cat_file}")
