from strategies.strategy import Strategy
from itertools import combinations

'''
This strategy identifies hidden triples in a unit (row, column, or box).
A hidden triple occurs when three candidates appear in only three cells within a unit,
and these cells may contain other candidates.

For example, if in a row, the numbers 4,7,9 only appear in three cells
(even though these cells may have other candidates), then 4,7,9 must go in these cells,
and all other candidates can be eliminated from these cells.

This is a candidate eliminator strategy, where candidates are removed based on pattern analysis.

Reference: https://www.sudokuwiki.org/Hidden_Candidates#HT
'''

class HiddenTriplesStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Hidden Triples Strategy", type="Candidate Eliminator")
    
    def process(self):
        """
        Find hidden triples in rows, columns, and boxes.
        A hidden triple is when three candidates appear in only three cells within a unit.
        We can then eliminate all other candidates from these cells.
        """
        eliminations = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if less than 3 empty cells
                if len(empty_cells) < 3:
                    continue
                
                # Create a map of candidates to cells they appear in
                candidate_locations = {i: [] for i in range(1, 10)}
                for row, col in empty_cells:
                    for candidate in self.board.candidates[row][col]:
                        candidate_locations[candidate].append((row, col))
                
                # Find candidates that appear in 2 or 3 cells
                potential_candidates = []
                for candidate, locations in candidate_locations.items():
                    if 2 <= len(locations) <= 3:
                        potential_candidates.append((candidate, frozenset(locations)))
                
                # Check all possible combinations of three candidates
                for cands in combinations(potential_candidates, 3):
                    # Get all cells where these candidates appear
                    all_cells = set()
                    for _, locs in cands:
                        all_cells.update(locs)
                    
                    # If these candidates appear in exactly three cells
                    if len(all_cells) == 3:
                        # Get the three candidates
                        triple = {cand for cand, _ in cands}
                        
                        # Remove all other candidates from these cells
                        found_elimination = False
                        for row, col in all_cells:
                            for candidate in list(self.board.candidates[row][col]):
                                if candidate not in triple:
                                    eliminations.append((row, col, candidate))
                                    found_elimination = True
                        
                        if found_elimination:
                            return eliminations  # Return as soon as we find a useful triple
        
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