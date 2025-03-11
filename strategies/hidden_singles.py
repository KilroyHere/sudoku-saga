from typing import List, Optional, Tuple, Dict, Set
from board.board import Board
from strategies.strategy import Strategy

'''
This strategy identifies hidden singles in a unit (row, column, or box).
A hidden single occurs when a candidate appears in only one cell within a unit,
even though that cell may have other candidates.

For example, if in a row, the number 4 only appears as a candidate in one cell
(even though that cell may have other candidates like [4,7,9]), then 4 must go in that cell.

This is a value finder strategy, where we place a value when we find a hidden single.

Reference: https://www.sudokuwiki.org/Hidden_Singles
'''

class HiddenSinglesStrategy(Strategy):
    """
    Hidden Singles Strategy.
    
    This strategy identifies cells where a candidate appears only once within a unit
    (row, column, or box), even though the cell may have other candidates.
    When found, all other candidates can be eliminated from that cell.
    
    The strategy works by:
    1. Finding candidates that appear only once in a unit
    2. Identifying the cell containing that candidate
    3. Eliminating all other candidates from that cell
    
    Example:
        If in a row, number 5 appears as a candidate in only one cell (even though
        that cell has other candidates like [2,5,7]), then:
        - That cell must contain 5
        - All other candidates (2,7) can be eliminated
    
    Reference: https://www.sudokuwiki.org/Hidden_Singles
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Hidden Singles Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Hidden Singles Strategy", type="Value Finder")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden singles in rows, columns, and boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value should be placed in the cell at (row, col). Returns None if no hidden
            singles are found.
        """
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if no empty cells
                if not empty_cells:
                    continue
                
                # Find hidden singles in this unit
                hidden_single = self._find_hidden_single_in_unit(empty_cells)
                if hidden_single:
                    return [hidden_single]  # Return as soon as we find a hidden single
        
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

    def _find_hidden_single_in_unit(self, empty_cells: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int]]:
        """
        Find a hidden single within a given unit's empty cells.
        
        Args:
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the unit
            
        Returns:
            Optional[Tuple[int, int, int]]: A tuple (row, col, value) if a hidden single is found,
            None otherwise.
        """
        # Create a map of candidates to cells they appear in
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        # Check each candidate
        for candidate, locations in candidate_locations.items():
            # If a candidate appears in exactly one cell
            if len(locations) == 1:
                row, col = locations[0]
                # Only return if this cell has multiple candidates
                # (otherwise it would be a naked single)
                if len(self.board.candidates[row][col]) > 1:
                    return (row, col, candidate)
        
        return None 