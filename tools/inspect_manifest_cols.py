import csv

with open('manifest.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("Fieldnames:", reader.fieldnames)
