
from fastapi import FastAPI

from config import Config
from schemas import Blockchain

cfg = Config()
app = FastAPI()
blockchain = Blockchain(difficulty=cfg.difficulty)

# TODO create pydantic schemas

@app.get("/blockchain/length")
async def get_blockchain_length():
    return {"length": len(blockchain.chain)}

@app.get("/blockchain/history")
async def get_blockchain_history():
    return {"history": blockchain.chain}

@app.post("/blockchain/append")
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
        blockchain.create_new_block()
    except Exception as e:
        #TODO: handle exception correctly
        pass

