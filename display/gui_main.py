import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import from absolute paths
from board.board import Board
from sudoku.solver_util import SolverUtil
from sudoku.sudoku import Sudoku
# Import the GUI display classes directly
from display.gui_display import SudokuGUIDisplay, SudokuGUILogger
import argparse

def main():
    """
    Main function to run the Sudoku GUI visualization.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Sudoku Solver Visualization')
    parser.add_argument('-p', '--puzzle', type=str, 
                        default="000000000001900500560310090100600028004000700270004003040068035002005900000000000",
                        help='Sudoku puzzle string (81 characters, 0 for empty cells)')
    parser.add_argument('-d', '--description', type=str, default="",
                        help='Description of the puzzle')
    parser.add_argument('-s', '--solver', type=str, default="Strategic",
                        choices=["Strategic", "Backtracking"],
                        help='Solver type to use')
    
    args = parser.parse_args()
    
    # Create a board from the puzzle string
    board = Board(args.puzzle)
    
    # Create a GUI logger
    logger = SudokuGUILogger(verbose=True)
    
    # Solve the puzzle using the logger
    solver = SolverUtil.create_solver(board, args.solver, "Default")
    solver.logger = logger
    logger.set_board(board)
    
    # Log the initial state
    logger.log_initial_state(board)
    
    # Create a Sudoku instance and solve it
    sudoku = Sudoku(board, solver, logger)
    sudoku.solve()
    
    # Create and run the GUI display
    display = SudokuGUIDisplay(board, logger)
    display.run()
    display.close()

if __name__ == "__main__":
    main() 