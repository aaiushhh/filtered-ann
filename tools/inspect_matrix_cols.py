import csv

with open("matrix.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

print("Fieldnames:", fieldnames)
print("Total rows:", len(rows))
