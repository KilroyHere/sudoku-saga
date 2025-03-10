from board.board import Board

class SudokuObserver:
    """Observer interface for monitoring Sudoku solving process."""
    def on_strategy_found(self, strategy_name):
        pass
    
    def on_strategy_applied(self, strategy_name, updates):
        pass
    
    def on_state_changed(self, state, board):
        pass

class Sudoku:
    def __init__(self, board:Board, solver):
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
        if solved:
            print("Solved :)")
        else:
            print("Could not solve :(")
        return solved

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
        self.no_strategy_count = 0  # Track consecutive no-strategy findings
        self.observers = []  # Reference to Sudoku's observers
    
    def solve(self):
        """Main method to run the state machine until the puzzle is solved."""
        if not self.solver.is_strategy_based():
            return self.solver.solve()
        
        while self.current_state != "solved" and self.current_state != "unsolvable":
            self.solver.display(f"\nState Machine: Current state = {self.current_state}")
            self.solver.display(f"Board valid: {self.solver.board.is_valid()}")
            self.solver.display(f"Board solved: {self.solver.board.is_solved()}")
            empty_cells = sum(1 for row in self.solver.board.cells for cell in row if cell is None)
            self.solver.display(f"Empty cells: {empty_cells}")
            
            # Notify observers of state change
            for observer in self.observers:
                observer.on_state_changed(self.current_state, self.solver.board)
            
            self.transition_state()
        
        self.solver.display(f"\nState Machine: Final state = {self.current_state}")
        self.solver.display(f"Board valid: {self.solver.board.is_valid()}")
        self.solver.display(f"Board solved: {self.solver.board.is_solved()}")
        empty_cells = sum(1 for row in self.solver.board.cells for cell in row if cell is None)
        self.solver.display(f"Empty cells: {empty_cells}")
        
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
        self.solver.display(f"Finding strategy: found = {strategy_found}, strategy = {best_strategy}")
        
        if strategy_found:
            # Notify observers of strategy found
            for observer in self.observers:
                observer.on_strategy_found(best_strategy)
            
            self.current_state = "applying_strategy"
            self.no_strategy_count = 0  # Reset counter when strategy is found
        else:
            # Only mark as unsolvable if the board is invalid or we've tried too many times
            if not self.solver.board.is_valid() or self.no_strategy_count >= 3:
                self.current_state = "unsolvable"
            else:
                # If no immediate strategy is found but board is valid,
                # we might need more complex strategies
                self.no_strategy_count += 1
                self.current_state = "checking_if_solved"

    def applying_strategy(self):
        """Insert values into the board based on the chosen strategy."""
        updates = self.solver.apply_strategy()
        self.solver.display(f"Applied strategy: updates = {updates}")
        
        # Notify observers of strategy applied
        for observer in self.observers:
            observer.on_strategy_applied(self.solver.current_strategy.name, updates)
        
        self.current_state = "checking_if_solved"

    def checking_if_solved(self):
        """Verify if the sudoku is solved."""
        is_solved = self.solver.board.is_solved()
        self.solver.display(f"Checking if solved: {is_solved}")
        
        if is_solved:
            self.current_state = "solved"
        else:
            self.current_state = "finding_best_strategy"
    
    def solved(self):
        # Stop
        pass
    
    def unsolvable(self):
        # Stop
        pass

    

    


                 

  