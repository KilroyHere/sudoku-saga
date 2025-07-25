from typing import List, Any


class SudokuLogger:
    """Centralized logger for the Sudoku solving process."""

    def __init__(self, verbose: bool = False) -> None:
        self.verbose = verbose
        self.step_counter = 0
        self.strategies_used: List[str] = []
        self.strategy_counts = {}
        self.current_board = None

    def set_board(self, board) -> None:
        """Set the board reference for logging."""
        self.current_board = board

    def log_initial_state(self, board) -> None:
        print("\nInitial board:")
        board.display_board()
        print("\nInitial candidates:")
        board.display_candidates()
        print("\nStarting solving process..." if self.verbose else "\nStarting to solve...")

    def log_strategy_found(self, strategy_name: str, details: Any = None) -> None:
        self.strategies_used.append(strategy_name)
        self.strategy_counts[strategy_name] = self.strategy_counts.get(strategy_name, 0) + 1
        if self.verbose:
            print(f"Found strategy: {strategy_name}")

    def log_strategy_applied(self, strategy_name: str, updates: List, update_type: str | None = None) -> None:
        if update_type:
            self.step_counter += 1
            if update_type == "elimination":
                formatted = [f"Candidate {v} from ({r}, {c})" for r, c, v in updates]
                print(f"Applied {strategy_name}: Eliminated {len(updates)} candidates")
                for text in formatted:
                    print(f"  {text}")
            else:
                formatted = [f"Value {v} at ({r}, {c})" for r, c, v in updates]
                print(f"Applied {strategy_name}: Inserted {len(updates)} values")
                for text in formatted:
                    print(f"  {text}")
        else:
            print(f"Applied {strategy_name}: {updates}")

        if self.verbose and self.current_board:
            print("\nBoard after strategy:")
            self.current_board.display_board()
            print("\nCandidates after strategy:")
            self.current_board.display_candidates()

    def log_state_change(self, state: str, board) -> None:
        if self.verbose:
            print(f"\nState Machine: Current state = {state}")
            print(f"Board valid: {board.is_valid()}")
            print(f"Board solved: {board.is_solved()}")
            print(f"Empty cells: {sum(1 for row in board.cells for cell in row if cell is None)}")

    def log_strategy_testing(self, strategy_name: str) -> None:
        if self.verbose:
            print(f"- Testing {strategy_name}...")

    def log_strategy_not_found(self, strategy_name: str) -> None:
        if self.verbose:
            print(f"  No opportunities found for {strategy_name}")

    def log_no_strategies_found(self) -> None:
        print("No applicable strategies found" if self.verbose else "No more strategies can be applied")

    def log_solve_check(self, is_solved: bool) -> None:
        if self.verbose:
            print(f"Checking if solved: {is_solved}")

    def log_final_state(self, board, solved: bool) -> None:
        print("\nFinal board:")
        board.display_board()
        print("\nFinal candidates:")
        board.display_candidates()
        print(f"\nPuzzle {'solved' if solved else 'not solved'}")
        if not solved:
            print(f"Remaining empty cells: {sum(1 for row in board.cells for cell in row if cell is None)}")

    def print_summary(self) -> None:
        print("\n===== Solving Summary =====")
        print(f"Total strategies applied: {self.step_counter}")
        if self.strategies_used:
            print("\nStrategies used by frequency:")
            for strategy, count in sorted(self.strategy_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"- {strategy}: {count} times")
            print("\nStrategies used in order:")
            for i, strategy in enumerate(self.strategies_used, 1):
                print(f"{i}. {strategy}")
        else:
            print("No strategies were applied")

