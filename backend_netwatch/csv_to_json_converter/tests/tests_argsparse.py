import argparse


parser = argparse.ArgumentParser()

subparsers = parser.add_subparsers(dest='command')
parser.add_argument('a', type=int, help='add two numbers')
parser.add_argument('b', type=int, help='add 2 numbers')


convert = subparsers.add_parser('convert', help='convert to json')
convert.add_argument('-s', '--subtract')


preview = subparsers.add_parser('preview', help='preview data')
preview.add_argument('-m', '--multiply')

args = parser.parse_args()

if not args.command:
    print(args.a, args.b)

if args.command == 'convert':
    print(args.a, args.b, args.convert.s)

if args.command == 'preview':
    print(args.a, args.b, args.multiply)


