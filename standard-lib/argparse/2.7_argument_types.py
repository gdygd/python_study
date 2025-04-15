import argparse

# py 2.7_argument_types.py  -r 1.1 -i 10 -s abc

parser = argparse.ArgumentParser(description='A simple argparse example.')
parser.add_argument("-r", "--ratio", type=float)
parser.add_argument("-i", "--num", type=int)
parser.add_argument("-s", "--string", type=str)
args = parser.parse_args()

print(f"Ratio: {args.ratio}")
print(f"num: {args.num}")
print(f"str: {args.string}")
