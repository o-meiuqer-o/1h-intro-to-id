"""Check DESIGN_WORKS image paths and find which need updating."""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

html = Path(r"D:\history of id course\index.html").read_text(encoding='utf-8')

# Find all image references in DESIGN_WORKS
matches = re.findall(r"image:\s*'([^']+)'", html)
print(f"DESIGN_WORKS image refs: {len(matches)}")

base = Path(r"D:\history of id course")
broken = []
working = []
for m in sorted(set(matches)):
    p = base / m
    if p.exists():
        working.append(m)
    else:
        broken.append(m)
        print(f"  BROKEN: {m}")

print(f"\nWorking: {len(working)}, Broken: {len(broken)}")
