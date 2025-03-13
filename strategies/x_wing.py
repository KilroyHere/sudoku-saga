from typing import List, Optional, Tuple, Dict, Set
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

class XWingStrategy(Strategy):
    """
    X-Wing Strategy.
    
    This strategy identifies a pattern where a candidate appears exactly twice in each of two different rows,
    and these candidates are aligned in the same columns. When found, the candidate can be eliminated from
    other cells in those columns.
    
    The same pattern can also be found with columns and rows reversed.
    
    The strategy works by:
    1. Finding rows where a candidate appears exactly twice
    2. Looking for pairs of such rows where the candidate appears in the same columns
    3. Eliminating the candidate from other cells in those columns
    
    Example:
        If candidate 5 appears exactly twice in row 1 (at columns 2 and 7) and
        candidate 5 also appears exactly twice in row 6 (at columns 2 and 7), then:
        - Cells (1,2), (1,7), (6,2), and (6,7) form an X-Wing pattern
        - Candidate 5 can be eliminated from all other cells in columns 2 and 7
    """

    def __init__(self, board: Board) -> None:
        """
        Initialize the X-Wing Strategy.
        
        Args:
            board (Board): The Sudoku board to analyze
        """
        super().__init__(board, name="X-Wing Strategy", type="Candidate Eliminator")
    
    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find X-Wing patterns in rows and columns.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of (row, col, value) tuples where
            value is a candidate that should be eliminated from the cell at (row, col).
            Returns None if no X-Wing patterns are found.
        """
        # First check for X-Wing patterns in rows
        row_eliminations = self._find_x_wing_in_rows()
        if row_eliminations:
            return row_eliminations
        
        # Then check for X-Wing patterns in columns
        col_eliminations = self._find_x_wing_in_columns()
        if col_eliminations:
            return col_eliminations
        
        return None
    
    def _find_x_wing_in_rows(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find X-Wing patterns where the candidate appears exactly twice in each of two rows,
        and these candidates are aligned in the same columns.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if an X-Wing pattern is found,
            None otherwise.
        """
        # For each candidate value
        for candidate in range(1, 10):
            # Find rows where the candidate appears exactly twice
            rows_with_candidate_twice = []
            row_to_cols = {}  # Maps row index to columns where candidate appears
            
            for row in range(9):
                # Find columns in this row where the candidate appears
                cols = [col for col in range(9) if 
                        self.board.cells[row][col] is None and 
                        candidate in self.board.candidates[row][col]]
                
                # If candidate appears exactly twice in this row
                if len(cols) == 2:
                    rows_with_candidate_twice.append(row)
                    row_to_cols[row] = cols
            
            # Check all pairs of rows
            for row1, row2 in combinations(rows_with_candidate_twice, 2):
                # If the candidate appears in the same columns in both rows
                if row_to_cols[row1] == row_to_cols[row2]:
                    # We found an X-Wing pattern
                    col1, col2 = row_to_cols[row1]
                    
                    # Find cells in these columns (excluding the X-Wing cells) where the candidate can be eliminated
                    eliminations = []
                    for row in range(9):
                        if row != row1 and row != row2:
                            # Check column 1
                            if (self.board.cells[row][col1] is None and 
                                candidate in self.board.candidates[row][col1]):
                                eliminations.append((row, col1, candidate))
                            
                            # Check column 2
                            if (self.board.cells[row][col2] is None and 
                                candidate in self.board.candidates[row][col2]):
                                eliminations.append((row, col2, candidate))
                    
                    if eliminations:
                        return eliminations
        
        return None
    
    def _find_x_wing_in_columns(self) -> Optional[List[Tuple[int, int, int]]]:
        """
        Find X-Wing patterns where the candidate appears exactly twice in each of two columns,
        and these candidates are aligned in the same rows.
        
        Returns:
            Optional[List[Tuple[int, int, int]]]: List of eliminations if an X-Wing pattern is found,
            None otherwise.
        """
        # For each candidate value
        for candidate in range(1, 10):
            # Find columns where the candidate appears exactly twice
            cols_with_candidate_twice = []
            col_to_rows = {}  # Maps column index to rows where candidate appears
            
            for col in range(9):
                # Find rows in this column where the candidate appears
                rows = [row for row in range(9) if 
                        self.board.cells[row][col] is None and 
                        candidate in self.board.candidates[row][col]]
                
                # If candidate appears exactly twice in this column
                if len(rows) == 2:
                    cols_with_candidate_twice.append(col)
                    col_to_rows[col] = rows
            
            # Check all pairs of columns
            for col1, col2 in combinations(cols_with_candidate_twice, 2):
                # If the candidate appears in the same rows in both columns
                if col_to_rows[col1] == col_to_rows[col2]:
                    # We found an X-Wing pattern
                    row1, row2 = col_to_rows[col1]
                    
                    # Find cells in these rows (excluding the X-Wing cells) where the candidate can be eliminated
                    eliminations = []
                    for col in range(9):
                        if col != col1 and col != col2:
                            # Check row 1
                            if (self.board.cells[row1][col] is None and 
                                candidate in self.board.candidates[row1][col]):
                                eliminations.append((row1, col, candidate))
                            
                            # Check row 2
                            if (self.board.cells[row2][col] is None and 
                                candidate in self.board.candidates[row2][col]):
                                eliminations.append((row2, col, candidate))
                    
                    if eliminations:
                        return eliminations
        
        return None 