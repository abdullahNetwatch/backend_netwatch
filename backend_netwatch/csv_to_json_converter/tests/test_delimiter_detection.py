import csv
from csv import reader

# reader = csv.reader(open(r"csv_to_json\1_codes.csv", "r"), delimiter=',')
# writer = csv.writer(open(r"csv_to_json\output.csv", 'w'), delimiter='|')
# writer.writerows(reader)

# print("Delimiter successfully changed")

filename = r'csv_to_json\data\000Webhost.txt'

with open(filename, 'r', encoding="utf8") as csvfile:
    dialect = csv.Sniffer().sniff(csvfile.read(1024))
    print(dialect.delimiter)
