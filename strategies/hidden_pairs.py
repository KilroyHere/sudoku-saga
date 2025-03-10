from strategies.strategy import Strategy
from itertools import combinations

'''
This strategy identifies hidden pairs in a unit (row, column, or box).
A hidden pair occurs when two candidates appear in only two cells within a unit,
and these cells may contain other candidates.

For example, if in a row, the numbers 4,7 only appear in two cells
(even though these cells may have other candidates), then 4 and 7 must go in these cells,
and all other candidates can be eliminated from these cells.

This is a candidate eliminator strategy, where candidates are removed based on pattern analysis.

Reference: https://www.sudokuwiki.org/Hidden_Candidates#HP
'''

class HiddenPairsStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Hidden Pairs Strategy", type="Candidate Eliminator")
    
    def process(self):
        """
        Find hidden pairs in rows, columns, and boxes.
        A hidden pair is when two candidates appear in only two cells within a unit.
        We can then eliminate all other candidates from these cells.
        """
        eliminations = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if less than 2 empty cells
                if len(empty_cells) < 2:
                    continue
                
                # Create a map of candidates to cells they appear in
                candidate_locations = {i: [] for i in range(1, 10)}
                for row, col in empty_cells:
                    for candidate in self.board.candidates[row][col]:
                        candidate_locations[candidate].append((row, col))
                
                # Find candidates that appear in exactly 2 cells
                pairs = []
                for candidate, locations in candidate_locations.items():
                    if len(locations) == 2:
                        pairs.append((candidate, frozenset(locations)))
                
                # Check all possible combinations of two candidates
                for (cand1, locs1), (cand2, locs2) in combinations(pairs, 2):
                    # If both candidates appear in the same two cells
                    if locs1 == locs2:
                        # Get the two cells
                        cells = list(locs1)
                        pair = {cand1, cand2}
                        
                        # Remove all other candidates from these cells
                        found_elimination = False
                        for row, col in cells:
                            for candidate in list(self.board.candidates[row][col]):
                                if candidate not in pair:
                                    eliminations.append((row, col, candidate))
                                    found_elimination = True
                        
                        if found_elimination:
                            return eliminations  # Return as soon as we find a useful pair
        
        return None if not eliminations else eliminations

    def _get_empty_cells_in_unit(self, unit_type, index):
        """
        Get all empty cells in a given unit (row, column, or box).
        
        Args:
            unit_type (str): Type of unit ('row', 'column', or 'box')
            index (int): Index of the unit (0-8)
            
        Returns:
            list: List of (row, col) tuples representing empty cells
        """
        empty_cells = []
        if unit_type == 'row':
            for col in range(9):
                if self.board.cells[index][col] is None:
                    empty_cells.append((index, col))
        elif unit_type == 'column':
            for row in range(9):
                if self.board.cells[row][index] is None:
                    empty_cells.append((row, index))
        else:  # box
            box_row, box_col = (index // 3) * 3, (index % 3) * 3
            for i in range(3):
                for j in range(3):
                    row, col = box_row + i, box_col + j
                    if self.board.cells[row][col] is None:
                        empty_cells.append((row, col))
        return empty_cells 