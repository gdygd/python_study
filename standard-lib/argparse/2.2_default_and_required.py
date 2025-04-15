import argparse

# py 2.2_default_and_required.py aaa bbb

parser = argparse.ArgumentParser(description='A simple argparse example')
parser.add_argument('input', help='Input file to process')
parser.add_argument('-o', '--output', required=True, help='Output file.')

args = parser.parse_args()
print(f'Processing file : {args.input}')
print(f'Writing file : {args.output}')