from solvers.solver import Solver
class StrategicSolver(Solver):
    def __init__(self, mode = "Default"):
        super().__init__(mode)
    
    def is_strategy_based(self):
        return True


    def find_strategy(self):
        """
        Determines the best strategy to apply next. This method should be 
        implemented by subclasses to return the strategy information.

        Returns:
            tuple: A tuple containing a boolean indicating if a strategy was found
                   and the best strategy to apply.
        """
        raise NotImplementedError("Yet to Implement.")
    
    def insert_values(self):
        """
        Inserts values into the board based on the chosen strategy. This method
        should be implemented by subclasses to update the board.

        Returns:
            list: A list of values inserted into the board, with row, col Information.
        """
        raise NotImplementedError("Yet to Implement.")
    
