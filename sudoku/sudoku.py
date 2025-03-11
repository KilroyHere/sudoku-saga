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

class SudokuLogger:
    """Handles logging of Sudoku solving process."""
    def __init__(self, solver):
        self.solver = solver

    def log_state(self, board_state: BoardState, is_final: bool = False):
        """Log the current state of the board."""
        prefix = "\nState Machine: Final state" if is_final else "\nState Machine: Current state"
        self.solver.display(f"{prefix} = {board_state.state_name}")
        self.solver.display(f"Board valid: {board_state.is_valid}")
        self.solver.display(f"Board solved: {board_state.is_solved}")
        self.solver.display(f"Empty cells: {board_state.empty_cells}")

    def log_strategy_result(self, strategy_found: bool, strategy_name: str):
        """Log the result of strategy finding."""
        self.solver.display(f"Finding strategy: found = {strategy_found}, strategy = {strategy_name}")

    def log_strategy_updates(self, updates: List):
        """Log the updates made by a strategy."""
        self.solver.display(f"Applied strategy: updates = {updates}")

    def log_solve_check(self, is_solved: bool):
        """Log the result of solve check."""
        self.solver.display(f"Checking if solved: {is_solved}")

class SudokuObserver:
    """Observer interface for monitoring Sudoku solving process."""
    def on_strategy_found(self, strategy_name):
        pass
    
    def on_strategy_applied(self, strategy_name, updates):
        pass
    
    def on_state_changed(self, state, board):
        pass

class Sudoku:
    def __init__(self, board: Board, solver):
        self.board = board
        self.solver = solver
        self.solver_state_machine = SudokuStateMachine(self.solver)
        self.observers = []  # List of observers monitoring the solving process
        assert self.board == self.solver.board, "Solver and Sudoku have different Boards!"
    
    def add_observer(self, observer):
        """Add an observer to monitor the solving process."""
        self.observers.append(observer)
        self.solver_state_machine.observers = self.observers
    
    def solve(self):
        """Solve the entire puzzle at once."""
        solved = self.solver_state_machine.solve()
        print("Solved :)" if solved else "Could not solve :(")
        return solved

class SudokuStateMachine:
    def __init__(self, solver) -> None:
        self.solver = solver
        self.logger = SudokuLogger(solver)
        self.states = {
            "finding_best_strategy": self.finding_best_strategy,
            "applying_strategy": self.applying_strategy,
            "checking_if_solved": self.checking_if_solved,
            "solved": self.solved,
            "unsolvable": self.unsolvable
        }
        self.current_state = "finding_best_strategy"
        self.no_strategy_count = 0  # Track consecutive no-strategy findings
        self.observers = []  # Reference to Sudoku's observers
    
    def solve(self):
        """Main method to run the state machine until the puzzle is solved."""
        if not self.solver.is_strategy_based():
            return self.solver.solve()
        
        while self.current_state not in ("solved", "unsolvable"):
            board_state = BoardState.from_board(self.solver.board, self.current_state)
            self.logger.log_state(board_state)
            
            # Notify observers of state change
            for observer in self.observers:
                observer.on_state_changed(self.current_state, self.solver.board)
            
            self.transition_state()
        
        # Log final state
        final_state = BoardState.from_board(self.solver.board, self.current_state)
        self.logger.log_state(final_state, is_final=True)
        
        # Notify observers of final state
        for observer in self.observers:
            observer.on_state_changed(self.current_state, self.solver.board)
        
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
        self.logger.log_strategy_result(strategy_found, best_strategy)
        
        if strategy_found:
            # Notify observers of strategy found
            for observer in self.observers:
                observer.on_strategy_found(best_strategy)
            
            self.current_state = "applying_strategy"
            self.no_strategy_count = 0  # Reset counter when strategy is found
        else:
            # Only mark as unsolvable if the board is invalid or we've tried too many times
            if not self.solver.board.is_valid() or self.no_strategy_count >= 1:
                self.current_state = "unsolvable"
            else:
                # If no immediate strategy is found but board is valid,
                # we might need more complex strategies
                self.no_strategy_count += 1
                self.current_state = "checking_if_solved"

    def applying_strategy(self):
        """Insert values into the board based on the chosen strategy."""
        updates = self.solver.apply_strategy()
        self.logger.log_strategy_updates(updates)
        
        # Notify observers of strategy applied
        for observer in self.observers:
            observer.on_strategy_applied(self.solver.current_strategy.name, updates)
        
        self.current_state = "checking_if_solved"

    def checking_if_solved(self):
        """Verify if the sudoku is solved."""
        is_solved = self.solver.board.is_solved()
        self.logger.log_solve_check(is_solved)
        
        self.current_state = "solved" if is_solved else "finding_best_strategy"
    
    def solved(self):
        # Stop
        pass
    
    def unsolvable(self):
        # Stop
        pass

    

    


                 

  