from collections import Counter
import csv
filename = r'csv_to_json\data\YouNow_July_2017.txt'

col_lens = []
with open(filename, 'r', encoding="utf8") as csvfile:
    # reader = csv.DictReader(csvfile, delimiter=',')
    # next(reader)
    for row in csvfile:
        col_lens.append(len(row))

print(Counter(col_lens))
