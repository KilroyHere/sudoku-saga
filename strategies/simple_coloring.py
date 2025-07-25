from typing import Dict, List, Optional, Set, Tuple
from collections import defaultdict, deque
from board.board import Board
from strategies.strategy import Strategy

class SimpleColoringStrategy(Strategy):
    """Simple Coloring technique for candidate elimination."""

    def __init__(self, board: Board) -> None:
        super().__init__(board, name="Simple Coloring Strategy", type="Candidate Eliminator")

    def process(self) -> Optional[List[Tuple[int, int, int]]]:
        for candidate in range(1, 10):
            links = self._find_strong_links(candidate)
            components = self._color_components(links)
            for color_map in components:
                eliminations = self._check_contradiction(candidate, color_map)
                if eliminations:
                    return eliminations
        return None

    def _find_strong_links(self, candidate: int) -> Dict[Tuple[int, int], Set[Tuple[int, int]]]:
        links: Dict[Tuple[int, int], Set[Tuple[int, int]]] = defaultdict(set)

        # Rows and columns
        for i in range(9):
            row_cells = [(i, c) for c in range(9)
                         if self.board.cells[i][c] is None and candidate in self.board.candidates[i][c]]
            if len(row_cells) == 2:
                a, b = row_cells
                links[a].add(b)
                links[b].add(a)

            col_cells = [(r, i) for r in range(9)
                         if self.board.cells[r][i] is None and candidate in self.board.candidates[r][i]]
            if len(col_cells) == 2:
                a, b = col_cells
                links[a].add(b)
                links[b].add(a)

        # Boxes
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                box_cells = []
                for r in range(br, br + 3):
                    for c in range(bc, bc + 3):
                        if self.board.cells[r][c] is None and candidate in self.board.candidates[r][c]:
                            box_cells.append((r, c))
                if len(box_cells) == 2:
                    a, b = box_cells
                    links[a].add(b)
                    links[b].add(a)
        return links

    def _color_components(self, links: Dict[Tuple[int, int], Set[Tuple[int, int]]]) -> List[Dict[Tuple[int, int], bool]]:
        visited: Set[Tuple[int, int]] = set()
        components: List[Dict[Tuple[int, int], bool]] = []

        for cell in links:
            if cell in visited:
                continue
            comp: Dict[Tuple[int, int], bool] = {}
            queue = deque([(cell, True)])
            while queue:
                current, color = queue.popleft()
                if current in comp:
                    continue
                comp[current] = color
                visited.add(current)
                for neighbor in links.get(current, set()):
                    if neighbor not in comp:
                        queue.append((neighbor, not color))
            components.append(comp)
        return components

    def _cells_share_unit(self, a: Tuple[int, int], b: Tuple[int, int]) -> bool:
        if a[0] == b[0] or a[1] == b[1]:
            return True
        return a[0] // 3 == b[0] // 3 and a[1] // 3 == b[1] // 3

    def _check_contradiction(self, candidate: int, color_map: Dict[Tuple[int, int], bool]) -> Optional[List[Tuple[int, int, int]]]:
        for color in [True, False]:
            cells = [cell for cell, col in color_map.items() if col == color]
            for i in range(len(cells)):
                for j in range(i + 1, len(cells)):
                    if self._cells_share_unit(cells[i], cells[j]):
                        # Contradiction found, eliminate candidate from opposite color
                        elim_color = not color
                        eliminations = []
                        for cell, col in color_map.items():
                            if col == elim_color:
                                r, c = cell
                                if candidate in self.board.candidates[r][c]:
                                    eliminations.append((r, c, candidate))
                        return eliminations if eliminations else None
        return None
