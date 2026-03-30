
import uuid
from pydantic import BaseModel, Field


class StatusModel(BaseModel):
    length: int
    is_valid: bool

class TransactionModel(BaseModel):
    sender: str
    receiver: str
    amount: float
    tx_id: str = Field(default_factory=lambda: str(uuid.uuid4())) 

class BlockModel(BaseModel):
    index: int
    previous_hash: str
    timestamp: str
    transactions: list[TransactionModel]
    nonce: int
    hash: str

class HistoryModel(StatusModel):
    history: list[BlockModel]

class NeighbourModel(BaseModel):
    ip: str
    port: int

    def __hash__(self):
        return hash((self.ip, self.port))

    def __eq__(self, other):
        return isinstance(other, NeighbourModel) and \
            self.ip == other.ip and \
            self.port == other.port

class PeersModel(BaseModel):
    n_peers: int
    peers: list[NeighbourModel]
