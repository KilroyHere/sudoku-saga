from strategies.strategy import Strategy

'''
This strategy effectively handles various scenarios where a cell's value can 
be conclusively determined by following the 3 basic rules:
Set(1..9) in a row 
Set(1..9) in a column 
Set(1..9) in a box

Thus making it the only strategy where values are placed.
All other strategies work towards eliminating candidates until one remains.

Reference: https://www.sudokuwiki.org/Getting_Started    
'''

class SingleCandidateStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="Single Candidate Strategy", type="Value Finder")


    
    def process(self):
        values_to_insert = []
        for row in range(9):
            for col in range(9):
                if self.board.cells[row][col] is None:
                    possible_values = self.board.candidates[row][col]
                    if len(possible_values) == 1:
                        values_to_insert.append((row, col, possible_values.pop()))
        return values_to_insert
    