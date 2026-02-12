
import sys
import shutil
import os

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"D:\history of id course"
SYNCED_MANIFEST = os.path.join(BASE_DIR, "gallery_manifest_synced.json")
MANIFEST = os.path.join(BASE_DIR, "gallery_manifest.json")
SYNCED_JS = os.path.join(BASE_DIR, "design_works_synced.js")
HTML_FILE = os.path.join(BASE_DIR, "index.html")

try:
    # 1. Update Manifest
    if os.path.exists(SYNCED_MANIFEST):
        shutil.copy2(SYNCED_MANIFEST, MANIFEST)
        print(f"Updated {MANIFEST}")
    else:
        print(f"Error: {SYNCED_MANIFEST} not found")
        sys.exit(1)

    # 2. Splice JS into Index.html
    if not os.path.exists(SYNCED_JS):
        print(f"Error: {SYNCED_JS} not found")
        sys.exit(1)

    with open(SYNCED_JS, encoding='utf-8') as f:
        new_works_block = f.read()

    with open(HTML_FILE, encoding='utf-8') as f:
        html_lines = f.read().split('\n')

    start_line = None
    end_line = None
    
    for i, line in enumerate(html_lines):
        if 'const DESIGN_WORKS' in line:
            start_line = i
        if start_line is not None and line.strip() == '};':
            end_line = i
            break
    
    if start_line is not None and end_line is not None:
        print(f"Found DESIGN_WORKS at lines {start_line+1}-{end_line+1}")
        new_html_lines = html_lines[:start_line] + [new_works_block] + html_lines[end_line+1:]
        with open(HTML_FILE, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_html_lines))
        print(f"Updated index.html with new DESIGN_WORKS content")
    else:
        print("Error: Could not find DESIGN_WORKS block boundaries in index.html")
        sys.exit(1)

except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
