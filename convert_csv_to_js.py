import csv
import json

csv_file_path = r"d:\history of id course\design_analysis.csv"
js_output_path = r"d:\history of id course\design_works_data.js"

design_works = {}

try:
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # key: work_id (from CSV)
            # value: { title, context, influence, analysis, image }
            work_id = row.get('key', '').strip()
            if not work_id:
                # Fallback if key is missing, use title
                work_id = row.get('title', '').lower().replace(' ', '_')
            
            design_works[work_id] = {
                "title": row.get('title', ''),
                "context": row.get('context', ''),
                "influence": row.get('influence', ''),
                "analysis": row.get('analysis', ''),
                "image": row.get('image_path', '')
            }

    js_content = f"const DESIGN_WORKS = {json.dumps(design_works, indent=4)};"
    
    with open(js_output_path, mode='w', encoding='utf-8') as jsfile:
        jsfile.write(js_content)
    
    print(f"Successfully created {js_output_path}")

except Exception as e:
    print(f"Error: {e}")
