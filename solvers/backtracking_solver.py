
from solvers.solver import Solver
class BacktrackingSolver(Solver):

  def __init__(self,validator, mode = "Default"):
    super().__init__( validator, mode)

  def isStateMachine(self):
    return True
  
  def solve(self):
    pass