from typing import List, Optional, Set, Tuple
from itertools import product
from board.board import Board
from strategies.strategy import Strategy

class XYZWingStrategy(Strategy):
    """XYZ-Wing technique for candidate elimination."""

    def __init__(self, board: Board) -> None:
        super().__init__(board, name="XYZ-Wing Strategy", type="Candidate Eliminator")

    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        tri_cells = [(r, c, self.board.candidates[r][c])
                     for r in range(9) for c in range(9)
                     if self.board.cells[r][c] is None and len(self.board.candidates[r][c]) == 3]
        for pivot_row, pivot_col, pivot_cands in tri_cells:
            wings = self._find_wings(pivot_row, pivot_col, pivot_cands)
            for i in range(len(wings)):
                for j in range(i + 1, len(wings)):
                    w1 = wings[i]
                    w2 = wings[j]
                    if w1[0:2] == w2[0:2]:
                        continue
                    if not self._is_valid_xyz(pivot_cands, w1[2], w2[2]):
                        continue
                    elim_candidate = (w1[2] & w2[2]).pop()
                    eliminations = self._find_eliminations(w1[0:2], w2[0:2], elim_candidate)
                    if eliminations:
                        return eliminations
        return None

    def _find_wings(self, row: int, col: int, pivot_cands: Set[int]) -> List[Tuple[int, int, Set[int]]]:
        wings = []
        for r in range(9):
            for c in range(9):
                if (r, c) == (row, col):
                    continue
                if self.board.cells[r][c] is not None:
                    continue
                cands = self.board.candidates[r][c]
                if len(cands) == 2 and cands.issubset(pivot_cands):
                    if self._cells_can_see_each_other((row, col), (r, c)):
                        wings.append((r, c, cands.copy()))
        return wings

    def _is_valid_xyz(self, pivot_cands: Set[int], wing1: Set[int], wing2: Set[int]) -> bool:
        union = wing1 | wing2 | pivot_cands
        if union != pivot_cands:
            return False
        if len(wing1 & wing2) != 1:
            return False
        return True

    def _cells_can_see_each_other(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        if a[0] == b[0] or a[1] == b[1]:
            return True
        return a[0] // 3 == b[0] // 3 and a[1] // 3 == b[1] // 3

    def _find_eliminations(self, wing1: Tuple[int, int], wing2: Tuple[int, int], candidate: int) -> Optional[List[Tuple[int, int, int]]]:
        eliminations = []
        for r in range(9):
            for c in range(9):
                if (r, c) in [wing1, wing2]:
                    continue
                if (self._cells_can_see_each_other((r, c), wing1) and
                        self._cells_can_see_each_other((r, c), wing2)):
                    if self.board.cells[r][c] is None and candidate in self.board.candidates[r][c]:
                        eliminations.append((r, c, candidate))
        return eliminations if eliminations else None
