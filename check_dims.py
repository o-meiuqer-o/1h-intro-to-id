"""Check dimensions of the largest files to understand the resize results."""
import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

IMAGES_DIR = Path(r"D:\history of id course\images")
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}

files = sorted(IMAGES_DIR.rglob('*'))
img_files = [f for f in files if f.is_file() and f.suffix.lower() in IMG_EXTS]

# Sort by file size descending
img_files.sort(key=lambda f: f.stat().st_size, reverse=True)

print(f"{'Size MB':>8}  {'Dimensions':>12}  {'Short':>5}  Path")
print("-" * 90)

for f in img_files[:30]:
    try:
        img = Image.open(f)
        w, h = img.size
        short = min(w, h)
        size_mb = f.stat().st_size / (1024*1024)
        rel = f.relative_to(IMAGES_DIR)
        print(f"{size_mb:>7.2f}  {w:>5} x {h:<5}  {short:>5}  {rel}")
    except:
        rel = f.relative_to(IMAGES_DIR)
        print(f"  ERROR  {'?':>12}  {'?':>5}  {rel}")
