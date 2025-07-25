from typing import List, Optional, Tuple
from board.board import Board
from strategies.strategy import Strategy

class BUGStrategy(Strategy):
    """Basic BUG+1 strategy to resolve bivalue universal grave situations."""

    def __init__(self, board: Board) -> None:
        super().__init__(board, name="BUG Strategy", type="Value Finder")

    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        unsolved = [(r, c) for r in range(9) for c in range(9) if self.board.cells[r][c] is None]
        non_bi = [cell for cell in unsolved if len(self.board.candidates[cell[0]][cell[1]]) != 2]
        if len(non_bi) != 1:
            return None

        row, col = non_bi[0]
        candidates = self.board.candidates[row][col]
        for value in candidates:
            if self._candidate_unique_in_unit(row, col, value):
                return [(row, col, value)]
        return None

    def _candidate_unique_in_unit(self, row: int, col: int, value: int) -> bool:
        row_count = sum(1 for c in range(9) if value in self.board.candidates[row][c])
        if row_count == 1:
            return True
        col_count = sum(1 for r in range(9) if value in self.board.candidates[r][col])
        if col_count == 1:
            return True
        br = (row // 3) * 3
        bc = (col // 3) * 3
        box_count = 0
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                if value in self.board.candidates[r][c]:
                    box_count += 1
        return box_count == 1
