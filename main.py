# main.py
from sudoku.sudoku import Sudoku
from board.board import Board 
from solvers.solver_factory import SolverFactory
from solvers.backtracking_solver import BacktrackingSolver
from sudoku.solver_util import SolverUtil
import argparse
import sys


def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Solve a Sudoku puzzle using various strategies.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output with detailed solving steps')
    parser.add_argument('-p', '--puzzle', type=str, default="309000400200709000087000000750060230600904008028050041000000590000106007006000104",
                        help='Sudoku puzzle string (81 characters, use 0 or . for empty cells)')
    parser.add_argument('-d', '--description', type=str, default="Sudoku puzzle",
                        help='Description of the puzzle')
    parser.add_argument('-s', '--solver', type=str, default="Strategic",
                        help='Solver type (Strategic or Backtracking)')
    
    args = parser.parse_args()
    
    # Validate the puzzle string
    puzzle_string = args.puzzle.replace('.', '0')  # Allow . as empty cells too
    
    # Validate the solver type
    if args.solver not in ["Strategic", "Backtracking"]:
        print("Invalid solver type. Please use 'Strategic' or 'Backtracking'.")
        sys.exit(1)

    
    # Solve with specified verbosity
    result = SolverUtil.solve_puzzle( puzzle_string, verbose=args.verbose, description=args.description, solver_type=args.solver)
    
    if not result["solved"]:
        print("\nNote: This puzzle requires advanced strategies not yet implemented.")


if __name__ == "__main__":
    main()



