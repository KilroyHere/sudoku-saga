# main.py
from sudoku import Sudoku
from board.board import Board 
from solvers.solver_factory import SolverFactory
from solvers.backtracking_solver import BacktrackingSolver

def main():
    # Example Sudoku puzzle string
    # This string represents one of the easiest boards
    board_string = "300967001040302080020000070070000090000873000500010003004705100905000207800621004"
    # Create the Board
    board = Board(board_string)
    # Create the Solver
    # solver  = SolverFactory().create_solver(board, solverType="Backtracking")
    solver = SolverFactory().create_solver(board, solverType="Strategic")
    # Create Sudoku Game
    sudoku = Sudoku(board, solver)
    # Solve The Sudoku 
    sudoku.board.display_board()
    sudoku.solve()
    sudoku.board.display_board()
    
if __name__ == "__main__":
    main()



