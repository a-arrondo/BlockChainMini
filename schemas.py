
import json
import hashlib
import datetime as dt
from dataclasses import dataclass, asdict, field

@dataclass
class Block:
    index: int
    sender: str
    receiver: str
    amount: float
    previous_hash: str | None

    proof: int = 0
    timestamp: str = field(default_factory=lambda: str(dt.datetime.now()))
    hash: str = field(init=False)
    
    def __post_init__(self):
        self.hash = ""
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_dict = asdict(self)
        if "hash" in block_dict:
            del block_dict["hash"]
        block_str = json.dumps(
            block_dict, sort_keys=True
            ).encode()
        return hashlib.sha256(block_str).hexdigest()

