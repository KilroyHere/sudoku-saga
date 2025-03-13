from typing import List, Optional, Tuple, Dict, Set, FrozenSet
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

class NakedPairsStrategy(Strategy):
    """
    Naked Pairs Strategy.
    
    This strategy identifies two cells within a unit (row, column, or box) that have
    the exact same two candidates. When found, these candidates can be eliminated from
    all other cells in the unit.
    
    The strategy works by:
    1. Finding cells that have exactly two candidates
    2. Looking for pairs of such cells with identical candidates
    3. Eliminating these candidates from other cells in the same unit
    
    Example:
        If two cells in a row both have candidates [2,7], then:
        - These two cells must contain 2 and 7
        - 2 and 7 can be eliminated from all other cells in that row

    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Naked Pairs Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Naked Pairs Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find naked pairs in rows, columns, and boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no naked pairs are found.
        """
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if less than 2 empty cells
                if len(empty_cells) < 2:
                    continue
                
                # Find naked pairs in this unit
                unit_eliminations = self._find_naked_pairs_in_unit(empty_cells)
                if unit_eliminations:
                    return unit_eliminations  # Return as soon as we find a useful pair
        
        return None
    
    def _find_naked_pairs_in_unit(self, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find naked pairs within a given unit's empty cells.
        
        Args:
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the unit
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a naked pair is found,
            None otherwise.
        """
        # Find cells with exactly two candidates
        pair_cells = [
            (row, col, frozenset(self.board.candidates[row][col]))
            for row, col in empty_cells
            if len(self.board.candidates[row][col]) == 2
        ]
        
        # Check all possible combinations of two cells
        for (row1, col1, cands1), (row2, col2, cands2) in combinations(pair_cells, 2):
            # If these cells have the same candidates
            if cands1 == cands2:
                # Try to eliminate these candidates from other cells in the unit
                eliminations = []
                for row, col in empty_cells:
                    if (row, col) not in [(row1, col1), (row2, col2)]:
                        for candidate in cands1:
                            if candidate in self.board.candidates[row][col]:
                                eliminations.append((row, col, candidate))
                
                if eliminations:
                    return eliminations
        
        return None

    def _get_empty_cells_in_unit(self, unit_type, index):
        """
        Get all empty cells in a given unit (row, column, or box).
        
        Args:
            unit_type (str): Type of unit ('row', 'column', or 'box')
            index (int): Index of the unit (0-8)
            
        Returns:
            list: List of (row, col) tuples representing empty cells
        """
        empty_cells = []
        if unit_type == 'row':
            for col in range(9):
                if self.board.cells[index][col] is None:
                    empty_cells.append((index, col))
        elif unit_type == 'column':
            for row in range(9):
                if self.board.cells[row][index] is None:
                    empty_cells.append((row, index))
        else:  # box
            box_row, box_col = (index // 3) * 3, (index % 3) * 3
            for i in range(3):
                for j in range(3):
                    row, col = box_row + i, box_col + j
                    if self.board.cells[row][col] is None:
                        empty_cells.append((row, col))
        return empty_cells 