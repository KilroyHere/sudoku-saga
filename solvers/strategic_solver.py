from solvers.solver import Solver
from strategies.single_candidate import SingleCandidateStrategy
class StrategicSolver(Solver):
    def __init__(self, board, mode = "Default"):
        super().__init__(board, mode)
        self.strategies = [
            SingleCandidateStrategy(self.board)
        ]
        # State storing variables
        self.current_strategy = None
        self.values_to_insert = []
        self.candidates_to_eliminate = []
    
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
        self.current_strategy = None
        for strategy in self.strategies:
            result = strategy.process()
            if(result):
                self.current_strategy = strategy
                self.display("Found Strategy: "+self.current_strategy.name)
                match (self.current_strategy.type):
                    case "Value Finder":
                        self.values_to_insert = result
                    case "Candidate Eliminator":
                        self.candidates_to_eliminate = result
                    case _:
                        pass
                break
 
        if(result):
            return (True, self.current_strategy.name)
        else:
            return (False, "None")
    
    def apply_strategy(self):
        """
        Either eliminates candidates or inserts values dependant on the strategy.

        Returns:
            list: A list of values inserted into the board, with row, col Information.
        """
        updates = []
        if(self.current_strategy):
            if(self.candidates_to_eliminate):
                self._eliminate_candidates()
                updates = self.candidates_to_eliminate
                self.candidates_to_eliminate = []
            elif(self.values_to_insert):
                self._insert_values()
                updates = self.values_to_insert
                self.values_to_insert = []
        return updates
            
    def _eliminate_candidates(self):
        pass
    
    def _insert_values(self):
        for value in self.values_to_insert:
            row,col,num = value
            self.board.cells[row][col] = num
            self.board.update_candidates_on_insert(row,col)

    
