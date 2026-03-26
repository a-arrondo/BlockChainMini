
import json
from pprint import pprint

from schemas import Blockchain
from config import Config

def main():
    cfg = Config()
    with open(cfg.json_path) as f:
        transactions_log = json.load(f)

    blockchain = Blockchain(difficulty=cfg.difficulty)
    print(f"Validation: {blockchain.validate_chain()}\n")
    for i, transaction in enumerate(transactions_log):
        print(f"# Transaction {i}")
        blockchain.add_transaction(
            transaction["sender"],
            transaction["receiver"],
            transaction["amount"]
        )
        blockchain.create_new_block()
        pprint(blockchain)
        print(f"Validation: {blockchain.validate_chain()}\n")
        

if __name__ == "__main__":
    main()
