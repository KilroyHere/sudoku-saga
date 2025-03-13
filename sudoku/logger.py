from typing import List, Optional, Any

class SudokuLogger:
    """Centralized logger for Sudoku solving process with verbose/non-verbose modes."""
    
    def __init__(self, verbose: bool = False):
        """Initialize the logger.
        
        Args:
            verbose: Whether to show detailed output
        """
        self.verbose = verbose
        self.step_counter = 0
        self.strategies_used = []
        self.strategy_counts = {}
        self.current_board = None
    
    def set_board(self, board):
        """Set the current board reference."""
        self.current_board = board
    
    def log_initial_state(self, board):
        """Log the initial state of the board."""
        # Always show initial board in both modes
        print("\nInitial board:")
        board.display_board()
        print("\nInitial candidates:")
        board.display_candidates()
        
        if self.verbose:
            print("\nStarting solving process...")
        else:
            print("\nStarting to solve...")
    
    def log_strategy_found(self, strategy_name: str, details: Any = None):
        """Log when a strategy is found."""
        # Track strategy usage
        self.strategies_used.append(strategy_name)
        if strategy_name not in self.strategy_counts:
            self.strategy_counts[strategy_name] = 0
        self.strategy_counts[strategy_name] += 1
        
        
        if self.verbose:
            print(f"Found strategy: {strategy_name}")
    
    def log_strategy_applied(self, strategy_name: str, updates: List, update_type: str = None):
        """Log when a strategy is applied.
        
        Args:
            strategy_name: Name of the strategy applied
            updates: List of updates made (row, col, value) tuples
            update_type: Type of update - "elimination" or "insertion"
        """
        # Both verbose and non-verbose show strategy applied
        if update_type:
            self.step_counter += 1
            if update_type == "elimination":
                formatted_updates = [f"Candidate {val} from ({row}, {col})" for row, col, val in updates]
                print(f"Applied {strategy_name}: Eliminated {len(updates)} candidates")
                for update in formatted_updates:
                    print(f"  {update}")

            else:  # insertion
                formatted_updates = [f"Value {val} at ({row}, {col})" for row, col, val in updates]
                print(f"Applied {strategy_name}: Inserted {len(updates)} values")
                # List all insertions even in non-verbose mode as they're important
                for update in formatted_updates:
                    print(f"  {update}")
        else:
            # Fallback for backward compatibility
            print(f"Applied {strategy_name}: {updates}")
        
        # Only verbose mode shows board after each step
        if self.verbose and self.current_board:
            print("\nBoard after strategy:")
            self.current_board.display_board()
            print("\nCandidates after strategy:")
            self.current_board.display_candidates()
    
    def log_state_change(self, state: str, board):
        """Log when the state machine changes state."""
        if self.verbose:
            print(f"\nState Machine: Current state = {state}")
            print(f"Board valid: {board.is_valid()}")
            print(f"Board solved: {board.is_solved()}")
            print(f"Empty cells: {sum(1 for row in board.cells for cell in row if cell is None)}")
    
    def log_strategy_testing(self, strategy_name: str):
        """Log when a strategy is being tested."""
        if self.verbose:
            print(f"- Testing {strategy_name}...")
    
    def log_strategy_not_found(self, strategy_name: str):
        """Log when a strategy doesn't find any opportunities."""
        if self.verbose:
            print(f"  No opportunities found for {strategy_name}")
    
    def log_no_strategies_found(self):
        """Log when no strategies are found."""
        if self.verbose:
            print("No applicable strategies found")
        else:
            print("No more strategies can be applied")
    
    def log_solve_check(self, is_solved: bool):
        """Log the result of checking if the puzzle is solved."""
        if self.verbose:
            print(f"Checking if solved: {is_solved}")
    
    def log_final_state(self, board, solved: bool):
        """Log the final state of the board."""
        # Always show final board in both modes
        print("\nFinal board:")
        board.display_board()
        print("\nFinal candidates:")
        board.display_candidates()
        
        print(f"\nPuzzle {'solved' if solved else 'not solved'}")
        if not solved:
            print(f"Remaining empty cells: {sum(1 for row in board.cells for cell in row if cell is None)}")
    
    def print_summary(self):
        """Print a summary of the solving process."""
        print("\n===== Solving Summary =====")
        print(f"Total strategies applied: {self.step_counter}")
        
        if self.strategies_used:
            print("\nStrategies used by frequency:")
            # Sort strategies by frequency
            sorted_strategies = sorted(
                self.strategy_counts.items(), 
                key=lambda x: x[1], 
                reverse=True
            )
            for strategy, count in sorted_strategies:
                print(f"- {strategy}: {count} times")
            

            print("\nStrategies used in order:")
            for i, strategy in enumerate(self.strategies_used, 1):
                print(f"{i}. {strategy}")
        else:
                print("No strategies were applied") 