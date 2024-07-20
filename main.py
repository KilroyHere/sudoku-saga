# main.py
from sudoku import Sudoku
from board import Board 
from solvers.solver_factory import SolverFactory
from solvers.backtracking_solver import BacktrackingSolver

def main():
    # Example Sudoku puzzle string
    board_string = "309000400200709000087000000750060230600904008028050041000000590000106007006000104"
    # Create the Board
    board = Board(board_string)
    # Create the Solver
    solver  = SolverFactory().create_solver(solverType="Backtracking")
    # Create Sudoku Game
    sudoku = Sudoku(board, solver)
    # Solve The Sudoku 
    sudoku.board.display_board()
    sudoku.solve()
    sudoku.board.display_board()
    
if __name__ == "__main__":
    main()



