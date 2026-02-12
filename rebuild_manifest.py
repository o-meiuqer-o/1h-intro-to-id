"""
Rebuild gallery_manifest.json from actual image files to ensure consistency.
"""
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

IMAGES_DIR = Path(r"D:\history of id course\images")
BASE_DIR = Path(r"D:\history of id course")
MANIFEST_FILE = Path(r"D:\history of id course\gallery_manifest.json")
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
SKIP_DIRS = {'_archive', '_extras', 'pininfarina'}

# Load existing manifest for bio/philosophy/integration data
existing = {}
if MANIFEST_FILE.exists():
    try:
        existing = json.loads(MANIFEST_FILE.read_text(encoding='utf-8'))
    except:
        pass

# Designer metadata
DESIGNER_META = {
    'aalto': {'name': 'Alvar Aalto', 'birth': '1898', 'death': '1976', 'peakYear': '1932'},
    'behrens': {'name': 'Peter Behrens', 'birth': '1868', 'death': '1940', 'peakYear': '1907'},
    'bellini': {'name': 'Mario Bellini', 'birth': '1935', 'death': None, 'peakYear': '1972'},
    'bill': {'name': 'Max Bill', 'birth': '1908', 'death': '1994', 'peakYear': '1952'},
    'brandt': {'name': 'Marianne Brandt', 'birth': '1893', 'death': '1983', 'peakYear': '1926'},
    'breuer': {'name': 'Marcel Breuer', 'birth': '1902', 'death': '1981', 'peakYear': '1925'},
    'castiglioni': {'name': 'Achille Castiglioni', 'birth': '1918', 'death': '2002', 'peakYear': '1962'},
    'dresser': {'name': 'Christopher Dresser', 'birth': '1834', 'death': '1904', 'peakYear': '1860'},
    'dreyfuss': {'name': 'Henry Dreyfuss', 'birth': '1904', 'death': '1972', 'peakYear': '1937'},
    'dyson': {'name': 'James Dyson', 'birth': '1947', 'death': None, 'peakYear': '1993'},
    'eames': {'name': 'Charles & Ray Eames', 'birth': '1907', 'death': '1988', 'peakYear': '1946'},
    'earl': {'name': 'Harley Earl', 'birth': '1893', 'death': '1969', 'peakYear': '1938'},
    'fukasawa': {'name': 'Naoto Fukasawa', 'birth': '1956', 'death': None, 'peakYear': '2003'},
    'gandini': {'name': 'Marcello Gandini', 'birth': '1938', 'death': '2024', 'peakYear': '1971'},
    'geddes': {'name': 'Norman Bel Geddes', 'birth': '1893', 'death': '1958', 'peakYear': '1935'},
    'giugiaro': {'name': 'Giorgetto Giugiaro', 'birth': '1938', 'death': None, 'peakYear': '1974'},
    'gropius': {'name': 'Walter Gropius', 'birth': '1883', 'death': '1969', 'peakYear': '1919'},
    'guimard': {'name': 'Hector Guimard', 'birth': '1867', 'death': '1942', 'peakYear': '1900'},
    'ive': {'name': 'Jony Ive', 'birth': '1967', 'death': None, 'peakYear': '2001'},
    'jacobsen': {'name': 'Arne Jacobsen', 'birth': '1902', 'death': '1971', 'peakYear': '1952'},
    'lihotzky': {'name': 'Margarete Schutte-Lihotzky', 'birth': '1897', 'death': '2000', 'peakYear': '1926'},
    'loewy': {'name': 'Raymond Loewy', 'birth': '1893', 'death': '1986', 'peakYear': '1940'},
    'morris': {'name': 'William Morris', 'birth': '1834', 'death': '1896', 'peakYear': '1862'},
    'nelson': {'name': 'George Nelson', 'birth': '1908', 'death': '1986', 'peakYear': '1952'},
    'newson': {'name': 'Marc Newson', 'birth': '1963', 'death': None, 'peakYear': '1995'},
    'nizzoli': {'name': 'Marcello Nizzoli', 'birth': '1887', 'death': '1969', 'peakYear': '1948'},
    'ponti': {'name': 'Gio Ponti', 'birth': '1891', 'death': '1979', 'peakYear': '1957'},
    'rams': {'name': 'Dieter Rams', 'birth': '1932', 'death': None, 'peakYear': '1961'},
    'rashid': {'name': 'Karim Rashid', 'birth': '1960', 'death': None, 'peakYear': '2002'},
    'sapper': {'name': 'Richard Sapper', 'birth': '1932', 'death': '2015', 'peakYear': '1972'},
    'sottsass': {'name': 'Ettore Sottsass', 'birth': '1917', 'death': '2007', 'peakYear': '1981'},
    'starck': {'name': 'Philippe Starck', 'birth': '1949', 'death': None, 'peakYear': '1990'},
    'wagenfeld': {'name': 'Wilhelm Wagenfeld', 'birth': '1900', 'death': '1990', 'peakYear': '1924'},
}

manifest = {}
for d in sorted(IMAGES_DIR.iterdir()):
    if not d.is_dir() or d.name in SKIP_DIRS or d.name.startswith('_'):
        continue
    
    key = d.name
    meta = DESIGNER_META.get(key, {'name': key.capitalize(), 'birth': None, 'death': None, 'peakYear': None})
    
    # Get images
    images = []
    for f in sorted(d.rglob('*')):
        if f.is_file() and f.suffix.lower() not in SKIP_EXTS:
            rel = str(f.relative_to(BASE_DIR)).replace('\\', '/')
            images.append(rel)
    
    if not images:
        continue
    
    entry = {
        'name': meta['name'],
        'birth': meta['birth'],
        'death': meta['death'],
        'peakYear': meta['peakYear'],
        'images': images,
    }
    
    # Preserve existing bio/philosophy/integration
    if key in existing:
        for field in ['bio', 'philosophy', 'integration']:
            if field in existing[key]:
                entry[field] = existing[key][field]
    
    manifest[key] = entry

# Write manifest
MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
print(f"Manifest updated with {len(manifest)} designers")
for k, v in sorted(manifest.items()):
    print(f"  {k}: {len(v['images'])} images")
