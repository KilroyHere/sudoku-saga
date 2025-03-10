from typing import List, Set, Tuple
from .strategy import Strategy
from board.board import Board

class BoxLineIntersectionStrategy(Strategy):
    """
    Box/Line Intersection Strategy (also known as Line/Box Reduction).
    When a candidate in a row/column appears only in one box, that candidate can be eliminated
    from the rest of that box.
    
    Example:
    If candidate 5 in row 1 appears only in box 0,
    then 5 can be eliminated from all other cells in box 0.
    """
    
    def __init__(self, board: Board):
        super().__init__(board, name="Box/Line Intersection Strategy", type="Candidate Eliminator")
        
    def _get_cells_with_candidate_in_unit(self, unit_type: str, unit_index: int, candidate: int) -> List[Tuple[int, int]]:
        """Get all cells in a unit (row/column) that contain a specific candidate."""
        cells = []
        
        if unit_type == "row":
            for col in range(9):
                if self.board.cells[unit_index][col] is None and candidate in self.board.candidates[unit_index][col]:
                    cells.append((unit_index, col))
        else:  # column
            for row in range(9):
                if self.board.cells[row][unit_index] is None and candidate in self.board.candidates[row][unit_index]:
                    cells.append((row, unit_index))
                    
        return cells
    
    def _cells_in_same_box(self, cells: List[Tuple[int, int]]) -> Tuple[bool, int]:
        """Check if all cells are in the same box. Returns (True/False, box_index)."""
        if not cells:
            return False, -1
            
        boxes = {(row // 3) * 3 + (col // 3) for row, col in cells}
        if len(boxes) == 1:
            return True, next(iter(boxes))
            
        return False, -1
    
    def _eliminate_from_box(self, box: int, candidate: int, exclude_cells: Set[Tuple[int, int]]) -> List[Tuple[int, int, int]]:
        """Eliminate candidate from cells in the box except for the excluded cells."""
        eliminations = []
        box_row, box_col = (box // 3) * 3, (box % 3) * 3
        
        for i in range(3):
            for j in range(3):
                row, col = box_row + i, box_col + j
                if (row, col) not in exclude_cells:
                    if self.board.cells[row][col] is None and candidate in self.board.candidates[row][col]:
                        eliminations.append((row, col, candidate))
                            
        return eliminations
    
    def process(self):
        """
        Find box/line intersections and eliminate candidates.
        Returns a list of (row, col, candidate) tuples indicating candidates to eliminate.
        """
        all_eliminations = []
        
        # Check each candidate
        for candidate in range(1, 10):
            # Check each row and column
            for unit_type in ["row", "column"]:
                for unit_index in range(9):
                    # Get cells in this unit that contain this candidate
                    cells = self._get_cells_with_candidate_in_unit(unit_type, unit_index, candidate)
                    
                    # If we found cells with this candidate
                    if cells:
                        # Check if they're all in the same box
                        in_same_box, box = self._cells_in_same_box(cells)
                        
                        if in_same_box:
                            # Eliminate this candidate from other cells in the box
                            eliminations = self._eliminate_from_box(box, candidate, set(cells))
                            all_eliminations.extend(eliminations)
        
        return all_eliminations if all_eliminations else None 