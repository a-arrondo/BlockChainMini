
from fastapi import status, FastAPI, HTTPException

from service import BlockChainHandler
from schemas import StatusModel, HistoryModel, TransactionModel, NeighbourModel, PeersModel


app = FastAPI()
service = BlockChainHandler()


@app.get("/blockchain/status", response_model=StatusModel)
async def get_blockchain_length():
    try:
        result = service.get_status()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/blockchain/history", response_model=HistoryModel)
async def get_blockchain_history():
    try:
        result = service.get_history()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/blockchain/append", status_code=status.HTTP_204_NO_CONTENT)
async def add_transaction(
        transaction: TransactionModel
        ):
    try:
        service.add_transaction(transaction)
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/blockchain/neighbours", status_code=status.HTTP_204_NO_CONTENT)
async def add_neighbours(
        neighbours: list[NeighbourModel]
        ):
    try:
        service.add_neighbours(neighbours)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/blockchain/neighbours", response_model=PeersModel)
async def get_neighbours():
    try:
        result = service.get_neighbours()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.delete("/blockchain/neighbours", status_code=status.HTTP_204_NO_CONTENT)
async def reset_neighbours():
    try:
        service.reset_neighbours()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.post("/blockchain/block", status_code=status.HTTP_204_NO_CONTENT)
async def receive_block(block: BlockModel):
    try:
        service.add_block(block)
    except ValueError as ve:
        raise HTTPException(
            status_code=400,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
