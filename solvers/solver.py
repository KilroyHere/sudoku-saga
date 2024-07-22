class Solver:

  def __init__(self, board, mode = "Default"):
    self.modeSet = {"Default", "Verbose"}
    self.board = board

    if mode in self.modeSet:
        self.mode = mode
    else:
       self.mode = "Default"

  def display(self, str):
    if(self.mode == "Verbose"):
      print(str)
    else:
      pass