from typing import List, Set, Tuple
from .strategy import Strategy
from board.board import Board

class PointingPairsStrategy(Strategy):
    """
    Pointing Pairs/Triples Strategy.
    When a candidate appears in only 2 or 3 cells within a box, and those cells share a row or column,
    that candidate can be eliminated from other cells in that row or column.
    
    Example:
    If a candidate 5 appears only in cells (1,1) and (1,2) within box 0,
    then 5 can be eliminated from all other cells in row 1 outside box 0.
    """
    
    def __init__(self, board: Board):
        super().__init__(board, name="Pointing Pairs Strategy", type="Candidate Eliminator")
        
    def _get_cells_with_candidate_in_box(self, box: int, candidate: int) -> List[Tuple[int, int]]:
        """Get all cells in a box that contain a specific candidate."""
        cells = []
        box_row, box_col = (box // 3) * 3, (box % 3) * 3
        
        for i in range(3):
            for j in range(3):
                row, col = box_row + i, box_col + j
                if self.board.cells[row][col] is None and candidate in self.board.candidates[row][col]:
                    cells.append((row, col))
        
        return cells
    
    def _cells_share_unit(self, cells: List[Tuple[int, int]]) -> Tuple[bool, str, int]:
        """Check if cells share a row or column."""
        if not cells:
            return False, "", -1
            
        rows = {row for row, _ in cells}
        cols = {col for _, col in cells}
        
        if len(rows) == 1:
            return True, "row", next(iter(rows))
        if len(cols) == 1:
            return True, "column", next(iter(cols))
            
        return False, "", -1
    
    def _eliminate_from_unit(self, unit_type: str, unit_index: int, box: int, candidate: int) -> List[Tuple[int, int, int]]:
        """Eliminate candidate from cells in the unit (row/column) outside the box."""
        eliminations = []
        box_row, box_col = (box // 3) * 3, (box % 3) * 3
        
        if unit_type == "row":
            # Eliminate from the row outside the box
            for col in range(9):
                if not (box_col <= col < box_col + 3):  # If cell is not in the box
                    if self.board.cells[unit_index][col] is None:
                        if candidate in self.board.candidates[unit_index][col]:
                            eliminations.append((unit_index, col, candidate))
                            
        elif unit_type == "column":
            # Eliminate from the column outside the box
            for row in range(9):
                if not (box_row <= row < box_row + 3):  # If cell is not in the box
                    if self.board.cells[row][unit_index] is None:
                        if candidate in self.board.candidates[row][unit_index]:
                            eliminations.append((row, unit_index, candidate))
                            
        return eliminations
    
    def process(self):
        """
        Find pointing pairs/triples in each box and eliminate candidates from corresponding rows/columns.
        Returns a list of (row, col, candidate) tuples indicating candidates to eliminate.
        """
        all_eliminations = []
        
        # Check each box
        for box in range(9):
            # Check each candidate
            for candidate in range(1, 10):
                # Get cells in this box that contain this candidate
                cells = self._get_cells_with_candidate_in_box(box, candidate)
                
                # If we found 2 or 3 cells with this candidate
                if len(cells) in [2, 3]:
                    # Check if they share a row or column
                    shares_unit, unit_type, unit_index = self._cells_share_unit(cells)
                    
                    if shares_unit:
                        # Eliminate this candidate from other cells in the shared unit
                        eliminations = self._eliminate_from_unit(unit_type, unit_index, box, candidate)
                        all_eliminations.extend(eliminations)
        
        return all_eliminations if all_eliminations else None 