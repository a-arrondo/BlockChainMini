
import json
import hashlib
import datetime as dt
from dataclasses import dataclass, asdict, field


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    
    def __post_init__(self) -> None:
        if not self.sender.strip():
            raise ValueError("The sender must not be empty")

        if not self.receiver.strip():
            raise ValueError("The receiver must not be empty")

        if self.sender != "Blockchain" and self.amount <= 0:
            raise ValueError("The amount of the transaction must be a positive float")
        
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
        
    def calculate_hash(self) -> str:
        block_str = json.dumps({
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [asdict(tx) for tx in self.transactions],
            "nonce": self.nonce,
        }, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()


@dataclass
class Blockchain:
    chain: list[Block] = field(default_factory=list)
    pending_transactions: list[Transaction] = field(default_factory=list)
    difficulty: int = 4

    def __post_init__(self):
        self.add_transaction(
            "Blockchain",
            "Genesis",
            0.0
        )
        self.create_new_block()

    def create_new_block(
            self
            ) -> None:
        pending_list = list(self.pending_transactions)
        
        if not self.chain:
            new_index = 0
            prev_hash = "0"
        else:
            last_block = self.last_block
            new_index = last_block.index + 1
            prev_hash = last_block.hash

        new_block = Block(
            index=new_index,
            previous_hash=prev_hash,
            transactions=pending_list
        )

        self.pending_transactions = []
        self.proof_of_work(new_block)
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def proof_of_work(
            self,
            block: Block
            ) -> None:
        while not self.valid_pow(block.hash):
            block.nonce += 1
            block.hash = block.calculate_hash()

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def valid_pow(
            self,
            hash: str
            ) -> bool:
        return hash.startswith("0" * self.difficulty)

    def validate_chain(self) -> bool:
        genesis = self.chain[0]
        genesis_calculated_hash = genesis.calculate_hash()
        if (genesis.hash != genesis_calculated_hash or
            not self.valid_pow(genesis_calculated_hash)):
            return False

        for i in range(1, len(self.chain)):
            cur_block = self.chain[i]
            calculated_hash = cur_block.calculate_hash()

            if (cur_block.hash != calculated_hash or
                cur_block.previous_hash != self.chain[i-1].hash or
                not self.valid_pow(calculated_hash)):
                return False
                
        return True
    
    def add_transaction(
            self,
            sender: str,
            receiver: str,
            amount: float
            ) -> None:
        self.pending_transactions.append(
            Transaction(
                sender=sender,
                receiver=receiver,
                amount=amount
            )
        )
