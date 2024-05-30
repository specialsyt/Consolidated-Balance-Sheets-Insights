
from dataclasses import dataclass

@dataclass
class ProcessingRequest:
    ticker: str = ""
    year: int = 0
    running: bool = False
    cached: bool = False