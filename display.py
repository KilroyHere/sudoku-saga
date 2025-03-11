import pygame
from typing import List, Tuple

# Constants for the display
WINDOW_SIZE = 600
GRID_SIZE = 9
CELL_SIZE = WINDOW_SIZE // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

class SudokuDisplay:
    def __init__(self, board: List[List[int]]) -> None:
        """
        Initialize the display with the given Sudoku board.

        Args:
            board (List[List[int]]): The Sudoku board to display
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption('Sudoku Solver')
        self.board = board

    def draw_grid(self) -> None:
        """Draw the Sudoku grid lines."""
        for x in range(0, WINDOW_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, WINDOW_SIZE))
            pygame.draw.line(self.screen, GRAY, (0, x), (WINDOW_SIZE, x))

        # Draw thicker lines for the 3x3 boxes
        for x in range(0, WINDOW_SIZE, CELL_SIZE * 3):
            pygame.draw.line(self.screen, BLACK, (x, 0), (x, WINDOW_SIZE), 3)
            pygame.draw.line(self.screen, BLACK, (0, x), (WINDOW_SIZE, x), 3)

    def draw_numbers(self) -> None:
        """Draw the numbers on the Sudoku board."""
        font = pygame.font.Font(None, 36)
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                num = self.board[row][col]
                if num != 0:
                    text = font.render(str(num), True, BLUE)
                    self.screen.blit(text, (col * CELL_SIZE + 15, row * CELL_SIZE + 10))

    def update_display(self) -> None:
        """Update the display with the current board state."""
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_numbers()
        pygame.display.flip()

    def close(self) -> None:
        """Close the pygame display."""
        pygame.quit()

# Example usage
if __name__ == '__main__':
    example_board = [
        [3, 0, 9, 0, 0, 0, 4, 0, 0],
        [2, 0, 0, 7, 0, 9, 0, 0, 0],
        [0, 8, 7, 0, 0, 0, 0, 0, 0],
        [7, 5, 0, 0, 6, 0, 2, 3, 0],
        [6, 0, 0, 9, 0, 4, 0, 0, 8],
        [0, 2, 8, 0, 5, 0, 0, 4, 1],
        [0, 0, 0, 0, 0, 0, 0, 9, 6],
        [0, 0, 0, 1, 0, 0, 0, 0, 7],
        [8, 0, 0, 0, 0, 0, 1, 0, 4]
    ]
    display = SudokuDisplay(example_board)
    display.update_display()
    pygame.time.wait(5000)  # Display for 5 seconds
    display.close() 