from typing import Optional, Dict, Any

from board.board import Board
from solvers.solver_factory import SolverFactory
from solvers.strategic_solver import StrategicSolver
from sudoku.sudoku import Sudoku
from sudoku.logger import SudokuLogger


class SolverUtil:
    """Utility class for solving Sudoku puzzles."""

    @staticmethod
    def create_solver(board: Board, solver_type: str = "Strategic", mode: str = "Default") -> Any:
        """Create a solver instance with the specified type and mode."""
        return SolverFactory.create_solver(board, solverType=solver_type, mode=mode)

    @staticmethod
    def solve_puzzle(
        puzzle_str: str,
        verbose: bool = False,
        description: str = "",
        solver_type: str = "Strategic",
        logger: Optional[SudokuLogger] = None,
    ) -> Dict[str, Any]:
        """Solve a single puzzle and return detailed results."""
        try:
            if description:
                print(f"\nSolving puzzle: {description}")
            if verbose:
                print(f"Puzzle string: {puzzle_str}")

            board = Board(puzzle_str)
            solver = SolverUtil.create_solver(board, mode="Default", solver_type=solver_type)

            if logger is None:
                logger = SudokuLogger(verbose=verbose)
            else:
                logger.verbose = verbose

            if isinstance(solver, StrategicSolver):
                solver.logger = logger

            sudoku = Sudoku(board, solver, logger)
            solved = sudoku.solve()

            if isinstance(solver, StrategicSolver) and hasattr(logger, "print_summary"):
                logger.print_summary()
            elif not isinstance(solver, StrategicSolver):
                board.display_board()

            return {
                "solved": solved,
                "board": board,
                "strategies_used": logger.strategies_used,
                "empty_cells": sum(1 for row in board.cells for cell in row if cell is None),
                "logger": logger,
            }
        except Exception as e:
            print(f"\nError solving puzzle {description}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            raise

