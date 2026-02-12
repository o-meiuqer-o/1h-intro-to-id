"""
Compress and optimize all images in the images/ directory.
- Images already have short dim <= 800px (web resolution)
- Re-encode large files to quality=85 for significant savings
- PNG -> JPG conversion
- Videos/PDFs/OGG/SVG/GIF are skipped
"""

import sys
from pathlib import Path
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

SIZE_THRESHOLD = 500 * 1024  # 500KB - compress anything larger
SKIP_EXTS = {'.webm', '.ogv', '.ogg', '.pdf', '.svg', '.gif'}
IMG_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
IMAGES_DIR = Path(r"D:\history of id course\images")

stats = {'compressed': 0, 'converted': 0, 'skipped': 0, 'small_ok': 0, 'errors': 0}
saved_bytes = 0

def process_image(filepath):
    global saved_bytes
    ext = filepath.suffix.lower()

    if ext in SKIP_EXTS:
        stats['skipped'] += 1
        return
    if ext not in IMG_EXTS:
        stats['skipped'] += 1
        return

    try:
        original_size = filepath.stat().st_size
        img = Image.open(filepath)

        # Convert to RGB for JPEG
        if img.mode in ('RGBA', 'P', 'LA'):
            img = img.convert('RGB')
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        w, h = img.size

        # PNG -> JPG conversion (always)
        if ext == '.png':
            new_path = filepath.with_suffix('.jpg')
            img.save(new_path, 'JPEG', quality=85, optimize=True)
            filepath.unlink()
            new_size = new_path.stat().st_size
            saved = original_size - new_size
            saved_bytes += saved
            stats['converted'] += 1
            rel = new_path.relative_to(IMAGES_DIR)
            print(f"  PNG->JPG {rel} ({original_size//1024}KB -> {new_size//1024}KB, saved {saved//1024}KB)")
            return

        # Compress large files
        if original_size > SIZE_THRESHOLD:
            if ext == '.webp':
                img.save(filepath, 'WEBP', quality=85)
            else:
                img.save(filepath, 'JPEG', quality=85, optimize=True)
            new_size = filepath.stat().st_size
            saved = original_size - new_size
            saved_bytes += saved
            stats['compressed'] += 1
            rel = filepath.relative_to(IMAGES_DIR)
            print(f"  COMPRESS {rel} ({original_size//1024}KB -> {new_size//1024}KB, saved {saved//1024}KB)")
        else:
            stats['small_ok'] += 1

    except Exception as e:
        stats['errors'] += 1
        print(f"  ERROR {filepath.name}: {e}")


def main():
    print(f"Scanning {IMAGES_DIR} ...")
    files = sorted(f for f in IMAGES_DIR.rglob('*') if f.is_file())
    print(f"Found {len(files)} files\n")

    for f in files:
        process_image(f)

    print(f"\n{'='*50}")
    print(f"RESULTS:")
    print(f"  Compressed:    {stats['compressed']}")
    print(f"  PNG->JPG:      {stats['converted']}")
    print(f"  Already OK:    {stats['small_ok']} (<500KB)")
    print(f"  Skipped:       {stats['skipped']} (non-image)")
    print(f"  Errors:        {stats['errors']}")
    print(f"  Space saved:   {saved_bytes / (1024*1024):.1f} MB")


if __name__ == '__main__':
    main()
