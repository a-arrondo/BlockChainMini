
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    difficulty: int = 2
    mining_interval: int = 30
    min_transactions: int = 5
