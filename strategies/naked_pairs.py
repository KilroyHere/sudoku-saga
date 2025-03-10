from strategies.strategy import Strategy
from itertools import combinations

'''
This strategy identifies naked pairs in a unit (row, column, or box).
A naked pair occurs when two cells in a unit have exactly the same two candidates.
When found, these two candidates can be eliminated from all other cells in that unit.

For example, if two cells in a row both have only candidates 4,7, then 4 and 7 
cannot appear in any other cell in that row.

Thus making it a candidate eliminator strategy, where candidates are removed based on pattern analysis.

Reference: https://www.sudokuwiki.org/Naked_Candidates#NPs
'''

class NakedPairsStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Naked Pairs Strategy", type="Candidate Eliminator")
    
    def process(self):
        """
        Find naked pairs in rows, columns, and boxes.
        A naked pair is when two cells in a unit have the exact same two candidates.
        We can then eliminate these candidates from other cells in the same unit.
        """
        eliminations = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Find cells with exactly 2 candidates
                cells_with_two = []
                for cell in empty_cells:
                    row, col = cell
                    candidates = self.board.candidates[row][col]
                    if len(candidates) == 2:
                        cells_with_two.append((row, col, frozenset(candidates)))
                
                # Check all possible pairs of cells
                for cell1, cell2 in combinations(cells_with_two, 2):
                    row1, col1, cands1 = cell1
                    row2, col2, cands2 = cell2
                    
                    # If we found a naked pair (same two candidates)
                    if cands1 == cands2:
                        # Remove these candidates from other cells in the unit
                        other_cells = [cell for cell in empty_cells 
                                     if cell != (row1, col1) and cell != (row2, col2)]
                        
                        found_elimination = False
                        for row, col in other_cells:
                            for candidate in cands1:
                                if candidate in self.board.candidates[row][col]:
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