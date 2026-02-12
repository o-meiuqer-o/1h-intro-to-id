"""
Generate a complete DESIGN_WORKS JavaScript object from all actual image files.
For each image, infer the work title from filename, assign the designer and movement,
and produce placeholder analysis text that we'll fill in properly.
"""
import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

IMAGES_DIR = Path(r"D:\history of id course\images")
BASE_DIR = Path(r"D:\history of id course")
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
SKIP_DIRS = {'_archive', '_extras', 'pininfarina'}

# Designer info map
DESIGNER_INFO = {
    'aalto': {'name': 'Alvar Aalto', 'movement': 'Modernism / Biomorphism'},
    'behrens': {'name': 'Peter Behrens', 'movement': 'Modernism / Deutscher Werkbund'},
    'bellini': {'name': 'Mario Bellini', 'movement': 'Italian Rationalism'},
    'bill': {'name': 'Max Bill', 'movement': 'Bauhaus / Ulm School'},
    'brandt': {'name': 'Marianne Brandt', 'movement': 'Bauhaus'},
    'breuer': {'name': 'Marcel Breuer', 'movement': 'Bauhaus / Modernism'},
    'castiglioni': {'name': 'Achille Castiglioni', 'movement': 'Italian Rationalism'},
    'dresser': {'name': 'Christopher Dresser', 'movement': 'Arts & Crafts / Aesthetic Movement'},
    'dreyfuss': {'name': 'Henry Dreyfuss', 'movement': 'Streamlining / Functionalism'},
    'dyson': {'name': 'James Dyson', 'movement': 'Minimalism / Engineering'},
    'eames': {'name': 'Charles & Ray Eames', 'movement': 'Mid-Century Modern'},
    'earl': {'name': 'Harley Earl', 'movement': 'Streamlining'},
    'fukasawa': {'name': 'Naoto Fukasawa', 'movement': 'Minimalism'},
    'gandini': {'name': 'Marcello Gandini', 'movement': 'Wedge Era'},
    'geddes': {'name': 'Norman Bel Geddes', 'movement': 'Streamlining'},
    'giugiaro': {'name': 'Giorgetto Giugiaro', 'movement': 'Wedge Era'},
    'gropius': {'name': 'Walter Gropius', 'movement': 'Bauhaus / Modernism'},
    'guimard': {'name': 'Hector Guimard', 'movement': 'Art Nouveau'},
    'ive': {'name': 'Jony Ive', 'movement': 'Minimalism'},
    'jacobsen': {'name': 'Arne Jacobsen', 'movement': 'Mid-Century Modern'},
    'lihotzky': {'name': 'Margarete Schutte-Lihotzky', 'movement': 'Functionalism / Bauhaus'},
    'loewy': {'name': 'Raymond Loewy', 'movement': 'Streamlining'},
    'morris': {'name': 'William Morris', 'movement': 'Arts & Crafts'},
    'nelson': {'name': 'George Nelson', 'movement': 'Mid-Century Modern'},
    'newson': {'name': 'Marc Newson', 'movement': 'Biomorphism'},
    'nizzoli': {'name': 'Marcello Nizzoli', 'movement': 'Italian Rationalism'},
    'ponti': {'name': 'Gio Ponti', 'movement': 'Italian Rationalism'},
    'rams': {'name': 'Dieter Rams', 'movement': 'Ulm School / Minimalism'},
    'rashid': {'name': 'Karim Rashid', 'movement': 'Postmodernism'},
    'sapper': {'name': 'Richard Sapper', 'movement': 'Italian Rationalism'},
    'sottsass': {'name': 'Ettore Sottsass', 'movement': 'Postmodernism / Memphis'},
    'starck': {'name': 'Philippe Starck', 'movement': 'Postmodernism'},
    'wagenfeld': {'name': 'Wilhelm Wagenfeld', 'movement': 'Bauhaus'},
}

