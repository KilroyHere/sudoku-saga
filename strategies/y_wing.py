from typing import List, Optional, Tuple, Dict, Set
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

class YWingStrategy(Strategy):
    """
    Y-Wing Strategy.
    
    This strategy identifies a pattern where:
    1. A pivot cell has exactly two candidates (X,Y)
    2. Two wing cells each share one candidate with the pivot and have exactly two candidates
    3. The wing cells share a common candidate (Z) that is different from the pivot's candidates
    
    The rule states:
    If a cell can see both wing cells, it cannot contain the common candidate (Z).
    
    Example:
    Pivot cell: {X,Y}
    Wing 1: {X,Z}
    Wing 2: {Y,Z}
    Any cell that can see both wing cells cannot contain Z.
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Y-Wing Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Y-Wing Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find Y-Wing patterns in the grid.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no patterns are found.
        """
        # Find all bi-value cells
        bi_value_cells = self._find_bi_value_cells()
        
        # For each potential pivot cell
        for pivot_row, pivot_col, pivot_candidates in bi_value_cells:
            # Find potential wing cells
            wing_cells = self._find_wing_cells(pivot_row, pivot_col, pivot_candidates, bi_value_cells)
            
            # For each pair of wing cells
            for wing1, wing2 in combinations(wing_cells, 2):
                # Check if the wing cells form a valid Y-Wing with the pivot
                if not self._is_valid_ywing(pivot_row, pivot_col, pivot_candidates, wing1, wing2):
                    continue
                
                # Find eliminations based on this Y-Wing pattern
                eliminations = self._find_eliminations(pivot_row, pivot_col, wing1, wing2)
                if eliminations:
                    return eliminations
        
        return None
    
    def _find_bi_value_cells(self) -> List[Tuple[int, int, Set[int]]]:
        """
        Find all cells that have exactly two candidates.
        
        Returns:
            List[Tuple[int, int, Set[int]]]: List of (row, col, candidates) for bi-value cells
        """
        bi_value_cells = []
        for row in range(9):
            for col in range(9):
                if (self.board.cells[row][col] is None and 
                    len(self.board.candidates[row][col]) == 2):
                    bi_value_cells.append((row, col, self.board.candidates[row][col].copy()))
        return bi_value_cells
    
    def _find_wing_cells(self, pivot_row: int, pivot_col: int, pivot_candidates: Set[int],
                        bi_value_cells: List[Tuple[int, int, Set[int]]]) -> List[Tuple[int, int, Set[int]]]:
        """
        Find potential wing cells for a given pivot cell.
        
        Args:
            pivot_row: Row of the pivot cell
            pivot_col: Column of the pivot cell
            pivot_candidates: Candidates of the pivot cell
            bi_value_cells: List of all bi-value cells
        
        Returns:
            List[Tuple[int, int, Set[int]]]: List of potential wing cells
        """
        wing_cells = []
        for row, col, candidates in bi_value_cells:
            # Skip the pivot cell itself
            if row == pivot_row and col == pivot_col:
                continue
            
            # Check if this cell shares exactly one candidate with the pivot
            shared_candidates = candidates.intersection(pivot_candidates)
            if len(shared_candidates) == 1:
                # Check if this cell can see the pivot
                if self._cells_can_see_each_other((pivot_row, pivot_col), (row, col)):
                    wing_cells.append((row, col, candidates))
        
        return wing_cells
    
    def _is_valid_ywing(self, pivot_row: int, pivot_col: int, pivot_candidates: Set[int],
                        wing1: Tuple[int, int, Set[int]], wing2: Tuple[int, int, Set[int]]) -> bool:
        """
        Check if the wing cells form a valid Y-Wing with the pivot.
        
        Args:
            pivot_row: Row of the pivot cell
            pivot_col: Column of the pivot cell
            pivot_candidates: Candidates of the pivot cell
            wing1: (row, col, candidates) of first wing cell
            wing2: (row, col, candidates) of second wing cell
        
        Returns:
            bool: True if valid Y-Wing, False otherwise
        """
        # Get the shared candidates between pivot and each wing
        shared1 = pivot_candidates.intersection(wing1[2])
        shared2 = pivot_candidates.intersection(wing2[2])
        
        # Wings must share different candidates with the pivot
        if shared1 == shared2:
            return False
        
        # Get the common candidate between the wing cells
        common_candidate = wing1[2].intersection(wing2[2])
        if len(common_candidate) != 1:
            return False
        
        # The common candidate must not be in the pivot
        if next(iter(common_candidate)) in pivot_candidates:
            return False
        
        return True
    
    def _cells_can_see_each_other(self, cell1: Tuple[int, int], cell2: Tuple[int, int]) -> bool:
        """
        Check if two cells can see each other (same row, column, or box).
        
        Args:
            cell1: (row, col) of first cell
            cell2: (row, col) of second cell
        
        Returns:
            bool: True if cells can see each other, False otherwise
        """
        row1, col1 = cell1
        row2, col2 = cell2
        
        # Check if in same row
        if row1 == row2:
            return True
        
        # Check if in same column
        if col1 == col2:
            return True
        
        # Check if in same box
        box1_row, box1_col = row1 // 3, col1 // 3
        box2_row, box2_col = row2 // 3, col2 // 3
        if box1_row == box2_row and box1_col == box2_col:
            return True
        
        return False
    
    def _find_eliminations(self, pivot_row: int, pivot_col: int,
                          wing1: Tuple[int, int, Set[int]], wing2: Tuple[int, int, Set[int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find eliminations based on the Y-Wing pattern.
        
        Args:
            pivot_row: Row of the pivot cell
            pivot_col: Column of the pivot cell
            wing1: (row, col, candidates) of first wing cell
            wing2: (row, col, candidates) of second wing cell
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if found
        """
        # Get the common candidate between the wing cells
        common_candidate = wing1[2].intersection(wing2[2])
        if not common_candidate:
            return None
        
        common_candidate_value = next(iter(common_candidate))
        
        # Find cells that can see both wing cells
        eliminations = []
        for row in range(9):
            for col in range(9):
                # Skip the pivot and wing cells
                if (row, col) in [(pivot_row, pivot_col), (wing1[0], wing1[1]), (wing2[0], wing2[1])]:
                    continue
                
                # Check if this cell can see both wing cells
                if (self._cells_can_see_each_other((row, col), (wing1[0], wing1[1])) and 
                    self._cells_can_see_each_other((row, col), (wing2[0], wing2[1]))):
                    # If the cell has the common candidate, it can be eliminated
                    if (self.board.cells[row][col] is None and 
                        common_candidate_value in self.board.candidates[row][col]):
                        eliminations.append((row, col, common_candidate_value))
        
        return eliminations if eliminations else None