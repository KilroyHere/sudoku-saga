from typing import List, Optional, Tuple, Dict, Set
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

class SwordfishStrategy(Strategy):
    """
    Swordfish Strategy.
    
    This strategy identifies a pattern where a candidate appears exactly 2 or 3 times in each of three different rows,
    and these candidates are aligned in exactly three columns. When found, the candidate can be eliminated from
    other cells in those columns.
    
    The same pattern can also be found with columns and rows reversed.
    
    The strategy works by:
    1. Finding rows where a candidate appears exactly 2 or 3 times
    2. Looking for triplets of such rows where the candidate appears in exactly three columns
    3. Eliminating the candidate from other cells in those columns
    
    Example:
        If candidate 5 appears:
        - In row 1 at columns 2, 4, and 7
        - In row 5 at columns 2 and 4
        - In row 8 at columns 4 and 7
        Then:
        - Cells (1,2), (1,4), (1,7), (5,2), (5,4), (8,4), (8,7) form a Swordfish pattern
        - Candidate 5 can be eliminated from all other cells in columns 2, 4, and 7
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the Swordfish Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="Swordfish Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find Swordfish patterns in rows and columns.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no Swordfish patterns are found.
        """
        # First check for Swordfish patterns in rows
        row_eliminations = self._find_swordfish_in_rows()
        if row_eliminations:
            return row_eliminations
        
        # Then check for Swordfish patterns in columns
        col_eliminations = self._find_swordfish_in_columns()
        if col_eliminations:
            return col_eliminations
        
        return None
    
    def _find_swordfish_in_rows(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find Swordfish patterns where the candidate appears 2-3 times in each of three rows,
        and these candidates are aligned in exactly three columns.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a Swordfish pattern is found,
            None otherwise.
        """
        # For each candidate value
        for candidate in range(1, 10):
            # Find rows where the candidate appears 2 or 3 times
            rows_with_candidate = []
            row_to_cols = {}  # Maps row index to columns where candidate appears
            
            for row in range(9):
                # Find columns in this row where the candidate appears
                cols = [col for col in range(9) if 
                       self.board.cells[row][col] is None and 
                       candidate in self.board.candidates[row][col]]
                
                # If candidate appears 2 or 3 times in this row
                if len(cols) in [2, 3]:
                    rows_with_candidate.append(row)
                    row_to_cols[row] = cols
            
            # Check all combinations of three rows
            for row1, row2, row3 in combinations(rows_with_candidate, 3):
                # Get all columns where the candidate appears in these rows
                all_cols = set(row_to_cols[row1] + row_to_cols[row2] + row_to_cols[row3])
                
                # If the candidate appears in exactly three columns
                if len(all_cols) == 3:
                    # We found a Swordfish pattern
                    cols = list(all_cols)
                    
                    # Find cells in these columns (excluding the Swordfish cells) where the candidate can be eliminated
                    eliminations = []
                    swordfish_rows = {row1, row2, row3}
                    
                    for col in cols:
                        for row in range(9):
                            if row not in swordfish_rows:
                                if (self.board.cells[row][col] is None and 
                                    candidate in self.board.candidates[row][col]):
                                    eliminations.append((row, col, candidate))
                    
                    if eliminations:
                        return eliminations
        
        return None
    
    def _find_swordfish_in_columns(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find Swordfish patterns where the candidate appears 2-3 times in each of three columns,
        and these candidates are aligned in exactly three rows.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if a Swordfish pattern is found,
            None otherwise.
        """
        # For each candidate value
        for candidate in range(1, 10):
            # Find columns where the candidate appears 2 or 3 times
            cols_with_candidate = []
            col_to_rows = {}  # Maps column index to rows where candidate appears
            
            for col in range(9):
                # Find rows in this column where the candidate appears
                rows = [row for row in range(9) if 
                       self.board.cells[row][col] is None and 
                       candidate in self.board.candidates[row][col]]
                
                # If candidate appears 2 or 3 times in this column
                if len(rows) in [2, 3]:
                    cols_with_candidate.append(col)
                    col_to_rows[col] = rows
            
            # Check all combinations of three columns
            for col1, col2, col3 in combinations(cols_with_candidate, 3):
                # Get all rows where the candidate appears in these columns
                all_rows = set(col_to_rows[col1] + col_to_rows[col2] + col_to_rows[col3])
                
                # If the candidate appears in exactly three rows
                if len(all_rows) == 3:
                    # We found a Swordfish pattern
                    rows = list(all_rows)
                    
                    # Find cells in these rows (excluding the Swordfish cells) where the candidate can be eliminated
                    eliminations = []
                    swordfish_cols = {col1, col2, col3}
                    
                    for row in rows:
                        for col in range(9):
                            if col not in swordfish_cols:
                                if (self.board.cells[row][col] is None and 
                                    candidate in self.board.candidates[row][col]):
                                    eliminations.append((row, col, candidate))
                    
                    if eliminations:
                        return eliminations
        
        return None 