
import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\history of id course"
CSV_PATH = os.path.join(BASE_DIR, "design_analysis.csv")
MANIFEST_PATH = os.path.join(BASE_DIR, "gallery_manifest.json")
JS_OUTPUT_PATH = os.path.join(BASE_DIR, "design_works_synced.js")
JSON_OUTPUT_PATH = os.path.join(BASE_DIR, "gallery_manifest_synced.json")

def escape_js(s):
    if not s: return ""
    return s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")

try:
    # 1. Read CSV and Verify Files
    valid_works = []
    missing_count = 0
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        print(f"Reading {CSV_PATH}...")
        for row in reader:
            rel_path = row['image']
            abs_path = os.path.join(BASE_DIR, rel_path)
            if os.path.exists(abs_path):
                valid_works.append(row)
            else:
                print(f"MISSING FILE: {rel_path} - Removing from galleries.")
                missing_count += 1
    
    print(f"\nVerified {len(valid_works)} valid works. Removed {missing_count} missing files.")

    # 2. Rebuild Gallery Manifest
    # Load existing to preserve metadata (bio, etc.)
    existing_manifest = {}
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, encoding='utf-8') as f:
            existing_manifest = json.load(f)

    new_manifest = {}
    
    # helper to find metadata for a designer key
    def get_meta(key):
        return existing_manifest.get(key, {})

    # Group valid works by designer
    works_by_designer = {}
    for work in valid_works:
        d_key = work['designer_key']
        if d_key not in works_by_designer:
            works_by_designer[d_key] = []
        works_by_designer[d_key].append(work['image'])

    # Build new manifest object
    for d_key, images in works_by_designer.items():
        meta = get_meta(d_key)
        # Use first work's designer name as fallback if not in meta
        designer_name = valid_works[0]['designer'] # distinct fallback
        # actually find the specific name for this key from valid_works
        for w in valid_works:
            if w['designer_key'] == d_key:
                designer_name = w['designer']
                break
        
        new_manifest[d_key] = {
            'name': meta.get('name', designer_name),
            'birth': meta.get('birth'),
            'death': meta.get('death'),
            'peakYear': meta.get('peakYear'),
            'bio': meta.get('bio', ''),
            'philosophy': meta.get('philosophy', ''),
            'integration': meta.get('integration', ''),
            'images': images # Only the verified existing images
        }

    # Write synced manifest
    with open(JSON_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(new_manifest, f, indent=2, ensure_ascii=False)
    print(f"Wrote {JSON_OUTPUT_PATH}")

    # 3. Rebuild DESIGN_WORKS JS
    js_lines = ["        const DESIGN_WORKS = {"]
    for work in valid_works:
        key = work['key']
        title = escape_js(work['title'])
        image = escape_js(work['image'])
        context = escape_js(work['context'])
        influence = escape_js(work['influence'])
        analysis = escape_js(work['analysis'])
        
        line = f"            '{key}': {{ title: '{title}', image: '{image}', context: '{context}', influence: '{influence}', analysis: '{analysis}' }},"
        js_lines.append(line)
    js_lines.append("        };")
    
    with open(JS_OUTPUT_PATH, 'w', encoding='utf-8') as f:
        f.write("\n".join(js_lines))
    print(f"Wrote {JS_OUTPUT_PATH}")

except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
