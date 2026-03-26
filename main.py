
from pprint import pprint

from schemas import Block

def main():
    genesis = Block(0, "Alice", "Bob", 10, None)
    pprint(genesis)

if __name__ == "__main__":
    main()
