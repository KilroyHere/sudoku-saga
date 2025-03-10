from strategies.strategy import Strategy

'''
This strategy identifies hidden singles in a unit (row, column, or box).
A hidden single occurs when a candidate appears in only one cell within a unit,
even though that cell may have other candidates.

For example, if in a row, the number 4 only appears as a candidate in one cell
(even though that cell may have other candidates like [4,7,9]), then 4 must go in that cell.

This is a value finder strategy, where we place a value when we find a hidden single.

Reference: https://www.sudokuwiki.org/Hidden_Singles
'''

class HiddenSinglesStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Hidden Singles Strategy", type="Value Finder")
    
    def process(self):
        """
        Find hidden singles in rows, columns, and boxes.
        A hidden single is when a candidate appears in only one cell within a unit.
        We can then place that candidate in that cell.
        """
        values_to_insert = []
        
        # Check each unit type (row, column, box)
        for unit_type in ['row', 'column', 'box']:
            # Check each unit index (0-8)
            for unit_index in range(9):
                # Get empty cells in this unit
                empty_cells = self._get_empty_cells_in_unit(unit_type, unit_index)
                
                # Skip if no empty cells
                if not empty_cells:
                    continue
                
                # Create a map of candidates to cells they appear in
                candidate_locations = {i: [] for i in range(1, 10)}
                for row, col in empty_cells:
                    for candidate in self.board.candidates[row][col]:
                        candidate_locations[candidate].append((row, col))
                
                # Check each candidate
                for candidate, locations in candidate_locations.items():
                    # If candidate appears in exactly one cell
                    if len(locations) == 1:
                        row, col = locations[0]
                        # Only add if not already found
                        if (row, col, candidate) not in values_to_insert:
                            values_to_insert.append((row, col, candidate))
                            return values_to_insert  # Return as soon as we find one
        
        return None if not values_to_insert else values_to_insert

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