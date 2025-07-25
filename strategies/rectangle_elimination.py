from typing import List, Optional, Tuple, Set
from itertools import combinations
from board.board import Board
from strategies.strategy import Strategy

class RectangleEliminationStrategy(Strategy):
    """Unique Rectangle Type 1 elimination."""

    def __init__(self, board: Board) -> None:
        super().__init__(board, name="Rectangle Elimination Strategy", type="Candidate Eliminator")

    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        for rows in combinations(range(9), 2):
            for cols in combinations(range(9), 2):
                cells = [
                    (rows[0], cols[0]), (rows[0], cols[1]),
                    (rows[1], cols[0]), (rows[1], cols[1])
                ]
                cand_sets = [
                    self.board.candidates[r][c]
                    for r, c in cells
                    if self.board.cells[r][c] is None
                ]
                if len(cand_sets) < 4:
                    continue

                pair_cells = [s for s in cand_sets if len(s) == 2]
                if len(pair_cells) != 3:
                    continue

                if not all(pair_cells[0] == s for s in pair_cells[1:]):
                    continue

                common = pair_cells[0]
                target_idx = next(i for i, s in enumerate(cand_sets) if s != common)
                target = cells[target_idx]
                target_set = self.board.candidates[target[0]][target[1]]

                if common.issubset(target_set) and len(target_set) > 2:
                    eliminations = [(target[0], target[1], val) for val in common]
                    return eliminations
        return None
