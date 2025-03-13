from board.board import Board
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BoardState:
    """Encapsulates the current state of the Sudoku board."""
    is_valid: bool
    is_solved: bool
    empty_cells: int
    state_name: str

    @classmethod
    def from_board(cls, board: Board, state_name: str) -> 'BoardState':
        empty_cells = sum(1 for row in board.cells for cell in row if cell is None)
        return cls(
            is_valid=board.is_valid(),
            is_solved=board.is_solved(),
            empty_cells=empty_cells,
            state_name=state_name
        )

class Sudoku:
    def __init__(self, board: Board, solver, logger=None):
        self.board = board
        self.solver = solver
        self.solver_state_machine = SudokuStateMachine(self.solver, logger)
        assert self.board == self.solver.board, "Solver and Sudoku have different Boards!"
    
    def solve(self):
        """Solve the entire puzzle at once."""
        solved = self.solver_state_machine.solve()
        return solved

class SudokuStateMachine:
    def __init__(self, solver, logger=None) -> None:
        self.solver = solver
        self.logger = logger  # Use the new centralized logger
        self.states = {
            "finding_best_strategy": self.finding_best_strategy,
            "applying_strategy": self.applying_strategy,
            "checking_if_solved": self.checking_if_solved,
            "solved": self.solved,
            "unsolvable": self.unsolvable
        }
        self.current_state = "finding_best_strategy"
        self.no_strategy_count = 0  # Track consecutive no-strategy findings
    
    def solve(self):
        """Main method to run the state machine until the puzzle is solved."""
        if not self.solver.is_strategy_based():
            return self.solver.solve()
        
        # Set the board in the logger and log initial state
        if self.logger:
            self.logger.set_board(self.solver.board)
            self.logger.log_initial_state(self.solver.board)
        
        while self.current_state not in ("solved", "unsolvable"):
            # Log state change
            if self.logger:
                self.logger.log_state_change(self.current_state, self.solver.board)
            
            self.transition_state()
        
        # Log final state
        if self.logger:
            self.logger.log_state_change(self.current_state, self.solver.board)
            self.logger.log_final_state(self.solver.board, self.current_state == "solved")
        
        return self.current_state == "solved"

    def transition_state(self):
        """Transition between states based on the current state."""
        if self.current_state in self.states:
            self.states[self.current_state]()
        else:
            raise ValueError(f"Unknown state: {self.current_state}")

    def finding_best_strategy(self):
        """Determine the best strategy to apply next."""
        strategy_found, best_strategy = self.solver.find_strategy()
        
        if strategy_found:
            self.current_state = "applying_strategy"
            self.no_strategy_count = 0  # Reset counter when strategy is found
        else:
            # Only mark as unsolvable if the board is invalid or we've tried too many times
            if not self.solver.board.is_valid() or self.no_strategy_count >= 1:
                self.current_state = "unsolvable"
                # Only log no strategies found when transitioning to unsolvable
                if self.logger:
                    self.logger.log_no_strategies_found()
            else:
                # If no immediate strategy is found but board is valid,
                # we might need more complex strategies
                self.no_strategy_count += 1
                self.current_state = "checking_if_solved"

    def applying_strategy(self):
        """Insert values into the board based on the chosen strategy."""
        updates = self.solver.apply_strategy()
        
        # Log strategy application
        if self.logger and hasattr(self.solver, 'current_strategy') and self.solver.current_strategy:
            # Get update type if available
            update_type = None
            if hasattr(self.solver, 'last_update_type'):
                update_type = self.solver.last_update_type
            
            self.logger.log_strategy_applied(
                self.solver.current_strategy.name, 
                updates,
                update_type
            )
        
        self.current_state = "checking_if_solved"

    def checking_if_solved(self):
        """Verify if the sudoku is solved."""
        is_solved = self.solver.board.is_solved()
        
        # Log solve check
        if self.logger:
            self.logger.log_solve_check(is_solved)
        
        self.current_state = "solved" if is_solved else "finding_best_strategy"
    
    def solved(self):
        # Stop
        pass
    
    def unsolvable(self):
        # Stop
        pass

    

    


                 

  