import argparse, csv, json
from collections import defaultdict
from datetime import datetime

now = datetime.now()
print(now.strftime("%H:%M:%S"))
#############################################################

parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='fn', help='filename')
parser.add_argument('-d', '--delimiter', type=str, metavar='', default=None, help='delimiter used in csv file')
parser.add_argument('-ro', '--row_offset', type=int, default=1, help='row offset')
parser.add_argument('-en', '--encoding', type=str, default="ISO-8859-1", help='encoding')

subparsers = parser.add_subparsers(dest='command')

preview = subparsers.add_parser('preview', help='preview data')
preview.add_argument('-pc', '--preview_correct_data', action='store_true', default=False, help='preview correct data')
preview.add_argument('-pb', '--preview_incorrect_data', action='store_true', default=False,  help='preview incorrect data')
preview.add_argument('-pl', '--columns_to_preview', type=int, help='number of columns to preview')

convert = subparsers.add_parser('convert', help='convert data to csv')
convert.add_argument('-ci', '--convert_incorrect_data', default=False, action='store_true', help='convert incorrect data')
convert.add_argument('-cc', '--convert_correct_data', default=False, action='store_true', help='convert correct data')

args = parser.parse_args()

############################################################
fi = open(args.filename, 'rb')
data = fi.read()
fi.close()
fo = open(args.filename, 'wb')
fo.write(data.replace(b'\x00', b''))
fo.close()
# csv.field_size_limit(100000000)
#############################################################
def find_delimiter(filename):
    with open(filename, 'r', encoding=args.encoding) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        return dialect.delimiter

delimiter = args.delimiter or find_delimiter(args.filename)
#############################################################
col_lengths = defaultdict(int)

with open(args.filename, 'r', encoding=args.encoding) as csvfile:
    reader = csv.reader(csvfile, delimiter=delimiter, quoting=csv.QUOTE_NONE)
    for row in reader:
        col_lengths[len(row)] += 1

standard_col_length = max(col_lengths, key=col_lengths.get)
now = datetime.now()
print(now.strftime("%H:%M:%S"))

#############################################################
with open(args.filename, 'r', encoding=args.encoding) as csvfile:

    reader = csv.reader(csvfile, delimiter=delimiter, quoting=csv.QUOTE_NONE)
    # row_offsett
    for i in range(args.row_offset):
        next(reader)

    if args.command == 'preview':
        counter = 0
        for row in reader:
            if counter == args.columns_to_preview:
                break
            counter += 1

            if len(row) == standard_col_length and args.preview_correct_data:
                data = dict(zip([i + 1 for i in range(standard_col_length)], row))
                print(data)

            if len(row) != standard_col_length and args.preview_incorrect_data:
                print(row)

    else:
        count = 0
        if args.convert_correct_data:
            with open(args.filename[:-4] + 'good.jsonl', 'w') as jsonlFile:
                for row in reader:
                    # if count == 10:
                    #     break
                    # count += 1

                    if row[-2:] == '\n':
                        row = row[:-2]

                    if len(row) == standard_col_length:
                        data = dict(zip([i + 1 for i in range(standard_col_length)], row))
                        # if data[standard_col_length] == '':
                        #     continue

                        json.dump(data, jsonlFile)
                        jsonlFile.write('\n')
        else:
            with open(args.filename[:-4] + 'bad.jsonl', 'w') as jsonlFile:
                for row in reader:
                    if row[-2:] == '\n':
                        row = row[:-2]
                    if len(row) != standard_col_length:
                        json.dump(row, jsonlFile)
                        jsonlFile.write('\n')
###################################################
now = datetime.now()
print(now.strftime("%H:%M:%S"))