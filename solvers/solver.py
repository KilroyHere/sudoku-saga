class Solver:
  
  def __init__(self, mode = "Default"):
    self.modeSet = {"Default", "Debug"}
    self.board = None

    if mode in self.modeSet:
        self.mode = mode
    else:
       self.mode = "Default"
