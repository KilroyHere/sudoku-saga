from typing import List, Optional, Tuple, Dict, Set, FrozenSet
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

'''
This strategy identifies hidden pairs in a unit (row, column, or box).
A hidden pair occurs when two candidates appear in only two cells within a unit,
and these cells may contain other candidates.

For example, if in a row, the numbers 4,7 only appear in two cells
(even though these cells may have other candidates), then 4 and 7 must go in these cells,
and all other candidates can be eliminated from these cells.

This is a candidate eliminator strategy, where candidates are removed based on pattern analysis.

Reference: https://www.sudokuwiki.org/Hidden_Candidates#HP
'''

class HiddenPairsStrategy(Strategy):
    """
    Hidden Pairs Strategy.
    
    This strategy identifies two candidates that appear only in the same two cells
    within a unit (row, column, or box), even though those cells may contain other
    candidates. When found, all other candidates can be eliminated from those two cells.
    
    The strategy works by:
    1. Finding pairs of candidates that appear only in two cells within a unit
    2. Identifying the cells containing these candidates
    3. Eliminating all other candidates from those cells
    
    Example:
        If in a row, numbers 2,7 appear only in cells A,B (even though these cells
        have other candidates like [2,4,7,9] and [2,5,7,8]), then:
        - Cells A,B must contain 2,7
        - All other candidates (4,5,8,9) can be eliminated from these cells
    
    Reference: https://www.sudokuwiki.org/Hidden_Candidates#HP
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Hidden Pairs Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Hidden Pairs Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden pairs in rows, columns, and boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no hidden pairs are found.
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
                
                # Find hidden pairs in this unit
                unit_eliminations = self._find_hidden_pairs_in_unit(empty_cells)
                if unit_eliminations:
                    return unit_eliminations  # Return as soon as we find a useful pair
        
        return None
    
    def _find_hidden_pairs_in_unit(self, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden pairs within a given unit's empty cells.
        
        Args:
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the unit
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a hidden pair is found,
            None otherwise.
        """
        # Create a map of candidates to cells they appear in
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        # Find candidates that appear in 2 cells
        potential_candidates = [
            (candidate, frozenset(locations))
            for candidate, locations in candidate_locations.items()
            if len(locations) == 2
        ]
        
        # Check all possible combinations of two candidates
        for (cand1, locs1), (cand2, locs2) in combinations(potential_candidates, 2):
            # If these candidates appear in the same two cells
            if locs1 == locs2:
                # Get the two cells
                cells = list(locs1)
                pair = {cand1, cand2}
                
                # Try to eliminate other candidates from these cells
                eliminations = []
                for row, col in cells:
                    for candidate in list(self.board.candidates[row][col]):
                        if candidate not in pair:
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