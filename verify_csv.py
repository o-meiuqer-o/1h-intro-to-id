import sys, csv
sys.stdout.reconfigure(encoding='utf-8')
rows = list(csv.DictReader(open(r'D:\history of id course\design_analysis.csv', encoding='utf-8-sig')))
print(f"CSV: {len(rows)} rows")
designers = {}
for r in rows:
    d = r['designer']
    designers[d] = designers.get(d, 0) + 1
print(f"Designers: {len(designers)}")
for d in sorted(designers):
    print(f"  {d}: {designers[d]}")
# Show sample entry
print("\n=== SAMPLE ENTRY ===")
print(f"Key: {rows[5]['key']}")
print(f"Title: {rows[5]['title']}")
print(f"Context: {rows[5]['context'][:100]}...")
print(f"Analysis: {rows[5]['analysis'][:100]}...")
