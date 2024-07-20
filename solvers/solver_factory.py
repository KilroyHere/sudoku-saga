from solvers.backtracking_solver import BacktrackingSolver
from solvers.validator import Validator

class SolverFactory:
    @staticmethod
    def create_solver( solverType="Backtracking", mode="Default"):
        # Create and return an instance of BacktrackingSolver
        validator = Validator()
        match solverType:
            case "Backtracking":
                return BacktrackingSolver(validator, mode)
            case _:
                return BacktrackingSolver(validator, mode)