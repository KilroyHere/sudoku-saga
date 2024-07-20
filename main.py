# main.py

from sudoku import Sudoku
from board import Board 
from backtracking_solver import BacktrackingSolver
from validator import Validator

def main():
    # Example Sudoku puzzle string
    board_string = "000705306035040781007030050041000008063000120500000437000070000978050010350201070"
    # Create auxillary objects
    solver = BacktrackingSolver()
    board = Board(board_string)
    validator = Validator()
    
    sudoku = Sudoku(board, solver, validator)

    # Print the Sudoku board
    sudoku.board.display_board()
    sudoku.board.display_candidates()

if __name__ == "__main__":
    main()



