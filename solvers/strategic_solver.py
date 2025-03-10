from solvers.solver import Solver
from strategies.single_candidate import SingleCandidateStrategy
from strategies.naked_pairs import NakedPairsStrategy
from strategies.naked_triples import NakedTriplesStrategy
from strategies.naked_quads import NakedQuadsStrategy
from strategies.hidden_singles import HiddenSinglesStrategy
from strategies.hidden_pairs import HiddenPairsStrategy
from strategies.hidden_triples import HiddenTriplesStrategy
from strategies.hidden_quads import HiddenQuadsStrategy
from strategies.pointing_pairs import PointingPairsStrategy
from strategies.box_line_intersection import BoxLineIntersectionStrategy

class StrategicSolver(Solver):
    def __init__(self, board, mode = "Default"):
        super().__init__(board, mode)
        # Order strategies from simplest to most complex
        self.strategies = [
            SingleCandidateStrategy(self.board),    # Naked Singles
            HiddenSinglesStrategy(self.board),      # Hidden Singles
            PointingPairsStrategy(self.board),      # Pointing Pairs
            BoxLineIntersectionStrategy(self.board), # Box/Line Intersection
            NakedPairsStrategy(self.board),         # Naked Pairs
            HiddenPairsStrategy(self.board),        # Hidden Pairs
            NakedTriplesStrategy(self.board),       # Naked Triples
            HiddenTriplesStrategy(self.board),      # Hidden Triples
            NakedQuadsStrategy(self.board),         # Naked Quads
            HiddenQuadsStrategy(self.board)         # Hidden Quads
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
        strategy_found = False
        
        self.display("\nTrying strategies in order:")
        for strategy in self.strategies:
            self.display(f"- Testing {strategy.name}...")
            result = strategy.process()
            if result:
                self.current_strategy = strategy
                self.display(f"Found applicable strategy: {self.current_strategy.name}")
                match (self.current_strategy.type):
                    case "Value Finder":
                        self.values_to_insert = result
                        self.display(f"Values to insert: {self.values_to_insert}")
                    case "Candidate Eliminator":
                        self.candidates_to_eliminate = result
                        self.display(f"Candidates to eliminate: {self.candidates_to_eliminate}")
                    case _:
                        pass
                strategy_found = True
                # Track the strategy being used
                self.strategies_used.append(self.current_strategy.name)
                break
            else:
                self.display(f"  No opportunities found for {strategy.name}")
 
        if not strategy_found:
            self.display("No applicable strategies found")
        
        return (strategy_found, self.current_strategy.name if strategy_found else "None")
    
    def apply_strategy(self):
        """
        Either eliminates candidates or inserts values dependant on the strategy.

        Returns:
            list: A list of values inserted into the board, with row, col Information.
        """
        updates = []
        if self.current_strategy:
            if self.candidates_to_eliminate:
                self.display(f"\nApplying {self.current_strategy.name} to eliminate candidates:")
                for row, col, candidate in self.candidates_to_eliminate:
                    if candidate in self.board.candidates[row][col]:
                        self.display(f"  Removing candidate {candidate} from cell ({row}, {col})")
                        self.board.candidates[row][col].remove(candidate)
                updates = self.candidates_to_eliminate
                self.candidates_to_eliminate = []
            elif self.values_to_insert:
                self.display(f"\nApplying {self.current_strategy.name} to insert values:")
                for row, col, num in self.values_to_insert:
                    self.display(f"  Inserting {num} at cell ({row}, {col})")
                    self.board.cells[row][col] = num
                    self.board.update_candidates_on_insert(row, col)
                updates = self.values_to_insert
                self.values_to_insert = []
        return updates
            
    def _eliminate_candidates(self):
        """
        Eliminates candidates from cells based on the current strategy's findings.
        """
        for row, col, candidate in self.candidates_to_eliminate:
            if candidate in self.board.candidates[row][col]:
                self.board.candidates[row][col].remove(candidate)
    
    def _insert_values(self):
        """
        Inserts values into cells based on the current strategy's findings.
        """
        for value in self.values_to_insert:
            row,col,num = value
            self.board.cells[row][col] = num
            self.board.update_candidates_on_insert(row,col)

    
