import argparse

# py 3.3_subcommand_example.py add ba
# py 3.3_subcommand_example.py list
parser = argparse.ArgumentParser(description='A subcommand example.')
subparsers = parser.add_subparsers(help='Subcommand help')

list_parser = subparsers.add_parser('list', help='List items')
add_parser = subparsers.add_parser('add', help='Add an item')
add_parser.add_argument('item', help='Item to add')

args = parser.parse_args()

print(args)

if hasattr(args, 'item'):
    print(f"Item to add: {args.item}")
else:
    print("Listing items...")

