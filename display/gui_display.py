import pygame
import time
import sys
import os
from typing import List, Tuple, Dict, Set, Optional

# Add the project root to the path when running this file directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board.board import Board
from sudoku.logger import SudokuLogger

# Constants for the display
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_SIZE = 9
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // GRID_SIZE
CANDIDATE_CELL_SIZE = CELL_SIZE // 3
PADDING = 20
BUTTON_HEIGHT = 40
BUTTON_WIDTH = 150
INFO_PANEL_WIDTH = 500

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
YELLOW = (255, 255, 0)
HIGHLIGHT_COLOR = (255, 255, 200)  # Light yellow for highlighting

class StepInfo:
    """Class to store information about each solving step."""
    def __init__(self, strategy_name: str = "", updates: List = None, 
                 update_type: str = "", board_state: List[List] = None, 
                 candidates: List[List[Set[int]]] = None, description: str = ""):
        self.strategy_name = strategy_name
        self.updates = updates or []
        self.update_type = update_type
        self.board_state = board_state
        self.candidates = candidates
        self.description = description
        self.highlighted_cells = []
        
        # Extract cells to highlight from updates
        if updates:
            self.highlighted_cells = [(row, col) for row, col, _ in updates]

class SudokuGUILogger(SudokuLogger):
    """Extended logger that captures steps for GUI display."""
    
    def __init__(self, verbose: bool = False):
        super().__init__(verbose)
        self.steps = []
        self.current_step = StepInfo(
            strategy_name="Initial State",
            description="Starting board"
        )
    
    def log_initial_state(self, board):
        """Log the initial state of the board."""
        super().log_initial_state(board)
        
        # Capture initial state
        self.current_step.board_state = [row[:] for row in board.cells]
        self.current_step.candidates = [
            [cell.copy() if cell else set() for cell in row] 
            for row in board.candidates
        ]
        self.steps.append(self.current_step)
        
        # Reset for next step
        self.current_step = StepInfo()
    
    def log_strategy_found(self, strategy_name: str, details: any = None):
        """Log when a strategy is found."""
        super().log_strategy_found(strategy_name, details)
        
        self.current_step.strategy_name = strategy_name
        if details:
            self.current_step.description = f"Found {strategy_name}: {details}"
        else:
            self.current_step.description = f"Found {strategy_name}"
    
    def log_strategy_applied(self, strategy_name: str, updates: List, update_type: str = None):
        """Log when a strategy is applied."""
        super().log_strategy_applied(strategy_name, updates, update_type)
        
        # Capture the current state after strategy application
        if self.current_board:
            self.current_step.board_state = [row[:] for row in self.current_board.cells]
            self.current_step.candidates = [
                [cell.copy() if cell else set() for cell in row] 
                for row in self.current_board.candidates
            ]
            self.current_step.updates = updates
            self.current_step.update_type = update_type
            
            # Create description
            if update_type == "elimination":
                self.current_step.description = f"Applied {strategy_name}: Eliminated {len(updates)} candidates"
            elif update_type == "insertion":
                self.current_step.description = f"Applied {strategy_name}: Inserted {len(updates)} values"
            else:
                self.current_step.description = f"Applied {strategy_name}"
            
            # Add step to history
            self.steps.append(self.current_step)
            
            # Reset for next step
            self.current_step = StepInfo()
    
    def log_final_state(self, board, solved: bool):
        """Log the final state of the board."""
        super().log_final_state(board, solved)
        
        # Capture final state
        final_step = StepInfo(
            strategy_name="Final State",
            board_state=[row[:] for row in board.cells],
            candidates=[
                [cell.copy() if cell else set() for cell in row] 
                for row in board.candidates
            ],
            description=f"Puzzle {'solved' if solved else 'not solved'}"
        )
        self.steps.append(final_step)

