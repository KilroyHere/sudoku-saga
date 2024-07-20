from utilities.colors import Colors
import copy

class Board:

  def __init__(self, board_string):
    self.cells = self.string_to_board(board_string)
    self.original = copy.deepcopy(self.cells)
    self.candidates = self.initialize_candidates()
    self.colors = Colors()

    self.update_candidates()

  def string_to_board(self, board_string):
    """Converts a string representation of a Sudoku board to a 2D list."""
    assert len(board_string) == 81, "Illegal Board String"
    assert all(char in '0123456789' for char in board_string), "Illegal Board String"

    board = []
    for i in range(0, len(board_string), 9):
      row = [
          int(char) if char != '0' else None for char in board_string[i:i + 9]
      ]
      board.append(row)
    return board

  def initialize_candidates(self):
    """Initializes the candidates for each cell."""
    candidates = [[
        set(range(1, 10)) if cell is None else set() for cell in row
    ] for row in self.cells]
    return candidates

  def update_candidates(self, updated_row = None, updated_col = None):
    """Updates the candidates for each cell based on the current board state."""
    for row in range(9):
      for col in range(9):
        if self.cells[row][col] is None:
          possible_numbers = set(range(1, 10))
          possible_numbers -= self.get_row_numbers(row)
          possible_numbers -= self.get_col_numbers(col)
          possible_numbers -= self.get_box_numbers(row, col)
          self.candidates[row][col] = possible_numbers
        else:
          self.candidates[row][col] = set()
          

  # Getter Functions ====================================================================

  def get_row(self,row):
    return self.cells[row]
          
  def get_row_numbers(self, row):
    """Returns a set of numbers present in the specified row."""
    return {
        self.cells[row][col]
        for col in range(9) if self.cells[row][col] is not None
    }
  
  def get_col_list(self,col):
    return [row[col] for row in self.cells]

  def get_col_numbers(self, col):
    """Returns a set of numbers present in the specified column."""
    return {
        self.cells[row][col]
        for row in range(9) if self.cells[row][col] is not None
    }

  def get_box_numbers(self, row, col):
    """Returns a set of numbers in the 3x3 box containing the cell at (row, col)."""
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    box_numbers = {
        self.cells[r][c]
        for r in range(box_row_start, box_row_start + 3)
        for c in range(box_col_start, box_col_start + 3)
        if self.cells[r][c] is not None
    }
    return box_numbers
  

  # Display Functions====================================================================

  def display_board(self):
    """Display the board with original values in red"""
    print("+" + "---+" * 9)
    for i, row in enumerate(self.cells):
      formatted_row = []

      for j in range(9):
        cell_value = self.cells[i][j]
        original_value = self.original[i][j]

        if cell_value == original_value and cell_value is not None:
          formatted_value = self.colors.red(str(cell_value))
        else:
          formatted_value = " " if cell_value is None else str(cell_value)

        formatted_row.append(formatted_value)

      print(("|" + " {}   {}   {} |" * 3).format(*formatted_row))

      if i % 3 == 2:
        print("+" + "---+" * 9)
      else:
        print("+" + "   +" * 9)

  def display_candidates(self):
    """TODO: Update to a GUI"""
    row_list = []
    for candidates_row in self.candidates:
      row_list += self.get_candidate_row(candidates_row)

    print("+" + ("═" * 9 + "+") * 9)

    for i, row in enumerate(row_list):
      if (i % 9 == 0 and i != 0):
        print("+" + ("═" * 9 + "+") * 9)
      elif (i % 3 == 0 and i != 0):
        print("+" + ("-" * 9 + "+") * 9)
      row_string = ""
      for j, num in enumerate(row):
        if (j == 0):
          row_string += '‖'
        row_string += " " + str(num) + " "
        if ((j + 1) % 9 == 0):
          row_string += '‖'
        elif ((j + 1) % 3 == 0):
          row_string += '|'
      print(row_string)

    print("+" + ("═" * 9 + "+") * 9)

  def get_candidate_row(self, candidates_row):
    rows = []
    for i in range(3):
      row = []
      for candidates in candidates_row:
        for num in range(i * 3 + 1, i * 3 + 4):
          if num in candidates:
            row.append(num)
          else:
            row.append(" ")
      rows.append(row)
    return rows

