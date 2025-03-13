from typing import List, Optional, Tuple, Dict, Set, FrozenSet
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy


class HiddenQuadsStrategy(Strategy):
    """
    Hidden Quads Strategy.
    
    This strategy identifies four candidates that appear in exactly four cells within
    a unit (row, column, or box), even though those cells may contain other candidates.
    When found, all other candidates can be eliminated from those four cells.
    
    The strategy works by:
    1. Finding four candidates that appear only in four cells within a unit
    2. Eliminating all other candidates from those four cells
    
    Example:
        If in a row, numbers 1,2,3,4 only appear in cells A,B,C,D (which may have
        other candidates), then:
        - Cells A,B,C,D must contain 1,2,3,4
        - All other candidates can be eliminated from these cells
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Hidden Quads Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Hidden Quads Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden quads in rows, columns, and boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no hidden quads are found.
        """
        eliminations = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if less than 4 empty cells
                if len(empty_cells) < 4:
                    continue
                
                # Find hidden quads in this unit
                unit_eliminations = self._find_hidden_quads_in_unit(empty_cells)
                if unit_eliminations:
                    eliminations.extend(unit_eliminations)
                    return eliminations  # Return as soon as we find a useful quad
        
        return eliminations if eliminations else None
    
    def _find_hidden_quads_in_unit(self, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden quads within a given unit's empty cells.
        
        Args:
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the unit
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a hidden quad is found,
            None otherwise.
        """
        # Create a map of candidates to cells they appear in
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        # Find candidates that appear in 2, 3, or 4 cells
        potential_candidates = [
            (candidate, frozenset(locations))
            for candidate, locations in candidate_locations.items()
            if 2 <= len(locations) <= 4
        ]
        
        # Check all possible combinations of four candidates
        for cands in combinations(potential_candidates, 4):
            # Get all cells where these candidates appear
            all_cells = set().union(*(locs for _, locs in cands))
            
            # If these candidates appear in exactly four cells
            if len(all_cells) == 4:
                # Get the four candidates
                quad = {cand for cand, _ in cands}
                
                # Remove all other candidates from these cells
                eliminations = []
                found_elimination = False
                for row, col in all_cells:
                    for candidate in list(self.board.candidates[row][col]):
                        if candidate not in quad:
                            eliminations.append((row, col, candidate))
                            found_elimination = True
                
                if found_elimination:
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