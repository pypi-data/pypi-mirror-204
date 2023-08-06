from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Cell:
    cell_type: str
    source: List[str]
    metadata: Dict
    execution_count: Optional[int] = None
    outputs: Optional[List] = None
