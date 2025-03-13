from solvers.solver import Solver

class BacktrackingSolver(Solver):

    def __init__(self, board, mode="Default"):
        super().__init__(board, mode)
        self.cache = {}  # Memoization cache
    
    def is_strategy_based(self):
        return False
    
    def solve(self):
        """Solve the Sudoku puzzle using backtracking with optimizations."""
        self.board.update_candidates_backtracking()  # Initialize candidates
        return self._solve_board()
    
    def _board_to_tuple(self):
        """Convert board state to a hashable tuple."""
        return tuple(tuple(row) for row in self.board.cells)

    def _find_most_constrained_cell(self):
        """Find the empty cell with the fewest possible candidates (MRV heuristic)."""
        min_candidates = float('inf')
        best_cell = None

        for row in range(9):
            for col in range(9):
                if self.board.cells[row][col] is None:
                    num_candidates = len(self.board.candidates[row][col])
                    if num_candidates < min_candidates:
                        min_candidates = num_candidates
                        best_cell = (row, col)
        
        return best_cell  # Returns (row, col) or None if board is full

    def _solve_board(self):
        """Recursive helper function to solve the Sudoku board."""
        board_key = self._board_to_tuple()
        if board_key in self.cache:
            return self.cache[board_key]

        # Select the most constrained cell first (MRV heuristic)
        cell = self._find_most_constrained_cell()
        if cell is None:
            self.cache[board_key] = True  # Board solved
            return True  

        row, col = cell

        # Try each possible number for this cell
        for num in sorted(self.board.candidates[row][col]):  # Sort for consistency
            if self.board.check_placement(num, row, col):
                self.board.cells[row][col] = num
                
                # Forward checking: Temporarily update candidates
                saved_candidates = self.board.candidates.copy()
                self.board.update_candidates_backtracking()

                if self._solve_board():
                    self.cache[board_key] = True
                    return True
                
                # Backtrack: Restore previous state
                self.board.cells[row][col] = None
                self.board.candidates = saved_candidates

        self.cache[board_key] = False  # No valid number found, backtrack
        return False  
