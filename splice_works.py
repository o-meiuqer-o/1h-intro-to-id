"""Replace DESIGN_WORKS block in index.html with new version."""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

HTML_FILE = Path(r"D:\history of id course\index.html")
NEW_WORKS = Path(r"D:\history of id course\design_works_new.js")

html_lines = HTML_FILE.read_text(encoding='utf-8').split('\n')
new_works = NEW_WORKS.read_text(encoding='utf-8')

# Find start and end of DESIGN_WORKS block
start_line = None
end_line = None
for i, line in enumerate(html_lines):
    if 'const DESIGN_WORKS' in line:
        start_line = i
    if start_line is not None and line.strip() == '};':
        end_line = i
        break

if start_line is None or end_line is None:
    print("ERROR: Could not find DESIGN_WORKS boundaries")
    sys.exit(1)

print(f"Found DESIGN_WORKS at lines {start_line+1}-{end_line+1}")
print(f"Old block: {end_line - start_line + 1} lines")

# Replace
new_html_lines = html_lines[:start_line] + [new_works] + html_lines[end_line+1:]
new_html = '\n'.join(new_html_lines)

HTML_FILE.write_text(new_html, encoding='utf-8')
print(f"Replaced successfully. New file has {len(new_html_lines)} lines")
