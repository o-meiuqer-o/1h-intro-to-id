import re
import csv
import os

# Path to index.html
html_path = r"d:\history of id course\index.html"
output_csv = r"d:\history of id course\image_metadata.csv"

# Regex to find GALLERY_DATA object
# We look for the Start of GALLERY_DATA and then rudimentary parsing
# simpler: just regex for "images/.*\.(jpg|jpeg|png|webp)" inside the file
# but we want to know WHICH designer they belong to.

def extract_images():
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the GALLERY_DATA section (hacky but effective for this file)
    start_marker = "const GALLERY_DATA = {"
    end_marker = "window.onload" # or some other marker, or just parse the block
    
    # Let's simple regex for entries
    # "designer_key": { ... "images": [ ... ] }
    
    # Regex to find designer blocks
    # key: value
    # key is "name"
    
    image_entries = []
    
    # Split by designer keys roughly
    # We'll use a specific regex to capture lines with "images/..."
    # and infer designer from context if possible, or just dump them all
    
    # Better approach: Iterate lines, track current designer
    current_designer = "unknown"
    
    lines = content.split('\n')
    in_gallery = False
    
    for line in lines:
        if "const GALLERY_DATA = {" in line:
            in_gallery = True
            
        if not in_gallery:
            continue
            
        if "};" in line and not "images" in line: # End of gallery object roughly
            in_gallery = False
            
        # Detect designer key "aalto": {
        key_match = re.search(r'"(\w+)":\s*{', line)
        if key_match:
            current_designer = key_match.group(1)
            
        # Detect image
        # "images/aalto/aalto_1956_2_.jpg",
        img_match = re.search(r'"(images/.*?)"', line)
        if img_match:
            img_path = img_match.group(1)
            filename = os.path.basename(img_path)
            
            # Smart Guessing Year from filename (many have years like 1956)
            year_match = re.search(r'(18|19|20)\d{2}', filename)
            year = year_match.group(0) if year_match else ""
            
            image_entries.append({
                "Designer": current_designer,
                "RelativePath": img_path,
                "Filename": filename,
                "Year": year
            })

    # Write to CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Designer', 'RelativePath', 'Filename', 'Year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for entry in image_entries:
            writer.writerow(entry)
            
    print(f"Extracted {len(image_entries)} images to {output_csv}")

if __name__ == "__main__":
    extract_images()
