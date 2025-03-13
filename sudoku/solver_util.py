from typing import Optional, List, Dict, Any
from board.board import Board
from solvers.solver_factory import SolverFactory
from solvers.strategic_solver import StrategicSolver
from sudoku.sudoku import Sudoku
import json
from pathlib import Path
from sudoku.logger import SudokuLogger

# Keep SolverObserver for backward compatibility
class SolverObserver():
    """Base observer class for Sudoku solving process"""
    def __init__(self, verbose: bool = False):
        self.step = 1
        self.board = None
        self.verbose = verbose
        self.strategies_used = []
        # Track summary information even in non-verbose mode
        self.total_strategies_applied = 0
        self.strategy_counts = {}
    
    def on_strategy_found(self, strategy_name: str):
        self.strategies_used.append(strategy_name)
        
        # Update strategy counts for summary
        if strategy_name not in self.strategy_counts:
            self.strategy_counts[strategy_name] = 0
        self.strategy_counts[strategy_name] += 1
        
        if self.verbose:
            print(f"\nStep {self.step}: Found strategy: {strategy_name}")
    
    def on_strategy_applied(self, strategy_name: str, updates: List[tuple]):
        self.total_strategies_applied += 1
        
        if self.verbose:
            print(f"Updates made: {updates}")
            # Only try to display the board if it's available
            if self.board is not None:
                print("\nBoard after strategy:")
                self.board.display_board()
                print("\nCandidates after strategy:")
                self.board.display_candidates()
                
                print("\nBoard state:")
                print(f"Is valid: {self.board.is_valid()}")
                print(f"Is solved: {self.board.is_solved()}")
                print(f"Empty cells: {sum(1 for row in self.board.cells for cell in row if cell is None)}")
        
        self.step += 1
    
    def on_state_changed(self, state: str, board: Board):
        self.board = board
        if state == "unsolvable" and self.verbose:
            print("\nNo more strategies found")
    

class SolverUtil:
    """Utility class for solving Sudoku puzzles with various options"""
    
    @staticmethod
    def create_solver(board: Board, solver_type: str = "Strategic", mode: str = "Default") -> Any:
        """Create a solver instance with specified type and mode"""
        return SolverFactory.create_solver(board, solverType=solver_type, mode=mode)
    
    @staticmethod
    def solve_puzzle(puzzle_str: str, verbose: bool = False, description: str = "") -> Dict[str, Any]:
        """
        Solve a single puzzle and return detailed results
        
        Args:
            puzzle_str: The puzzle string to solve
            verbose: Whether to show detailed output
            description: Optional description of the puzzle
            
        Returns:
            Dictionary containing solving results and statistics
        """
        try:
            if description:
                print(f"\nSolving puzzle: {description}")
            
            if verbose:
                print(f"Puzzle string: {puzzle_str}")
            
            # Create board and solver
            board = Board(puzzle_str)
            solver = SolverUtil.create_solver(board, mode="Default")  # Mode doesn't matter now
            
            # Create the centralized logger
            logger = SudokuLogger(verbose=verbose)
            
            # Pass logger to solver if it's a strategic solver
            if isinstance(solver, StrategicSolver):
                solver.logger = logger
            
            # Create Sudoku game with logger
            sudoku = Sudoku(board, solver, logger)
            
            # Solve the puzzle
            solved = sudoku.solve()
            
            # Print summary
            logger.print_summary()
            
            return {
                "solved": solved,
                "board": board,
                "strategies_used": logger.strategies_used,
                "empty_cells": sum(1 for row in board.cells for cell in row if cell is None)
            }
            
        except Exception as e:
            print(f"\nError solving puzzle {description}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            raise 