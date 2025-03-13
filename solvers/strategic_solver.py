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
from strategies.x_wing import XWingStrategy
from strategies.swordfish import SwordfishStrategy
from strategies.y_wing import YWingStrategy

class StrategicSolver(Solver):
    def __init__(self, board, mode = "Default", logger=None):
        super().__init__(board, mode)
        self.logger = logger
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
            HiddenQuadsStrategy(self.board),        # Hidden Quads
            XWingStrategy(self.board),              # X-Wing
            SwordfishStrategy(self.board),          # Swordfish
            YWingStrategy(self.board)               # Y-Wing

        ]
        # State storing variables
        self.current_strategy = None
        self.values_to_insert = []
        self.candidates_to_eliminate = []
        self.observers = []  # Keep for backward compatibility
    
    def is_strategy_based(self):
        return True

    def add_observer(self, observer):
        """Add an observer to track solving progress (kept for backward compatibility)."""
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        """Remove an observer from tracking (kept for backward compatibility)."""
        if observer in self.observers:
            self.observers.remove(observer)

    def find_strategy(self):
        """
        Determines the best strategy to apply next.

        Returns:
            tuple: A tuple containing a boolean indicating if a strategy was found
                   and the best strategy to apply.
        """
        self.current_strategy = None
        strategy_found = False
        
        for strategy in self.strategies:
            if self.logger:
                self.logger.log_strategy_testing(strategy.name)
                
            result = strategy.process()
            if result:
                self.current_strategy = strategy
                
                match (self.current_strategy.type):
                    case "Value Finder":
                        self.values_to_insert = result
                    case "Candidate Eliminator":
                        self.candidates_to_eliminate = result
                    case _:
                        pass
                        
                strategy_found = True
                
                if self.logger:
                    details = self.values_to_insert if self.current_strategy.type == "Value Finder" else self.candidates_to_eliminate
                    self.logger.log_strategy_found(self.current_strategy.name, details)
                
                # Notify observers (for backward compatibility)
                for observer in self.observers:
                    if hasattr(observer, 'on_strategy_found'):
                        observer.on_strategy_found(self.current_strategy.name)
                        
                break
            else:
                if self.logger:
                    self.logger.log_strategy_not_found(strategy.name)
 
        if not strategy_found:
            # Notify observers of state change (for backward compatibility)
            for observer in self.observers:
                if hasattr(observer, 'on_state_changed'):
                    observer.on_state_changed("unsolvable", self.board)
        
        return (strategy_found, self.current_strategy.name if strategy_found else "None")
    
    def apply_strategy(self):
        """
        Either eliminates candidates or inserts values dependant on the strategy.

        Returns:
            list: A list of values inserted into the board, with row, col Information.
        """
        updates = []
        update_type = None
        
        if self.current_strategy:
            if self.candidates_to_eliminate:
                update_type = "elimination"
                for row, col, candidate in self.candidates_to_eliminate:
                    if candidate in self.board.candidates[row][col]:
                        self.board.candidates[row][col].remove(candidate)
                updates = self.candidates_to_eliminate
                self.candidates_to_eliminate = []
                
            elif self.values_to_insert:
                update_type = "insertion"
                for row, col, num in self.values_to_insert:
                    self.board.cells[row][col] = num
                    self.board.update_candidates_on_insert(row, col)
                updates = self.values_to_insert
                self.values_to_insert = []
            
            # Store update_type for the state machine to use
            self.last_update_type = update_type
            
            # Notify observers (for backward compatibility)
            for observer in self.observers:
                if hasattr(observer, 'on_strategy_applied'):
                    observer.on_strategy_applied(self.current_strategy.name, updates)
            
            # Check if puzzle is solved
            if self.board.is_solved():
                # Notify observers of state change (for backward compatibility)
                for observer in self.observers:
                    if hasattr(observer, 'on_state_changed'):
                        observer.on_state_changed("solved", self.board)
            elif not self.board.is_valid():
                # Notify observers of state change (for backward compatibility)
                for observer in self.observers:
                    if hasattr(observer, 'on_state_changed'):
                        observer.on_state_changed("invalid", self.board)
        
        return updates
            
    def _eliminate_candidates(self):
        """Eliminates candidates from cells based on the current strategy's findings."""
        for row, col, candidate in self.candidates_to_eliminate:
            if candidate in self.board.candidates[row][col]:
                self.board.candidates[row][col].remove(candidate)
    
    def _insert_values(self):
        """Inserts values into cells based on the current strategy's findings."""
        for value in self.values_to_insert:
            row, col, num = value
            self.board.cells[row][col] = num
            self.board.update_candidates_on_insert(row, col)

    
