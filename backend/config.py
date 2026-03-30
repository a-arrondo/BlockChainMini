
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    difficulty: int = 2
    mining_interval: int = 30
    min_transactions: int = 5
    consensus_interval: int = 60
    genesis_timestamp: str = "2026-01-01 00:00:00"
