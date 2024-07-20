# main.py

from sudoku import Sudoku
from board import Board 
from solvers.solver_factory import SolverFactory
from solvers.backtracking_solver import BacktrackingSolver

def main():
    # Example Sudoku puzzle string
    board_string = "000705306035040781007030050041000008063000120500000437000070000978050010350201070"
    # Create the Board
    board = Board(board_string)
    # Create the Solver
    solver  = SolverFactory().create_solver(solverType="Backtracking")
    # Create Sudoku Game
    sudoku = Sudoku(board, solver)
    # Solve The Sudoku 
    sudoku.solve()

if __name__ == "__main__":
    main()



