class Solver:
  
  def __init__(self, validator, mode = "Default"):
    self.modeSet = {"Default", "Debug"}
    self.validator = validator
    self.board = None

    if mode in self.modeSet:
        self.mode = mode
    else:
       self.mode = "Default"

  def isStateMachine(self):
    return True
