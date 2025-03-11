from typing import List, Optional, Tuple, Dict, Set
from .strategy import Strategy
from board.board import Board

class PointingPairsStrategy(Strategy):
    """
    Pointing Pairs Strategy.
    
    This strategy identifies when a candidate in a box appears only in cells that
    share a common row or column. When found, that candidate can be eliminated from
    other cells in that row/column outside the box.
    
    The strategy works by:
    1. Finding candidates in a box that only appear in two or three cells
    2. Checking if these cells share the same row or column
    3. Eliminating the candidate from other cells in that row/column outside the box
    
    Example:
        If in a box, the number 4 appears as a candidate only in two cells that share
        the same row, then:
        - 4 must be in one of those cells in that box
        - 4 can be eliminated from all other cells in that row outside the box
    
    Reference: https://www.sudokuwiki.org/Intersection_Removal#IR
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Pointing Pairs Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Pointing Pairs Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find pointing pairs in boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no pointing pairs are found.
        """
        # Check each box (0-8)
        for box_index in range(9):
            # Get empty cells in this box
            empty_cells = self._get_empty_cells_in_unit('box', box_index)
            
            # Skip if less than 2 empty cells
            if len(empty_cells) < 2:
                continue
            
            # Find pointing pairs in this box
            box_eliminations = self._find_pointing_pairs_in_box(box_index, empty_cells)
            if box_eliminations:
                return box_eliminations  # Return as soon as we find useful eliminations
        
        return None
    
    def _find_pointing_pairs_in_box(self, box_index: int, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find pointing pairs within a given box.
        
        Args:
            box_index (int): Index of the box (0-8)
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the box
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a pointing pair is found,
            None otherwise.
        """
        box_row, box_col = (box_index // 3) * 3, (box_index % 3) * 3
        
        # Create a map of candidates to their locations in this box
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        eliminations = []
        
        # Check each candidate that appears in 2 or 3 cells in the box
        for candidate, locations in candidate_locations.items():
            if len(locations) not in [2, 3]:
                continue
            
            # Check if all occurrences are in the same row
            rows = {row for row, _ in locations}
            if len(rows) == 1:
                row = next(iter(rows))
                # Look for the candidate in other cells in this row
                for col in range(9):
                    # Skip if cell is in the current box
                    if box_col <= col < box_col + 3:
                        continue
                    if (self.board.cells[row][col] is None and 
                        candidate in self.board.candidates[row][col]):
                        eliminations.append((row, col, candidate))
            
            # Check if all occurrences are in the same column
            cols = {col for _, col in locations}
            if len(cols) == 1:
                col = next(iter(cols))
                # Look for the candidate in other cells in this column
                for row in range(9):
                    # Skip if cell is in the current box
                    if box_row <= row < box_row + 3:
                        continue
                    if (self.board.cells[row][col] is None and 
                        candidate in self.board.candidates[row][col]):
                        eliminations.append((row, col, candidate))
        
        return eliminations if eliminations else None 