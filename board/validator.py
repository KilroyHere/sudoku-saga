class Validator:

  def __init__(self):
    self
  
 
  def is_solved(self, cells):
    if any(value is None for row in cells for value in row):
      return False
    else:
      return True

 
  def check_placement(self, num, row_nums, col_nums, box_nums):
      """Check if placing num at board[row][col] is valid."""
      if num in row_nums:
          return False
      if num in col_nums:
          return False
      if num in box_nums:
          return False
      return True


  def validate(self, cells):
    """Checks if the current board state is a valid Sudoku."""

    def is_valid_group(group):
      """Check if a group (row, column, or 3x3 box) is valid."""
      values = [num for num in group if num is not None]
      return len(values) == len(set(values))

    # Check rows
    for row in cells:
      if not is_valid_group(row):
        return False

    # Check columns
    for col in range(9):
      if not is_valid_group([cells[row][col] for row in range(9)]):
        return False

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
      for box_col in range(0, 9, 3):
        box_values = [
            cells[box_row + r][box_col + c] for r in range(3) for c in range(3)
        ]
        if not is_valid_group(box_values):
          return False

    return True