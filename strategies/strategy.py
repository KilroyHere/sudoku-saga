class Strategy:
    def __init__(self, board, name, type):
        self.board = board
        self.name = name
        self.type = type
    
 
    def process(self):
        """
        Find and return candidates for this strategy. This method should be
        overridden by specific strategy implementations to identify which
        cells or values are relevant for the strategy.
        """ 
        
        raise NotImplementedError("Strategy must implement the process method.")
    