
import csv
import json
import re
import os
import shutil

CSV_PATH = 'design_analysis.csv'
HTML_PATH = 'index.html'

def escape_js_string(s):
    if not s: return ''
    # Escape quotes and backslashes for JS single-quoted string
    return s.replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')

def regenerate():
    # 1. Read CSV
    print(f"Reading {CSV_PATH}...")
    design_works = {}
    # Use utf-8-sig to handle BOM
    with open(CSV_PATH, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        print(f"CSV Headers: {reader.fieldnames}")
        for row in reader:
            # Key logic: filename stem (without extension)
            # image_path = images/folder/filename.ext
            # key = filename (no ext)
            # Wait, index.html keys seem to be filename stems.
            # E.g. 'bel camaleonda_sofa' -> filename 'bellini_camaleonda_sofa.jpg'?
            # Let's check the CSV 'image_path'.
            
            # CSV Headers: key,designer,designer_key,movement,title,year,image,context,influence,analysis
            
            # Use 'key' from CSV if available and clean, else derive.
            # The previous verification script output showed 'key' exists.
            key = row['key']
            if not key:
                filename = os.path.basename(row['image'])
                key = os.path.splitext(filename)[0]
            
            design_works[key] = {
                'title': row['title'],
                'image': row['image'],
                'context': row['context'],
                'influence': row['influence'],
                'analysis': row['analysis']
            }

    print(f"Loaded {len(design_works)} entries.")
    
    # 2. Generate JS Block
    js_lines = ["        const DESIGN_WORKS = {"]
    for key, data in design_works.items():
        # strict JSON-like structure but with JS keys
        line = f"            '{key}': {{ "
        if 'camaleonda' in key:
            print(f"DEBUG CAMALEONDA KEY: {repr(key)}")
            print(f"DEBUG CAMALEONDA LINE START: {repr(line)}")
        line += f"title: '{escape_js_string(data['title'])}', "
        line += f"image: '{data['image']}', "
        line += f"context: '{escape_js_string(data['context'])}', "
        line += f"influence: '{escape_js_string(data['influence'])}', "
        line += f"analysis: '{escape_js_string(data['analysis'])}' "
        line += "},"
        js_lines.append(line)
    js_lines.append("        };")
    
    new_js_block = "\n".join(js_lines)
    
    # 3. Read HTML
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Backup
    shutil.copy(HTML_PATH, HTML_PATH + '.bak')
    print("Backup created.")
    
    # 4. Replace Block
    # Look for Start: `const DESIGN_WORKS = {`
    # Look for End: `};` before `/* ── MOVEMENT COLOR SYSTEM ── */` or `const MOVEMENT_PALETTE`
    
    # Pattern: `const DESIGN_WORKS = \{[\s\S]*?\};`
    # But be careful not to match too much.
    # The next variable is likely `const MOVEMENT_PALETTE`.
    
    pattern = re.compile(r"const DESIGN_WORKS = \{[\s\S]*?\};", re.MULTILINE)
    
    match = pattern.search(content)
    if not match:
        print("Could not find DESIGN_WORKS block.")
        # Try finding by context
        start_marker = "const DESIGN_WORKS = {"
        end_marker = "const MOVEMENT_PALETTE ="
        s_idx = content.find(start_marker)
        e_idx = content.find(end_marker)
        if s_idx != -1 and e_idx != -1:
             # Find the last `};` before e_idx
             sub = content[s_idx:e_idx]
             last_brace = sub.rfind("};")
             if last_brace != -1:
                 # Replace manually
                 new_content = content[:s_idx] + new_js_block + "\n\n        " + content[s_idx + last_brace + 2:]
                 with open(HTML_PATH, 'w', encoding='utf-8') as f:
                     f.write(new_content)
                 print("Replaced successfully (manual slice).")
                 return
        print("Failed to replace.")
        return

    print("Found block via regex.")
    # Use lambda to avoid interpreting backslashes in new_js_block
    new_content = pattern.sub(lambda m: new_js_block, content, count=1)
    
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Replaced successfully (regex with lambda).")

if __name__ == '__main__':
    regenerate()
