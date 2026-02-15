import json
import re
import math

# --- CONFIGURATION ---
INDEX_PATH = r"d:\history of id course\index.html"
OUTPUT_JS_PATH = r"d:\history of id course\gallery_meta.js"

# Movement Palette Keys (for consistency with index.html)
# mapped from movement names found in notes/html
MOVEMENT_MAP = {
    'arts_and_crafts': 'ac',
    'art_nouveau': 'an',
    'aesthetic': 'an',
    'modernism': 'modernism',
    'bauhaus': 'bh',
    'functionalism': 'sm',
    'rationalism': 'sm',
    'streamlining': 'ad',
    'midcentury': 'midcentury',
    'biomorphism': 'biomorphism',
    'minimalism': 'minimalism',
    'pop': 'mem',
    'memphis': 'mem',
    'postmodernism': 'pm',
    'high_tech': 'ht',
    'wedge': 'wedge'
}

def extract_designers():
    """Extracts designer keys and metadata from index.html GALLERY_DATA."""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the GALLERY_DATA object text
    match = re.search(r'const GALLERY_DATA = (\{.*?\});', content, re.DOTALL)
    if not match:
        print("Could not find GALLERY_DATA in index.html")
        return {}
    
    # Simple regex-based extraction of basic fields to avoid full JS parsing complexity
    designer_blobs = re.findall(r'"(\w+)":\s*\{(.*?)\s*\},', match.group(1), re.DOTALL)
    
    designers = {}
    for key, blob in designer_blobs:
        name_match = re.search(r'"name":\s*"(.*?)"', blob)
        birth_match = re.search(r'"birth":\s*"(.*?)"', blob)
        death_match = re.search(r'"death":\s*(null|"\d+")', blob)
        peak_match = re.search(r'"peakYear":\s*"(.*?)"', blob)
        
        death = death_match.group(1).replace('"', '') if death_match else None
        if death == 'null': death = None
        
        designers[key] = {
            "name": name_match.group(1) if name_match else "",
            "birth": int(birth_match.group(1)) if birth_match and birth_match.group(1).isdigit() else 1850,
            "death": int(death) if death and death.isdigit() else None,
            "peakYear": int(peak_match.group(1)) if peak_match and peak_match.group(1).isdigit() else None
        }
    return designers

def extract_movements():
    """Extracts movements from DESIGNER_MOVEMENTS in index.html."""
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    match = re.search(r'const DESIGNER_MOVEMENTS = (\{.*?\});', content, re.DOTALL)
    if not match:
        print("Could not find DESIGNER_MOVEMENTS in index.html")
        return {}
    
    # Extract 'key': ['move', 'move']
    move_lines = re.findall(r"'(\w+)':\s*\[(.*?)\]", match.group(1))
    
    movements = {}
    for key, moves_str in move_lines:
        moves = [m.strip().replace("'", "").replace('"', '') for m in moves_str.split(',') if m.strip()]
        movements[key] = moves
    return movements

def generate_productivity(start_year, end_year, peak_year):
    """Generates a bell-curve productivity dictionary."""
    if not peak_year:
        # Default peak to age 40 (mature career) instead of 20
        peak_year = start_year + 40
    
    # Career starts at age 22 (post-education), ends at death or age 75
    career_start = start_year + 22
    career_end = end_year if end_year else (start_year + 75)
    
    prod = {}
    # Use 3-year intervals for efficiency and smooth visual
    for y in range(career_start, career_end + 1, 3):
        # Gaussian distribution centered at peak_year
        # std_dev of 12 years for a tighter, more defined peak
        sigma = 12
        exponent = -0.5 * ((y - peak_year) / sigma) ** 2
        
        # Base multiplier 35, random noise could be added but smooth is better for graph
        value = math.exp(exponent) * 35 
        
        # Ramp-up constraint: Ensure very early years (22-25) aren't too high unless peak is there
        age = y - start_year
        if age < 25:
            value *= 0.3 # Slow start
        elif age < 30:
            value *= 0.7 # Building up
        
        if value > 1: # Only include non-zero productivity
            prod[str(y)] = {
                "count": round(value, 1),
                "movement": None # Will be filled later
            }
    return prod

def write_csv(meta_data, designers):
    """Writes the generated metadata to expanded_designers_v2.csv."""
    csv_path = r"d:\history of id course\expanded_designers_v2.csv"
    
    # Collect all possible year keys for columns
    all_years = set()
    for d_data in meta_data.values():
        all_years.update(d_data['productivity'].keys())
    sorted_years = sorted([int(y) for y in all_years])
    
    header = ["designer_key", "name", "birth", "death", "peak_year", "movements"] + [f"P_{y}" for y in sorted_years]
    
    rows = []
    rows.append(",".join(header))
    
    for key, data in meta_data.items():
        base = designers[key]
        movements = "|".join([m['name'] for m in data['movements']])
        
        row = [
            key,
            f'"{base["name"]}"',
            str(base["birth"]),
            str(base["death"]) if base["death"] else "",
            str(base["peakYear"]) if base["peakYear"] else "",
            movements
        ]
        
        # Add productivity values
        for y in sorted_years:
            val = data['productivity'].get(str(y), {}).get('count', 0)
            row.append(str(val))
            
        rows.append(",".join(row))
        
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(rows))
    print(f"Successfully wrote CSV to {csv_path}")

def main():
    designers = extract_designers()
    movements = extract_movements()
    
    meta_data = {}
    
    for key, info in designers.items():
        # 1. Base metadata
        peak = info['peakYear']
        prod = generate_productivity(info['birth'], info['death'], peak)
        
        # 2. Assign Movements
        designer_moves = movements.get(key, ['modernism'])
        
        # Sort productivity years
        years = sorted([int(y) for y in prod.keys()])
        if years:
            # Map movements across the career
            # If 1 movement: solid
            # If 2+: split them (first half, second half etc.)
            for i, y in enumerate(years):
                move_idx = min(len(designer_moves) - 1, int((i / len(years)) * len(designer_moves)))
                # Convert raw movement tag to display name for index.html mapping
                # We'll use the tag itself as the name, the CSS helper will handle the palette key
                prod[str(y)]['movement'] = designer_moves[move_idx]

        # 3. Format result
        meta_data[key] = {
            "movements": [{"name": m, "year": peak if i == 0 else peak + (i * 10)} for i, m in enumerate(designer_moves)],
            "productivity": prod
        }

    # Write to JS file
    js_content = f"const DESIGNER_META = {json.dumps(meta_data, indent=4)};"
    with open(OUTPUT_JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    
    # Write to CSV file (User Request)
    write_csv(meta_data, designers)
    
    print(f"Successfully generated exhaustive metadata for {len(meta_data)} designers.")

if __name__ == "__main__":
    main()
