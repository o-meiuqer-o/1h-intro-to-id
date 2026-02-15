import csv
import re
import os

CSV_FILE = r'd:\history of id course\movements.csv'
JS_FILE = r'd:\history of id course\movement_data.js'

def load_csv_data():
    data = {}
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[row['key']] = row
    return data

def inject_data():
    print("Loading simplified movement data...")
    csv_data = load_csv_data()
    
    with open(JS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Iterate through each movement key in the CSV
    for key, row in csv_data.items():
        print(f"Processing {key}...")
        
        # Regex to find the object block for this key
        # Looks for: "key": { ... }
        # We need to capture the inner content to append/replace fields
        pattern = re.compile(f'"{key}":\s*{{(.*?)}}', re.DOTALL)
        match = pattern.search(content)
        
        if match:
            block_content = match.group(1)
            
            # Helper to replace or append a field
            def update_field(block, field_name, new_value):
                # Escape quotes in the new value
                safe_value = new_value.replace("'", "\\'").replace('"', '\\"')
                # Handle newlines for the long context
                safe_value = safe_value.replace('\n', '\\n')
                
                field_regex = re.compile(f'"{field_name}":\s*".*?",', re.DOTALL)
                
                # Check if field exists
                if field_regex.search(block):
                    # Replace existing
                    return field_regex.sub(f'"{field_name}": "{safe_value}",', block)
                else:
                    # Append new field before the closing brace (simulated by adding to end of block)
                    # We'll actually add it before 'key_features' if it exists, or just append
                    if '"key_features"' in block:
                        return block.replace('"key_features"', f'"{field_name}": "{safe_value}",\n        "key_features"')
                    else:
                        return block + f', "{field_name}": "{safe_value}"'

            # Update fields
            # Description (might already exist)
            block_content = update_field(block_content, 'description', row['description'])
            
            # Philosophy (New)
            block_content = update_field(block_content, 'philosophy', row['philosophy'])
            
            # Impact (New)
            block_content = update_field(block_content, 'impact', row['impact'])
            
            # Sociopolitical Context (New)
            block_content = update_field(block_content, 'sociopolitical_context', row['sociopolitical_context'])
            
            # Reconstruct the full block
            new_block = f'"{key}": {{{block_content}}}'
            
            # Replace in main content
            content = content.replace(match.group(0), new_block)
            
        else:
            print(f"Warning: Could not find block for key '{key}' in JS file.")

    # Write back
    with open(JS_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Injection complete.")

if __name__ == "__main__":
    inject_data()
