from dataclasses import dataclass
from typing import Optional, List, Dict


@dataclass
class Cell:
    """
    A class to make the object from the cell dictionary

    :param cell_type: type of the cell
    :type cell_type: str
    :param source: source of the cell, where the code exists
    :type source: list
    :param metadata: metadata of the cell
    :type metadata: dict
    :param execution_count: count of the execution
    :type execution_count: Optional[list]
    :param outputs: outputs of the cell
    :type outputs: Optional[list]
    """

    cell_type: str
    source: List[str]
    metadata: Dict
    execution_count: Optional[int] = None
    outputs: Optional[List] = None
