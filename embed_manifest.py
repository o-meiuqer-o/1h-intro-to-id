
import json
import os

HTML_PATH = r"d:\history of id course\index.html"
MANIFEST_PATH = r"d:\history of id course\gallery_manifest.json"

# 1. Read Manifest
with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
    manifest_data = json.load(f)

# Convert to JS string
json_str = json.dumps(manifest_data, indent=4)
js_const = f"const GALLERY_DATA = {json_str};\n"

# 2. Read HTML
with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html_content = f.read()

# 3. Modify HTML
# Find loadGallery start
target = "async function loadGallery() {"
if target not in html_content:
    print("Error: loadGallery function not found in index.html")
    exit(1)

# We will inject the data BEFORE the function
# And modify the function to use it.

# New function logic
new_function_start = f"""
{js_const}
        async function loadGallery() {{
            try {{
                // const response = await fetch('gallery_manifest.json');
                // const data = await response.json();
                const data = GALLERY_DATA;
"""

# Replace the specific lines
# We need to be careful about what we replace.
# The original code:
# async function loadGallery() {
#     try {
#         const response = await fetch('gallery_manifest.json');
#         const data = await response.json();

# We can replace this block.
parts = html_content.split(target)
if len(parts) != 2:
    print("Error: Multiple or zero occurrences of loadGallery")
    exit(1)

pre_code = parts[0]
post_code = parts[1]

# In post_code, find the lines to replace
# We want to replace lines up to "const data = await response.json();"
# Let's use string replacement on a chunk of the post_code
chunk_to_replace = """
            try {
                const response = await fetch('gallery_manifest.json');
                const data = await response.json();
"""
# Note: Indentation might vary. Let's be deeper.
# Actually, strict replacement of the function signature + first few lines is safest.

# Let's locate the `const data = await response.json();` line index
lines = html_content.splitlines()
start_idx = -1
for i, line in enumerate(lines):
    if "async function loadGallery() {" in line:
        start_idx = i
        break

if start_idx == -1:
    print("Error: Function not found")
    exit(1)

# We want to insert the constant BEFORE start_idx
# And modify lines inside.

new_lines = []
# Keep lines before
new_lines.extend(lines[:start_idx])

# Insert Constant
new_lines.append(f"        {js_const}")

# Start Function
new_lines.append("        async function loadGallery() {")
new_lines.append("            try {")
new_lines.append("                // Local data for file:// access")
new_lines.append("                const data = GALLERY_DATA;")

# Skip the original lines
# We need to skip `try {`, `fetch`, `response.json`.
# Let's confirm exact lines in file
# 2867: async function loadGallery() {
# 2868:     try {
# 2869:         const response = await fetch('gallery_manifest.json');
# 2870:         const data = await response.json();

# So we skip 4 lines from start_idx (2867 -> 2870 inclusive? No, 2867 is kept/replaced. 2868 is kept/replaced.)
# Actually, I'm rewriting 2867-2870.
# So I should skip lines[start_idx] to lines[start_idx+3].
# Let's verify content of these lines to be safe.

check_lines = lines[start_idx:start_idx+4]
print("Lines to replace:")
for l in check_lines: print(l)

# If they match expectation, we good.
# Expect:
# async function loadGallery() {
#     try {
#         const response = await fetch('gallery_manifest.json');
#         const data = await response.json();

# My script logic:
# write new lines.
# append lines[start_idx+4:]

new_lines.extend(lines[start_idx+4:])

final_html = "\n".join(new_lines)

with open(HTML_PATH, 'w', encoding='utf-8') as f:
    f.write(final_html)

print("Successfully embedded manifest into index.html")
