class Validator:

  def __init__(self):
    pass

  def validate(self, board):
    """Checks if the current board state is a valid Sudoku."""

    def is_valid_group(group):
      """Check if a group (row, column, or 3x3 box) is valid."""
      values = [num for num in group if num is not None]
      return len(values) == len(set(values))

    # Check rows
    for row in board:
      if not is_valid_group(row):
        return False

    # Check columns
    for col in range(9):
      if not is_valid_group([board[row][col] for row in range(9)]):
        return False

    # Check 3x3 boxes
    for box_row in range(0, 9, 3):
      for box_col in range(0, 9, 3):
        box_values = [
            board[box_row + r][box_col + c] for r in range(3) for c in range(3)
        ]
        if not is_valid_group(box_values):
          return False

    return True
