from typing import List, Optional, Tuple, Set
from board.board import Board

class Strategy:
    """
    Base class for all Sudoku solving strategies.
    
    Each strategy implementation should follow these guidelines:
    1. Inherit from this class
    2. Implement the process() method
    3. Include detailed docstrings explaining the strategy
    4. Use type hints for all methods
    5. Follow consistent naming conventions
    
    Strategy Types:
    - "Value Finder": Strategies that directly find values for cells
    - "Candidate Eliminator": Strategies that eliminate candidates
    """
    
    def __init__(self, board: Board, name: str, type: str) -> None:
        """
        Initialize a strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
            name (str): Name of the strategy
            type (str): Type of strategy ("Value Finder" or "Candidate Eliminator")
        """
        self.board = board
        self._name = name
        self._type = type
    
    @property
    def name(self) -> str:
        """Return the strategy name."""
        return self._name
    
    @property
    def type(self) -> str:
        """Return the strategy type."""
        return self._type
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find and return candidates for this strategy.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where:
                - For Value Finder strategies: value is the number to place in cell (row, col)
                - For Candidate Eliminator strategies: value is the candidate to remove from cell (row, col)
                Returns None if no candidates are found.
        """
        raise NotImplementedError("Strategy must implement the process method.")
    
    def _get_empty_cells_in_unit(self, unit_type: str, index: int) -> List[Tuple[int, int]]:
        """
        Get all empty cells in a given unit (row, column, or box).
        
        Args:
            unit_type (str): Type of unit ('row', 'column', or 'box')
            index (int): Index of the unit (0-8)
            
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples representing empty cells
        """
        empty_cells = []
        if unit_type == 'row':
            empty_cells = [(index, col) for col in range(9) if self.board.cells[index][col] is None]
        elif unit_type == 'column':
            empty_cells = [(row, index) for row in range(9) if self.board.cells[row][index] is None]
        else:  # box
            box_row, box_col = (index // 3) * 3, (index % 3) * 3
            empty_cells = [(box_row + i, box_col + j) 
                          for i in range(3) 
                          for j in range(3) 
                          if self.board.cells[box_row + i][box_col + j] is None]
        return empty_cells
    