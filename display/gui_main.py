import sys
import os
import argparse

# Ensure the project root is on the path when running directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from display.gui_display import SudokuGUIDisplay, SudokuGUILogger
from sudoku.solver_util import SolverUtil


def main() -> None:
    """Launch the Sudoku GUI visualization."""
    parser = argparse.ArgumentParser(description="Sudoku Solver Visualization")
    parser.add_argument(
        "-p",
        "--puzzle",
        type=str,
        default="000000000001900500560310090100600028004000700270004003040068035002005900000000000",
        help="Sudoku puzzle string (81 characters, 0 for empty cells)",
    )
    parser.add_argument("-d", "--description", type=str, default="", help="Description of the puzzle")
    parser.add_argument(
        "-s",
        "--solver",
        type=str,
        default="Strategic",
        choices=["Strategic", "Backtracking"],
        help="Solver type to use",
    )
    args = parser.parse_args()

    logger = SudokuGUILogger(verbose=True)
    result = SolverUtil.solve_puzzle(
        args.puzzle,
        verbose=True,
        description=args.description,
        solver_type=args.solver,
        logger=logger,
    )
    board = result["board"]
    display = SudokuGUIDisplay(board, logger)
    display.run()
    display.close()


if __name__ == "__main__":
    main()
