from board.board import Board

class SudokuStateMachine:
  def __init__(self, solver) -> None:
    self.solver = solver
    self.states = {
            "finding_best_strategy": self.finding_best_strategy,
            "applying_strategy": self.applying_strategy,
            "checking_if_solved": self.checking_if_solved,
            "solved": self.solved,
            "unsolvable": self.unsolvable
        }
    self.current_state = "finding_best_strategy"
    
  def solve(self):
      """Main method to run the state machine until the puzzle is solved."""
      if self.solver.is_strategy_based():
        
        while self.current_state != "solved" and self.current_state != "unsolvable":
            self.transition_state()
        
        if(self.current_state == "solved"):
          return True
        else:
          return False
        
      else:
        return self.solver.solve()
      
  def transition_state(self):
        """Transition between states based on the current state."""
        if self.current_state in self.states:
            self.states[self.current_state]()
        else:
            raise ValueError(f"Unknown state: {self.current_state}")

  def finding_best_strategy(self):
      """Determine the best strategy to apply next."""
      strategy_found, best_strategy = self.solver.find_strategy()
      # print("Best strategy: "+best_strategy)
      # TODO: Maybe present an explanation for the strategy
      if(strategy_found):
        self.current_state = "insert_values"
      else:
        self.current_state = "unsolvable"

  def applying_strategy(self):
      """Insert values into the board based on the chosen strategy."""
      # Insert values and update 
      inserted_values = self.solver.insert_values()
      # print(inserted_values)
      self.current_state = "checking_if_solved"

  def checking_if_solved(self):
      """Verify if the sudoku is solved."""
      if self.board.is_solved():
          self.current_state = "solved"
      else:
          self.current_state = "finding_best_strategy"
  
  def solved(self):
    # Stop
    pass
  
  def unsolvable(self):
    # Stop
    pass

    
    
    
    




class Sudoku:
  def __init__(self , board, solver ):
    self.board = board
    self.solver = solver
    self.solver.board = self.board # Shallow Copy
    self.solver_state_machine = SudokuStateMachine(self.solver)
    
  
  def solve(self):
    solved = self.solver_state_machine.solve()
    if(solved):
      print("Solved :)")
    else:
      print("Could not solve :(") 
    
    


                 

  