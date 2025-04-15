import argparse

# py 1_simple_example.py 123

parser = argparse.ArgumentParser(description='A simple argparse example')
parser.add_argument('input', help='Input file to process')

args = parser.parse_args()
print(f'Processing file:{args.input}')