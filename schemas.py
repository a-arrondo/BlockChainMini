
from pydantic import BaseModel


class StatusModel(BaseModel):
    length: int
    is_valid: bool

class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float

class BlockModel(BaseModel):
    index: int
    previous_hash: str
    timestamp: str
    transactions: list[TransactionModel]
    nonce: int
    hash: str

class HistoryModel(StatusModel):
    history: list[BlockModel]


