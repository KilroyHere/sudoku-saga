from strategies.strategy import Strategy
from itertools import combinations

'''
This strategy identifies naked triples in a unit (row, column, or box).
A naked triple occurs when three cells in a unit collectively contain only three candidates.
Each cell must contain 2 or 3 of these candidates. When found, these three candidates
can be eliminated from all other cells in that unit.

For example, if three cells in a row contain only the numbers [4,5,6] between them
(like [4,5], [5,6], [4,5,6]), then 4,5,6 cannot appear in any other cell in that row.

This is a candidate eliminator strategy, where candidates are removed based on pattern analysis.

Reference: https://www.sudokuwiki.org/Naked_Candidates#NTs
'''

class NakedTriplesStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Naked Triples Strategy", type="Candidate Eliminator")
    
    def process(self):
        """
        Find naked triples in rows, columns, and boxes.
        A naked triple is when three cells in a unit collectively contain only three candidates.
        We can then eliminate these candidates from other cells in the same unit.
        """
        eliminations = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Find cells with 2 or 3 candidates
                potential_cells = []
                for cell in empty_cells:
                    row, col = cell
                    candidates = self.board.candidates[row][col]
                    if 2 <= len(candidates) <= 3:
                        potential_cells.append((row, col, frozenset(candidates)))
                
                # Check all possible combinations of three cells
                for cells in combinations(potential_cells, 3):
                    # Get union of all candidates in these three cells
                    all_candidates = set()
                    for _, _, cands in cells:
                        all_candidates.update(cands)
                    
                    # If we found a naked triple (exactly three candidates total)
                    if len(all_candidates) == 3:
                        triple_cells = [(row, col) for row, col, _ in cells]
                        
                        # Remove these candidates from other cells in the unit
                        other_cells = [cell for cell in empty_cells 
                                     if cell not in triple_cells]
                        
                        found_elimination = False
                        for row, col in other_cells:
                            for candidate in all_candidates:
                                if candidate in self.board.candidates[row][col]:
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