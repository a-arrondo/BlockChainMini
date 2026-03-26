
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    json_path: str = "./transactions_log.json"
    difficulty: int = 2
