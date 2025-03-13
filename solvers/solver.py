class Solver:

    def __init__(self, board, mode = "Default"):
        self.modeSet = {"Default", "Verbose"}
        self.board = board
        self.strategies_used = []  # Track strategies used during solving

        if mode in self.modeSet:
            self.mode = mode
        else:
            self.mode = "Default"

    def display(self, str):
        if(self.mode == "Verbose"):
            print(str)



    def get_strategies_used(self):
        """Return list of strategies used during solving."""
        return self.strategies_used.copy()

    def clear_strategies_used(self):
        """Clear the list of strategies used."""
        self.strategies_used = []

    def find_strategy(self):
        # This method is not provided in the original file or the code block
        # It's assumed to exist as it's called in the find_strategy method
        pass

  