class SudokuGUIDisplay:
    def __init__(self, board: Board, logger: SudokuGUILogger) -> None:
        """
        Initialize the GUI display with the given Sudoku board and logger.

        Args:
            board (Board): The Sudoku board to display
            logger (SudokuGUILogger): The logger with solving steps
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Sudoku Saga ')
        
        self.board = board
        self.logger = logger
        self.current_step_index = 0
        self.auto_play = False
        self.auto_play_speed = 1.0  # seconds between steps
        self.last_auto_step_time = 0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.number_font = pygame.font.Font(None, 36)
        self.candidate_font = pygame.font.Font(None, 18)
        self.info_font = pygame.font.Font(None, 24)
        self.button_font = pygame.font.Font(None, 24)
        
        # Buttons
        self.buttons = [
            {"text": "Previous", "rect": pygame.Rect(PADDING, WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.previous_step},
            {"text": "Next", "rect": pygame.Rect(PADDING + BUTTON_WIDTH + 10, WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.next_step},
            {"text": "Auto Play", "rect": pygame.Rect(PADDING + (BUTTON_WIDTH + 10) * 2, WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING, BUTTON_WIDTH, BUTTON_HEIGHT), "action": self.toggle_auto_play},
            {"text": "Speed -", "rect": pygame.Rect(PADDING + (BUTTON_WIDTH + 10) * 3, WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING, BUTTON_WIDTH // 2, BUTTON_HEIGHT), "action": self.decrease_speed},
            {"text": "Speed +", "rect": pygame.Rect(PADDING + (BUTTON_WIDTH + 10) * 3 + BUTTON_WIDTH // 2, WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING, BUTTON_WIDTH // 2, BUTTON_HEIGHT), "action": self.increase_speed}
        ]
        
        # Initialize with first step
        if logger.steps:
            self.current_step = logger.steps[0]
        else:
            self.current_step = StepInfo()
    
    def draw_grid(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the Sudoku grid lines."""
        for i in range(0, BOARD_SIZE + 1, CELL_SIZE):
            # Horizontal lines
            line_thickness = 3 if i % (CELL_SIZE * 3) == 0 else 1
            pygame.draw.line(self.screen, BLACK, 
                            (x_offset + 0, y_offset + i), 
                            (x_offset + BOARD_SIZE, y_offset + i), 
                            line_thickness)
            
            # Vertical lines
            pygame.draw.line(self.screen, BLACK, 
                            (x_offset + i, y_offset + 0), 
                            (x_offset + i, y_offset + BOARD_SIZE), 
                            line_thickness)
    
    def draw_numbers(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the numbers on the Sudoku board."""
        if not self.current_step.board_state:
            return
            
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Check if cell should be highlighted
                is_highlighted = (row, col) in self.current_step.highlighted_cells
                if is_highlighted:
                    pygame.draw.rect(self.screen, HIGHLIGHT_COLOR, 
                                    (x_offset + col * CELL_SIZE, y_offset + row * CELL_SIZE, 
                                    CELL_SIZE, CELL_SIZE))
                
                # Draw the number
                num = self.current_step.board_state[row][col]
                if num is not None:
                    # Check if it's an original number (from initial board)
                    is_original = self.board.original[row][col] is not None
                    color = RED if is_original else BLUE
                    
                    text = self.number_font.render(str(num), True, color)
                    text_rect = text.get_rect(center=(x_offset + col * CELL_SIZE + CELL_SIZE // 2, 
                                                    y_offset + row * CELL_SIZE + CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
    
    def draw_candidates(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the candidates for each cell."""
        if not self.current_step.candidates:
            return
            
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Only draw candidates for empty cells
                if self.current_step.board_state[row][col] is None:
                    candidates = self.current_step.candidates[row][col]
                    
                    for num in range(1, 10):
                        # Calculate position within the cell
                        sub_row = (num - 1) // 3
                        sub_col = (num - 1) % 3
                        
                        # Calculate center position for this candidate
                        center_x = x_offset + col * CELL_SIZE + sub_col * CANDIDATE_CELL_SIZE + CANDIDATE_CELL_SIZE // 2
                        center_y = y_offset + row * CELL_SIZE + sub_row * CANDIDATE_CELL_SIZE + CANDIDATE_CELL_SIZE // 2
                        
                        # Draw the candidate if it exists
                        if num in candidates:
                            text = self.candidate_font.render(str(num), True, GRAY)
                            text_rect = text.get_rect(center=(center_x, center_y))
                            self.screen.blit(text, text_rect)
    
    def draw_info_panel(self) -> None:
        """Draw the information panel showing current step details."""
        # Draw panel background
        info_panel_rect = pygame.Rect(BOARD_SIZE + PADDING * 2, PADDING, 
                                     INFO_PANEL_WIDTH, BOARD_SIZE)
        pygame.draw.rect(self.screen, LIGHT_GRAY, info_panel_rect)
        pygame.draw.rect(self.screen, BLACK, info_panel_rect, 2)
        
        # Draw step information
        title_text = self.title_font.render(f"Step {self.current_step_index + 1}/{len(self.logger.steps)}", 
                                          True, BLACK)
        self.screen.blit(title_text, (info_panel_rect.x + 10, info_panel_rect.y + 10))
        
        # Draw strategy name
        strategy_text = self.info_font.render(f"Strategy: {self.current_step.strategy_name}", 
                                            True, BLACK)
        self.screen.blit(strategy_text, (info_panel_rect.x + 10, info_panel_rect.y + 50))
        
        # Draw description
        description_lines = self._wrap_text(self.current_step.description, 
                                          self.info_font, INFO_PANEL_WIDTH - 20)
        for i, line in enumerate(description_lines):
            text = self.info_font.render(line, True, BLACK)
            self.screen.blit(text, (info_panel_rect.x + 10, info_panel_rect.y + 80 + i * 25))
        
        # Draw updates
        y_offset = info_panel_rect.y + 80 + len(description_lines) * 25 + 20
        if self.current_step.updates:
            updates_text = self.info_font.render("Updates:", True, BLACK)
            self.screen.blit(updates_text, (info_panel_rect.x + 10, y_offset))
            y_offset += 30
            
            for i, (row, col, val) in enumerate(self.current_step.updates[:10]):  # Limit to 10 updates
                if self.current_step.update_type == "elimination":
                    update_text = self.info_font.render(
                        f"Eliminated candidate {val} from ({row}, {col})", True, BLACK)
                else:
                    update_text = self.info_font.render(
                        f"Placed value {val} at ({row}, {col})", True, GREEN)
                self.screen.blit(update_text, (info_panel_rect.x + 20, y_offset + i * 25))
            
            # If there are more updates, show a message
            if len(self.current_step.updates) > 10:
                more_text = self.info_font.render(
                    f"... and {len(self.current_step.updates) - 10} more", True, BLACK)
                self.screen.blit(more_text, (info_panel_rect.x + 20, 
                                           y_offset + 10 * 25))
        
        # Draw auto-play status
        auto_text = self.info_font.render(
            f"Auto-play: {'ON' if self.auto_play else 'OFF'} (Speed: {self.auto_play_speed:.1f}s)", 
            True, GREEN if self.auto_play else BLACK)
        self.screen.blit(auto_text, (info_panel_rect.x + 10, info_panel_rect.y + info_panel_rect.height - 40))
    
    def draw_buttons(self) -> None:
        """Draw the control buttons."""
        for button in self.buttons:
            # Draw button background
            color = LIGHT_GRAY
            if button["text"] == "Auto Play" and self.auto_play:
                color = YELLOW
            pygame.draw.rect(self.screen, color, button["rect"])
            pygame.draw.rect(self.screen, BLACK, button["rect"], 2)
            
            # Draw button text
            text = self.button_font.render(button["text"], True, BLACK)
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
    
    def update_display(self) -> None:
        """Update the display with the current step."""
        self.screen.fill(WHITE)
        
        # Draw main board
        self.draw_grid(PADDING, PADDING)
        self.draw_numbers(PADDING, PADDING)
        
        # Draw candidates
        self.draw_candidates(PADDING, PADDING)
        
        # Draw info panel
        self.draw_info_panel()
        
        # Draw buttons
        self.draw_buttons()
        
        pygame.display.flip()
    
    def previous_step(self) -> None:
        """Go to the previous step."""
        if self.current_step_index > 0:
            self.current_step_index -= 1
            self.current_step = self.logger.steps[self.current_step_index]
    
    def next_step(self) -> None:
        """Go to the next step."""
        if self.current_step_index < len(self.logger.steps) - 1:
            self.current_step_index += 1
            self.current_step = self.logger.steps[self.current_step_index]
    
    def toggle_auto_play(self) -> None:
        """Toggle auto-play mode."""
        self.auto_play = not self.auto_play
        self.last_auto_step_time = pygame.time.get_ticks()
    
    def increase_speed(self) -> None:
        """Increase auto-play speed."""
        self.auto_play_speed = max(0.2, self.auto_play_speed - 0.2)
    
    def decrease_speed(self) -> None:
        """Decrease auto-play speed."""
        self.auto_play_speed = min(5.0, self.auto_play_speed + 0.2)
    
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if the application should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.previous_step()
                elif event.key == pygame.K_RIGHT:
                    self.next_step()
                elif event.key == pygame.K_SPACE:
                    self.toggle_auto_play()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button was clicked
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()
        return True
    
    def update_auto_play(self) -> None:
        """Update auto-play if enabled."""
        if self.auto_play:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_auto_step_time > self.auto_play_speed * 1000:
                self.next_step()
                self.last_auto_step_time = current_time
                # Disable auto-play if we reached the end
                if self.current_step_index == len(self.logger.steps) - 1:
                    self.auto_play = False
    
    def run(self) -> None:
        """Run the visualization loop."""
        running = True
        while running:
            running = self.handle_events()
            self.update_auto_play()
            self.update_display()
            pygame.time.delay(30)  # 30ms delay to reduce CPU usage
    
    def close(self) -> None:
        """Close the pygame display."""
        pygame.quit()
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """Wrap text to fit within a given width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            # Try adding the word to the current line
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                # Start a new line
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines

# Example usage
# if __name__ == '__main__':
#     from board.board import Board
    
#     example_board_str = "300000400200709000087000000750060230600904008028050071000000960000000007800000104"
#     board = Board(example_board_str)
    
#     # Create a logger with some example steps
#     logger = SudokuGUILogger(verbose=True)
#     logger.log_initial_state(board)
    
#     # Simulate some solving steps
#     step1 = StepInfo(
#         strategy_name="Single Candidate",
#         updates=[(0, 2, 9)],
#         update_type="insertion",
#         board_state=[row[:] for row in board.cells],
#         candidates=[
#             [cell.copy() if cell else set() for cell in row] 
#             for row in board.candidates
#         ],
#         description="Found a single candidate at (0, 2)"
#     )
#     step1.board_state[0][2] = 9
#     logger.steps.append(step1)
    
#     # Create and run the display
#     display = SudokuGUIDisplay(board, logger)
#     display.run()
#     display.close() 