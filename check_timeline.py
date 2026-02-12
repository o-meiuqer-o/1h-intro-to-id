
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

MANIFEST_PATH = r"d:\history of id course\gallery_manifest.json"
HTML_PATH = r"d:\history of id course\index.html"

# 1. Load Manifest
with open(MANIFEST_PATH, encoding='utf-8') as f:
    manifest = json.load(f)

full_list = sorted(manifest.keys())
print(f"Total Designers in Manifest: {len(full_list)}")
print(f"Manifest Keys: {full_list}\n")

# 2. Analyze HTML
with open(HTML_PATH, encoding='utf-8') as f:
    html = f.read()

# Find existing modal triggers/bubbles
# Typical pattern: onclick="openFullModal('morris')"
triggers = re.findall(r"openFullModal\('([^']+)'\)", html)
unique_triggers = sorted(list(set(triggers)))

print(f"Designers currently on Timeline: {len(unique_triggers)}")
print(f"Timeline Keys: {unique_triggers}\n")

# 3. Identify Missing
missing = [d for d in full_list if d not in unique_triggers]
print(f"Missing from Timeline: {len(missing)}")
print(f"Missing Keys: {missing}\n")

# 4. Analyze Existing Timeline Structure
# We need to know where to insert bubbles. Let's find "Phase" headers and existing bubbles nearby.
phases = re.findall(r"(Phase \d: [^<]+)", html)
print(f"Timeline Phases Found: {phases}")

# Suggest insertion points based on peakYear/movement from manifest
# Create a mapping of key -> suggested_phase
timeline_suggestions = []

for key in missing:
    data = manifest[key]
    year = data.get('peakYear')
    movement = 'Unknown' 
    # Try to infer movement from Design Works if possible, verify later
    
    # Simple year-based phase logic
    # Phase 1: Roots (Pre-1900)
    # Phase 2: Evolution (1900-1945)
    # Phase 3: Post-War / Modern (1945-1980)
    # Phase 4: Contemporary (1980+)
    
    phase = "Unknown"
    y = int(year) if year and year.isdigit() else 1900
    
    if y < 1900: phase = "Phase 1: Roots"
    elif y < 1945: phase = "Phase 2: Evolution"
    elif y < 1980: phase = "Phase 3: Post-War"
    else: phase = "Phase 4: Contemporary"
    
    timeline_suggestions.append(f"{key} ({year}) -> {phase}")

print("\nSuggestions:")
for s in timeline_suggestions:
    print(s)
