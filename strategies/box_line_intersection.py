from typing import List, Optional, Tuple, Dict, Set
from .strategy import Strategy
from board.board import Board

class BoxLineIntersectionStrategy(Strategy):
    """
    Box/Line Intersection Strategy.
    
    This strategy identifies when a candidate in a box appears only in cells that
    share a common row or column. When found, that candidate can be eliminated from
    other cells in that row/column outside the box.
    
    The strategy works by:
    1. Finding candidates in a box that only appear in one row or column
    2. Eliminating those candidates from other cells in that row/column outside the box
    
    Example:
        If in a box, the number 4 appears as a candidate only in cells that share
        the same row, then:
        - 4 must be in one of those cells in that box
        - 4 can be eliminated from all other cells in that row outside the box
    
    """
    
    def __init__(self, board: Board) -> None:
        """
        Initialize the Box/Line Intersection Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
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
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find box/line intersections in the grid.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no box/line intersections are found.
        """
        # Check each box (0-8)
        for box_index in range(9):
            # Get empty cells in this box
            empty_cells = self._get_empty_cells_in_unit('box', box_index)
            
            # Skip if no empty cells
            if not empty_cells:
                continue
            
            # Find box/line intersections in this box
            box_eliminations = self._find_box_line_intersections(box_index, empty_cells)
            if box_eliminations:
                return box_eliminations  # Return as soon as we find useful eliminations
        
        return None
    
    def _find_box_line_intersections(self, box_index: int, empty_cells: List[Tuple[int, int]]) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find box/line intersections within a given box.
        
        Args:
            box_index (int): Index of the box (0-8)
            empty_cells (List[Tuple[int, int]]): List of empty cell coordinates in the box
            
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if an intersection is found,
            None otherwise.
        """
        box_row, box_col = (box_index // 3) * 3, (box_index % 3) * 3
        
        # Create a map of candidates to their locations in this box
        candidate_locations: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(1, 10)}
        for row, col in empty_cells:
            for candidate in self.board.candidates[row][col]:
                candidate_locations[candidate].append((row, col))
        
        eliminations = []
        
        # Check each candidate that appears in the box
        for candidate, locations in candidate_locations.items():
            if not locations:
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