from solvers.solver import Solver
class BacktrackingSolver(Solver):

  def __init__(self, mode = "Default"):
    super().__init__(mode)
    
  def is_strategy_based(self):
    return False
  
  def solve(self):
        """Solve the Sudoku puzzle using backtracking."""
        self.board.update_candidates()  # Update candidates before starting
        if self._solve_board():
            return True
        else:
            return False
    
  def _solve_board(self):
      """Recursive helper function to solve the Sudoku board."""
      for row in range(9):
          for col in range(9):
              if self.board.cells[row][col] is None:
                  for num in self.board.candidates[row][col]:
                      if self.board.check_placement(num, row, col):
                          self.board.cells[row][col] = num
                          self.board.update_candidates()  # Update candidates after placing a number
 
                          if self._solve_board():
                              return True  # Solution found
                          
                          # If no solution, backtrack
                          self.board.cells[row][col] = None
                          self.board.update_candidates()

                  return False  # No valid number found, need to backtrack
              
      return True  # All cells are filled
