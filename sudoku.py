from board import Board

class Sudoku:

  def __init__(self , board, solver ):
    self.board = board
    self.solver = solver
    self.solver.board = self.board # Shallow Copy
    self.validator = self.solver.validator
    
    assert self.validator.validate(board.cells), "Illegal Numbers Input"
    assert self.solver.board == self.board, "Solver and Sudoku boards don't match!"
  
  def solve(self):
   if self.solver.isStateMachine():
     pass
   else:
     self.solver.solve()


                 