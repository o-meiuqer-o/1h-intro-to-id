import csv
import os

input_file = r"d:\history of id course\expanded_designers.csv"
output_file = r"d:\history of id course\expanded_designers_v2.csv"

# 3-Year Baskets from 1830 to 2024
start_year = 1830
end_year = 2024
baskets = []
for y in range(start_year, end_year + 1, 3):
    baskets.append(f"P_{y}")

try:
    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # New Fieldnames
        fieldnames = reader.fieldnames + ['Movements'] + baskets
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for row in reader:
                # Default "Movements" to current CategoryName (as placeholder)
                # Format: MovementName:StartYear
                # We don't have start year easily, so just put "Category:BirthYear" as a default
                movement_placeholder = row.get('CategoryName', 'Unknown')
                birth = row.get('Birth', '1900')
                row['Movements'] = f"{movement_placeholder}:{birth}"
                
                # Initialize all baskets to 0
                for b in baskets:
                    row[b] = 0
                
                writer.writerow(row)
                
    print(f"Successfully created {output_file} with {len(baskets)} new productivity columns.")
    
except Exception as e:
    print(f"Error: {e}")
