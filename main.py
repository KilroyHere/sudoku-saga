# main.py
from sudoku.sudoku import Sudoku
from board.board import Board 
from solvers.solver_factory import SolverFactory
from solvers.backtracking_solver import BacktrackingSolver

def main():
    # This is a challenging Sudoku puzzle that requires advanced strategies
    # beyond basic techniques like Single Candidates and Hidden Singles
    board_string = "309000400200709000087000000750060230600904008028050041000000590000106007006000104"
    
    # Create the Board
    board = Board(board_string)
    
    # Create the Strategic Solver (using verbose mode to see detailed progress)
    solver = SolverFactory().create_solver(board, solverType="Strategic", mode="Verbose")
    
    # Create Sudoku Game
    sudoku = Sudoku(board, solver)
    
    print("Initial board:")
    sudoku.board.display_board()
    print("\nInitial candidates:")
    sudoku.board.display_candidates()
    
    print("\nAttempting to solve...")
    solved = sudoku.solve()
    
    print("\nFinal board:")
    sudoku.board.display_board()
    print("\nFinal candidates:")
    sudoku.board.display_candidates()
    
    if not solved:
        print("\nNote: This puzzle requires advanced strategies not yet implemented.")
        print("Current strategies available:")
        for strategy in solver.strategies:
            print(f"- {strategy.name}")
    
if __name__ == "__main__":
    main()



