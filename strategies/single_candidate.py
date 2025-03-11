from typing import List, Optional, Tuple
from board.board import Board
from strategies.strategy import Strategy

'''
This strategy effectively handles various scenarios where a cell's value can 
be conclusively determined by following the 3 basic rules:
Set(1..9) in a row 
Set(1..9) in a column 
Set(1..9) in a box

Thus making it the only strategy where values are placed.
All other strategies work towards eliminating candidates until one remains.

Reference: https://www.sudokuwiki.org/Getting_Started    
'''

class SingleCandidateStrategy(Strategy):
    """
    Single Candidate Strategy (also known as Naked Singles).
    
    This strategy identifies cells that have only one possible candidate value.
    It is the most basic solving technique and the only strategy that directly
    places values in cells rather than eliminating candidates.
    
    The strategy works by:
    1. Finding cells with only one remaining candidate
    2. Placing that candidate value in the cell
    
    Example:
        If a cell has candidates [4], then 4 must be the value for that cell.
    
    Reference: https://www.sudokuwiki.org/Getting_Started
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Single Candidate Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Single Candidate Strategy", type="Value Finder")

    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find cells that have only one possible candidate value.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value should be placed in the cell at (row, col). Returns None if no single
            candidates are found.
        """
        values_to_insert = []
        
        # Check each empty cell for single candidates
        for row in range(9):
            for col in range(9):
                if self.board.cells[row][col] is None:
                    candidates = self.board.candidates[row][col]
                    if len(candidates) == 1:
                        value = next(iter(candidates))
                        values_to_insert.append((row, col, value))
        
        return values_to_insert if values_to_insert else None
    