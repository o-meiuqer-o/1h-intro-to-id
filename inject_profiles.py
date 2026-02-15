
import csv
import re
import json

CSV_PATH = r"d:\history of id course\expanded_designers_v2.csv"
INDEX_PATH = r"d:\history of id course\index.html"

def inject_profiles():
    # 1. Read CSV Data
    profiles = {}
    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row.get('designer_key') or row.get('Folder') or row.get('rank')
                if not key: continue

                profiles[key.lower()] = {
                    "bio": row.get('Bio', ''),
                    "philosophy": row.get('Philosophy', ''),
                    "integration": row.get('Integration', '')
                }
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print(f"Loaded {len(profiles)} profiles from CSV.")

    # 2. Read Index.html
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    updated_content = content
    
    for key, data in profiles.items():
        if not data['bio']: continue

        print(f"Injecting data for {key}...")
        
        # Robust Strategy: Match from Field Key to Next Field Key
        # "bio": "..."  , "philosophy"
        # "philosophy": "..." , "integration"
        # "integration": "..." , "images"
        
        def replace_block(text, current_key, next_key_start, new_value):
            # Escape quotes for JSON
            safe_value = new_value.replace('"', '\\"').replace('\n', ' ')
            
            # Pattern: 
            # 1. The designer block:  "key": { ...
            # 2. Inside that, the current field: "current_key":
            # 3. Any content (lazy) until
            # 4. The lookahead for the next key or end of fields
            
            # Actually, let's just find the designer block first to narrow scope
            block_pattern = r'("' + re.escape(key) + r'":\s*\{)'
            block_match = re.search(block_pattern, text)
            if not block_match:
                print(f"Warning: Key {key} not found")
                return text
                
            block_start = block_match.start()
            
            # Construct a regex that anchors to the specific field within this block
            # We want to replace everything between `"field":` and `,` (before next field)
            # OR `,` before ` "next_field"`
            
            # Regex:
            # ("field":\s*)([\s\S]*?)(\,\s*")next_field"
            # We capture the prefix ("field": ), the content to replace, and the suffix (comma + next field quote)
            
            # Important: We must match the *first* occurrence after the block start
            
            regex = re.compile(
                r'("' + current_key + r'":\s*)([\s\S]*?)(\,\s*"' + next_key_start + r'")'
            )
            
            # We need to search *starting from* block_start. 
            # Sub doesn't support start pos directly, so we search and splice.
            match = regex.search(text, pos=block_start)
            if not match:
                # Fallback: maybe it's the last field (integration) and followed by "images"
                if current_key == 'integration':
                     regex = re.compile(r'("' + current_key + r'":\s*)([\s\S]*?)(\,\s*"images")')
                     match = regex.search(text, pos=block_start)
                
                if not match:
                    print(f"  Field {current_key} structure mismatch for {key}")
                    return text
            
            # Valid match found. Reconstruct the string.
            # Group 1: "bio": 
            # Group 2: OLD_VALUE (potentially corrupted)
            # Group 3: , "philosophy"
            
            new_segment = match.group(1) + '"' + safe_value + '"' + match.group(3)
            
            # Replace using string slicing to ensure we only touch this instance
            return text[:match.start()] + new_segment + text[match.end():]

        # Apply updates in order
        updated_content = replace_block(updated_content, "bio", "philosophy", data['bio'])
        updated_content = replace_block(updated_content, "philosophy", "integration", data['philosophy'])
        updated_content = replace_block(updated_content, "integration", "images", data['integration'])

    # 4. Write back
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("Index.html repaired and updated.")

if __name__ == "__main__":
    inject_profiles()
