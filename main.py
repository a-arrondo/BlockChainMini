
from fastapi import FastAPI

from config import Config
from domain import Blockchain
from schemas import StatusModel, HistoryModel, TransactionModel

cfg = Config()
app = FastAPI()
blockchain = Blockchain(difficulty=cfg.difficulty)

# TODO create pydantic schemas

@app.get("/blockchain/status", response_model=StatusModel)
async def get_blockchain_length():
    try:
        result = {
            "length": len(blockchain.chain),
            "is_valid": blockchain.validate_chain()
        }
        return result
    except Exception as e:
        # TODO
        raise e

@app.get("/blockchain/history", response_model=HistoryModel)
async def get_blockchain_history():
    try:
        result = {
            "length": len(blockchain.chain),
            "is_valid": blockchain.validate_chain(),
            "history": blockchain.chain
        }
        return result
    except Exception as e:
        # TODO
        raise e

@app.post("/blockchain/append", response_model=TransactionModel)
async def add_transaction(
        sender: str,
        receiver: str,
        amount: float
        ):
    try:
        blockchain.add_transaction(
            sender=sender,
            receiver=receiver,
            amount=amount
        )
        blockchain.create_new_block() # TODO: should be removed later
        
        return {
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        }
    except Exception as e:
        #TODO: handle exception correctly
        raise e

