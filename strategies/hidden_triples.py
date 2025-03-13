from typing import List, Optional, Tuple, Dict, Set, FrozenSet
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy


class HiddenTriplesStrategy(Strategy):
    """
    Hidden Triples Strategy.
    
    This strategy identifies three candidates that appear only in the same three cells
    within a unit (row, column, or box), even though those cells may contain other
    candidates. When found, all other candidates can be eliminated from those three cells.
    
    The strategy works by:
    1. Finding three candidates that appear only in three cells within a unit
    2. Identifying the cells containing these candidates
    3. Eliminating all other candidates from those cells
    
    Example:
        If in a row, numbers 2,5,7 appear only in cells A,B,C (even though these cells
        have other candidates like [2,4,5,9], [2,5,8], [4,7,8,9]), then:
        - Cells A,B,C must contain 2,5,7
        - All other candidates (4,8,9) can be eliminated from these cells
  
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Hidden Triples Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Hidden Triples Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden triples in rows, columns, and boxes.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no hidden triples are found.
        """
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if less than 3 empty cells
                if len(empty_cells) < 3:
                    continue
                
                # Find hidden triples in this unit
                unit_eliminations = self._find_hidden_triples_in_unit(empty_cells)
                if unit_eliminations:
                    return unit_eliminations  # Return as soon as we find a useful triple
        
        return None
    
    def _find_hidden_triples_in_unit(self, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find hidden triples within a given unit's empty cells.
        
        Args:
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the unit
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a hidden triple is found,
            None otherwise.
        """
        # Create a map of candidates to cells they appear in
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        # Find candidates that appear in 2 or 3 cells
        potential_candidates = [
            (candidate, frozenset(locations))
            for candidate, locations in candidate_locations.items()
            if 2 <= len(locations) <= 3
        ]
        
        # Check all possible combinations of three candidates
        for cands in combinations(potential_candidates, 3):
            # Get all cells where these candidates appear
            all_cells = set().union(*(locs for _, locs in cands))
            
            # If these candidates appear in exactly three cells
            if len(all_cells) == 3:
                # Get the three candidates
                triple = {cand for cand, _ in cands}
                
                # Try to eliminate other candidates from these cells
                eliminations = []
                for row, col in all_cells:
                    for candidate in list(self.board.candidates[row][col]):
                        if candidate not in triple:
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