class Strategy:
    def __init__(self, board, name, type):
        self.board = board
        self._name = name
        self._type = type
    
    @property
    def name(self):
        """Return the strategy name."""
        return self._name
    
    @property
    def type(self):
        """Return the strategy type."""
        return self._type
    
    def process(self):
        """
        Find and return candidates for this strategy. This method should be
        overridden by specific strategy implementations to identify which
        cells or values are relevant for the strategy.
        """ 
        
        raise NotImplementedError("Strategy must implement the process method.")
    