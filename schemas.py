
import json
import hashlib
import datetime as dt
from dataclasses import dataclass, asdict, field


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float


@dataclass
class Block:
    index: int
    previous_hash: str

    timestamp: str = field(default_factory=lambda: str(dt.datetime.now()))
    transactions: list[Transaction] = field(default_factory=list)
    nonce: int = 0
    hash: str = field(init=False)
    
    def __post_init__(self) -> None:
        self.hash = ""
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_dict = asdict(self)
        if "hash" in block_dict:
            del block_dict["hash"]
        block_str = json.dumps(
            block_dict, sort_keys=True
            ).encode()
        return hashlib.sha256(block_str).hexdigest()


@dataclass
class Blockchain:
    chain: list[Block] = field(default_factory=list)
    pending_transactions: list[Transaction] = field(default_factory=list)
    difficulty: int = 4

    def __post_init__(self):
        self.pending_transactions.append(
            Transaction(
                "Blockchain",
                "Genesis",
                0.0
            )
        )
        self.create_new_block()

    def create_new_block(
            self
            ) -> Block:
        transactions = list(self.pending_transactions)
        
        if not self.chain:
            new_index = 0
            previous_hash = "0"
        else:
            last_block = self.last_block
            new_index = last_block.index + 1
            previous_hash = last_block.hash

        new_block = Block(
            index=new_index,
            previous_hash=previous_hash,
            transactions=transactions
        )

        self.pending_transactions = []
        self.proof_of_work(new_block)
        self.chain.append(new_block)

    def proof_of_work(
            self,
            block: Block
            ) -> None:
        target = "0" * self.difficulty

        while not block.hash.startswith(target):
            block.nonce += 1
            block.hash = block.calculate_hash()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def validate_chain(self) -> bool:
        genesis = self.chain[0]
        if genesis.hash != genesis.calculate_hash():
            return False

        for i in range(1, len(self.chain)):
            cur_block = self.chain[i]
            calculated_hash = cur_block.calculate_hash()

            if (cur_block.hash != calculated_hash or
                cur_block.previous_hash != self.chain[i-1].hash or
                not calculated_hash.startswith("0" * self.difficulty)):
                return False
                
        return True