def filename_to_title(filename, designer_key):
    """Convert a filename to a readable work title."""
    stem = Path(filename).stem
    # Remove designer prefix variations
    name_parts = DESIGNER_INFO.get(designer_key, {}).get('name', '').split()
    first_name_prefix = name_parts[0].lower() + '_' if name_parts else ''
    prefixes = [designer_key + '_', designer_key.upper() + '_', 'christopher_dresser_', 
                'Christopher_', 'christopher_']
    if first_name_prefix:
        prefixes.append(first_name_prefix)
    for p in prefixes:
        if stem.lower().startswith(p.lower()):
            stem = stem[len(p):]
    
    # Clean up filename
    stem = stem.replace('_', ' ').replace('%2C', ',').replace('%27', "'").replace('%28', '(').replace('%29', ')').replace('%C3%BC', 'u').replace('%C3%B6', 'o').replace('%C3%A4', 'a')
    
    # Remove trailing numbers/dimensions
    stem = re.sub(r'\s+\d{3,4}$', '', stem)
    stem = re.sub(r'\s+\(\d+\)$', '', stem)
    
    # Capitalize words
    words = stem.split()
    title = ' '.join(w.capitalize() if len(w) > 2 else w for w in words)
    
    if not title or title.strip() == '':
        title = designer_key.capitalize() + ' Work'
    
    return title.strip()

def make_work_key(designer_key, filename):
    """Generate a unique key for DESIGN_WORKS."""
    stem = Path(filename).stem.lower()
    stem = re.sub(r'[^a-z0-9_]', '_', stem)
    stem = re.sub(r'_+', '_', stem).strip('_')
    # Truncate to reasonable length
    if len(stem) > 50:
        stem = stem[:50]
    return stem

# Build the new DESIGN_WORKS data
works = {}
for d in sorted(IMAGES_DIR.iterdir()):
    if not d.is_dir() or d.name in SKIP_DIRS or d.name.startswith('_'):
        continue
    
    designer_key = d.name
    info = DESIGNER_INFO.get(designer_key, {'name': designer_key.capitalize(), 'movement': 'Unknown'})
    
    for f in sorted(d.rglob('*')):
        if not f.is_file() or f.suffix.lower() in SKIP_EXTS:
            continue
        
        rel_path = str(f.relative_to(BASE_DIR)).replace('\\', '/')
        title = filename_to_title(f.name, designer_key)
        work_key = make_work_key(designer_key, f.name)
        
        # Determine if it's a portrait
        is_portrait = 'portrait' in f.name.lower() or 'photo' in f.name.lower()
        
        works[work_key] = {
            'title': title,
            'image': rel_path,
            'designer': info['name'],
            'movement': info['movement'],
            'is_portrait': is_portrait,
            'context': f"Work by {info['name']} from the {info['movement']} movement.",
            'influence': f"Part of {info['name']}'s contribution to {info['movement']}.",
            'analysis': f"A work demonstrating the principles of {info['movement']}."
        }

# Also handle root-level images
for f in sorted(IMAGES_DIR.iterdir()):
    if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
        rel_path = str(f.relative_to(BASE_DIR)).replace('\\', '/')
        stem = f.stem.lower()
        work_key = re.sub(r'[^a-z0-9_]', '_', stem)
        works[work_key] = {
            'title': filename_to_title(f.name, ''),
            'image': rel_path,
            'designer': 'Historical',
            'movement': 'Historical',
            'is_portrait': False,
            'context': 'Historical reference image.',
            'influence': 'Historical context.',
            'analysis': 'Historical reference.'
        }

# Generate JS output
js_lines = []
js_lines.append("        const DESIGN_WORKS = {")
for key, data in works.items():
    title = data['title'].replace("'", "\\'")
    image = data['image'].replace("'", "\\'")
    context = data['context'].replace("'", "\\'")
    influence = data['influence'].replace("'", "\\'")
    analysis = data['analysis'].replace("'", "\\'")
    js_lines.append(f"            '{key}': {{ title: '{title}', image: '{image}', context: '{context}', influence: '{influence}', analysis: '{analysis}' }},")
js_lines.append("        };")

# Write JS snippet
js_out = Path(r"D:\history of id course\design_works_new.js")
js_out.write_text('\n'.join(js_lines), encoding='utf-8')
print(f"Generated {len(works)} DESIGN_WORKS entries")
print(f"JS snippet saved to {js_out}")

# Also save as JSON for analysis phase
json_out = Path(r"D:\history of id course\design_works_data.json")
json_out.write_text(json.dumps(works, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"JSON data saved to {json_out}")

# Print summary per designer
print(f"\n=== SUMMARY ===")
from collections import Counter
designer_counts = Counter()
for data in works.values():
    designer_counts[data['designer']] += 1
for designer, count in sorted(designer_counts.items()):
    print(f"  {designer}: {count} works")
