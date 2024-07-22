from solvers.backtracking_solver import BacktrackingSolver
from solvers.strategic_solver import StrategicSolver

class SolverFactory:
    @staticmethod
    def create_solver( board, solverType="Backtracking", mode="Default"):
        # Create and return an instance of BacktrackingSolver
        match solverType:
            case "Backtracking":
                print("Creating a Backtracking Solver")
                return BacktrackingSolver(board, mode)
            case "Strategic":
                print("Creating a Strategic Solver")
                return StrategicSolver(board, mode)
            case _:
                print("Creating a Backtracking Solver")
                return BacktrackingSolver(board, mode)