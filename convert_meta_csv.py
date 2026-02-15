import csv
import json

csv_path = r"d:\history of id course\expanded_designers_v2.csv"
js_output_path = r"d:\history of id course\gallery_meta.js"

def parse_movements(mv_str):
    # Format: "Art Nouveau:1895|Modernism:1907"
    if not mv_str or mv_str.strip() == "":
        return []
    
    moves = []
    parts = mv_str.split('|')
    for p in parts:
        if ':' in p:
            name, year = p.split(':')
            moves.append({"name": name.strip(), "year": int(year.strip())})
        else:
            # Fallback if no year
            moves.append({"name": p.strip(), "year": 0})
    return moves

def convert_csv():
    meta_data = {}
    
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                folder_key = row.get('Folder', '').lower().strip()
                if not folder_key:
                    continue
                
                # Movements
                movements = parse_movements(row.get('Movements', ''))
                
                # Productivity
                # Columns P_1830 to P_2024
                # New Format: "Count:Movement" (e.g., "5:Art Nouveau") or just "Count" (e.g. "5")
                prod_data = {}
                for k, v in row.items():
                    if k and k.startswith('P_'):
                        year = k.replace('P_', '')
                        try:
                            val_str = v.strip()
                            if not val_str: continue

                            # Parse "5:Art Nouveau"
                            parts = val_str.split(':')
                            count = int(parts[0])
                            
                            movement = None
                            if len(parts) > 1:
                                movement = parts[1].strip()

                            if count > 0:
                                prod_data[year] = { 
                                    "count": count, 
                                    "movement": movement 
                                }
                        except:
                            pass
                
                meta_data[folder_key] = {
                    "movements": movements,
                    "productivity": prod_data
                }
                
        js_content = f"const DESIGNER_META = {json.dumps(meta_data, indent=4)};"
        
        with open(js_output_path, 'w', encoding='utf-8') as out:
            out.write(js_content)
            
        print(f"Successfully generated {js_output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    convert_csv()
