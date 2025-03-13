import pygame
import math
import sys
import os
from typing import List, Set

# Add the project root to the path when running this file directly
if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from board.board import Board
from sudoku.logger import SudokuLogger

# Display constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
GRID_SIZE = 9
BOARD_SIZE = 600
CELL_SIZE = BOARD_SIZE // GRID_SIZE
CANDIDATE_CELL_SIZE = CELL_SIZE // 3
PADDING = 20
BUTTON_HEIGHT = 50
BUTTON_WIDTH = 160
SPEED_BUTTON_WIDTH = 140  # Wider speed buttons for better visibility
SPEED_BUTTON_SPACING = 30  # Much more spacing between speed buttons
INFO_PANEL_WIDTH = 500
BUTTON_RADIUS = 10

# Refined color palette
WHITE = (252, 252, 252)
BLACK = (40, 40, 40)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 245)
DARK_GRAY = (100, 100, 110)
BLUE = (65, 105, 225)
RED = (220, 60, 60)
GREEN = (60, 179, 113)
YELLOW = (255, 223, 0)
PURPLE = (147, 112, 219)
HIGHLIGHT_COLOR = (255, 255, 200, 180)
PANEL_BG = (248, 248, 255)
BOX_COLOR = (230, 230, 250)
GRID_COLOR = (70, 70, 70)
BUTTON_HOVER = (230, 230, 255)
ORIGINAL_CELL_BG = (245, 240, 240, 50)
SOLVED_CELL_BG = (240, 245, 255, 30)
CANDIDATE_BG = (245, 245, 255)
BACKGROUND_COLOR = (245, 245, 255)

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
        super().log_strategy_found(strategy_name, details)
        
        self.current_step.strategy_name = strategy_name
        if details:
            self.current_step.description = f"Found {strategy_name}: {details}"
        else:
            self.current_step.description = f"Found {strategy_name}"
    
    def log_strategy_applied(self, strategy_name: str, updates: List, update_type: str = None):
        super().log_strategy_applied(strategy_name, updates, update_type)
        
        if self.current_board:
            self.current_step.board_state = [row[:] for row in self.current_board.cells]
            self.current_step.candidates = [
                [cell.copy() if cell else set() for cell in row] 
                for row in self.current_board.candidates
            ]
            self.current_step.updates = updates
            self.current_step.update_type = update_type
            
            if update_type == "elimination":
                self.current_step.description = f"Applied {strategy_name}: Eliminated {len(updates)} candidates"
            elif update_type == "insertion":
                self.current_step.description = f"Applied {strategy_name}: Inserted {len(updates)} values"
            else:
                self.current_step.description = f"Applied {strategy_name}"
            
            self.steps.append(self.current_step)
            self.current_step = StepInfo()
    
    def log_final_state(self, board, solved: bool):
        super().log_final_state(board, solved)
        
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
        """Initialize the GUI display with the given Sudoku board and logger."""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Sudoku Saga - Advanced Solver')
        
        # Simpler icon approach that's more likely to work across platforms
        try:
            # Create a solid purple square icon - simple but distinctive
            icon = pygame.Surface((32, 32))
            icon.fill(PURPLE)
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Could not set icon: {e}")
            
        # Initialize fonts
        self.title_font = pygame.font.Font(None, 42)
        self.number_font = pygame.font.Font(None, 42)
        self.candidate_font = pygame.font.Font(None, 20)
        self.info_font = pygame.font.Font(None, 28)
        self.button_font = pygame.font.Font(None, 28)
        
        self.board = board
        self.logger = logger
        self.current_step_index = 0
        self.auto_play = False
        self.auto_play_speed = 1.0  # seconds between steps
        self.last_auto_step_time = 0
        self.hover_button = None
        
        # Animation values
        self.animation_progress = 0
        self.animation_speed = 0.03
        
        # Set up button layout
        self._setup_buttons()
        
        # Initialize with first step
        if logger.steps:
            self.current_step = logger.steps[0]
        else:
            self.current_step = StepInfo()
    
    def _setup_buttons(self):
        """Set up the control buttons with proper spacing and alignment."""
        button_y = WINDOW_HEIGHT - BUTTON_HEIGHT - PADDING
        button_spacing = 15
        
        # Calculate button positions with much more space for speed buttons
        prev_button_x = PADDING
        next_button_x = prev_button_x + BUTTON_WIDTH + button_spacing
        auto_button_x = next_button_x + BUTTON_WIDTH + button_spacing
        
        # Position speed buttons with significantly more spacing
        # and place them farther to the right
        speed_minus_x = auto_button_x + BUTTON_WIDTH + 40  # Extra space after auto play
        speed_plus_x = speed_minus_x + SPEED_BUTTON_WIDTH + SPEED_BUTTON_SPACING
        
        self.buttons = [
            {"text": "Previous", "rect": pygame.Rect(prev_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 
             "action": self.previous_step, "icon": "<"},
            {"text": "Next", "rect": pygame.Rect(next_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 
             "action": self.next_step, "icon": ">"},
            {"text": "Auto Play", "rect": pygame.Rect(auto_button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 
             "action": self.toggle_auto_play, "icon": ">>"},
            {"text": "Speed -", "rect": pygame.Rect(speed_minus_x, button_y, SPEED_BUTTON_WIDTH, BUTTON_HEIGHT), 
             "action": self.decrease_speed, "icon": "-"},
            {"text": "Speed +", "rect": pygame.Rect(speed_plus_x, button_y, SPEED_BUTTON_WIDTH, BUTTON_HEIGHT), 
             "action": self.increase_speed, "icon": "+"}
        ]
    
    def draw_rounded_rect(self, surface, rect, color, radius=10, border=0, border_color=None):
        """Draw a rounded rectangle."""
        rect = pygame.Rect(rect)
        pygame.draw.rect(surface, color, rect, border, border_radius=radius)
        
        if border > 0 and border_color:
            pygame.draw.rect(surface, border_color, rect, border, border_radius=radius)
    
    def draw_grid(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the Sudoku grid with stylized visual elements."""
        # Draw board background
        board_rect = pygame.Rect(x_offset, y_offset, BOARD_SIZE, BOARD_SIZE)
        self.draw_rounded_rect(self.screen, board_rect, WHITE, radius=15)
        
        # Draw alternating box backgrounds for visual separation
        for box_row in range(3):
            for box_col in range(3):
                if (box_row + box_col) % 2 == 0:
                    box_rect = pygame.Rect(
                        x_offset + box_col * (CELL_SIZE * 3),
                        y_offset + box_row * (CELL_SIZE * 3),
                        CELL_SIZE * 3, CELL_SIZE * 3
                    )
                    self.draw_rounded_rect(self.screen, box_rect, BOX_COLOR, radius=2)
        
        # Draw grid lines
        for i in range(0, BOARD_SIZE + 1, CELL_SIZE):
            is_box_boundary = i % (CELL_SIZE * 3) == 0
            line_thickness = 3 if is_box_boundary else 1
            line_color = GRID_COLOR if is_box_boundary else DARK_GRAY
            
            # Horizontal lines
            pygame.draw.line(
                self.screen, line_color,
                (x_offset, y_offset + i),
                (x_offset + BOARD_SIZE, y_offset + i),
                line_thickness
            )
            
            # Vertical lines
            pygame.draw.line(
                self.screen, line_color,
                (x_offset + i, y_offset),
                (x_offset + i, y_offset + BOARD_SIZE),
                line_thickness
            )
    
    def draw_numbers(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the numbers on the Sudoku board."""
        if not self.current_step.board_state:
            return
            
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell_rect = pygame.Rect(
                    x_offset + col * CELL_SIZE, 
                    y_offset + row * CELL_SIZE,
                    CELL_SIZE, CELL_SIZE
                )
                
                # Handle highlighting for cells
                if (row, col) in self.current_step.highlighted_cells:
                    # Create pulsing highlight effect
                    alpha = int(100 + 80 * math.sin(self.animation_progress * 2.5))
                    highlight_surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill((255, 255, 180, alpha))
                    self.screen.blit(highlight_surface, cell_rect)
                
                # Draw cell value if present
                num = self.current_step.board_state[row][col]
                if num is not None:
                    is_original = self.board.original[row][col] is not None
                    color = RED if is_original else BLUE
                    bg_color = ORIGINAL_CELL_BG if is_original else SOLVED_CELL_BG
                    
                    # Add subtle cell background
                    cell_bg = pygame.Surface((CELL_SIZE-4, CELL_SIZE-4), pygame.SRCALPHA)
                    cell_bg.fill(bg_color)
                    self.screen.blit(cell_bg, (cell_rect.x+2, cell_rect.y+2))
                    
                    # Render the number
                    text = self.number_font.render(str(num), True, color)
                    text_rect = text.get_rect(center=(
                        x_offset + col * CELL_SIZE + CELL_SIZE // 2,
                        y_offset + row * CELL_SIZE + CELL_SIZE // 2
                    ))
                    self.screen.blit(text, text_rect)
    
    def draw_candidates(self, x_offset: int = 0, y_offset: int = 0) -> None:
        """Draw the candidate numbers for empty cells."""
        if not self.current_step.candidates:
            return
            
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Only draw candidates for empty cells
                if self.current_step.board_state[row][col] is None:
                    candidates = self.current_step.candidates[row][col]
                    
                    # Skip if no candidates
                    if not candidates:
                        continue
                    
                    # Draw subtle background for the cell with candidates
                    cell_rect = pygame.Rect(
                        x_offset + col * CELL_SIZE + 2, 
                        y_offset + row * CELL_SIZE + 2,
                        CELL_SIZE - 4, CELL_SIZE - 4
                    )
                    pygame.draw.rect(self.screen, (248, 248, 255, 30), cell_rect, border_radius=2)
                    
                    # Draw each candidate
                    for num in range(1, 10):
                        if num not in candidates:
                            continue
                            
                        # Calculate position within the cell
                        sub_row = (num - 1) // 3
                        sub_col = (num - 1) % 3
                        
                        center_x = x_offset + col * CELL_SIZE + sub_col * CANDIDATE_CELL_SIZE + CANDIDATE_CELL_SIZE // 2
                        center_y = y_offset + row * CELL_SIZE + sub_row * CANDIDATE_CELL_SIZE + CANDIDATE_CELL_SIZE // 2
                        
                        # Draw background for each candidate
                        candidate_rect = pygame.Rect(
                            center_x - CANDIDATE_CELL_SIZE // 3 + 1,
                            center_y - CANDIDATE_CELL_SIZE // 3 + 1,
                            CANDIDATE_CELL_SIZE * 2 // 3 - 2,
                            CANDIDATE_CELL_SIZE * 2 // 3 - 2
                        )
                        pygame.draw.rect(self.screen, CANDIDATE_BG, candidate_rect, border_radius=3)
                        
                        # Draw the number
                        text = self.candidate_font.render(str(num), True, DARK_GRAY)
                        text_rect = text.get_rect(center=(center_x, center_y))
                        self.screen.blit(text, text_rect)
    
    def draw_info_panel(self, y_offset: int = PADDING) -> None:
        """Draw the information panel showing current step details."""
        # Panel background
        info_panel_rect = pygame.Rect(
            BOARD_SIZE + PADDING * 2, y_offset, 
            INFO_PANEL_WIDTH, BOARD_SIZE
        )
        self.draw_rounded_rect(self.screen, info_panel_rect, PANEL_BG, radius=15, border=2, border_color=DARK_GRAY)
        
        # Header section
        header_rect = pygame.Rect(
            info_panel_rect.x, info_panel_rect.y, 
            INFO_PANEL_WIDTH, 70
        )
        self.draw_rounded_rect(self.screen, header_rect, (230, 230, 250), radius=15, border=0)
        
        # Step counter with shadow
        title_shadow = self.title_font.render(
            f"Step {self.current_step_index + 1}/{len(self.logger.steps)}", 
            True, (100, 100, 100)
        )
        title_text = self.title_font.render(
            f"Step {self.current_step_index + 1}/{len(self.logger.steps)}", 
            True, BLACK
        )
        self.screen.blit(title_shadow, (info_panel_rect.x + 12, info_panel_rect.y + 17))
        self.screen.blit(title_text, (info_panel_rect.x + 10, info_panel_rect.y + 15))
        
        # Strategy name
        strategy_rect = pygame.Rect(
            info_panel_rect.x + 10, info_panel_rect.y + 55, 
            INFO_PANEL_WIDTH - 20, 40
        )
        self.draw_rounded_rect(self.screen, strategy_rect, (240, 240, 255), radius=10)
        
        strategy_text = self.info_font.render(
            f"Strategy: {self.current_step.strategy_name}", 
            True, BLUE
        )
        self.screen.blit(strategy_text, (info_panel_rect.x + 20, info_panel_rect.y + 60))
        
        # Divider
        pygame.draw.line(
            self.screen, GRAY, 
            (info_panel_rect.x + 20, info_panel_rect.y + 105), 
            (info_panel_rect.x + INFO_PANEL_WIDTH - 20, info_panel_rect.y + 105), 
            1
        )
        
        # Description text
        description_lines = self._wrap_text(
            self.current_step.description, 
            self.info_font, INFO_PANEL_WIDTH - 40
        )
        for i, line in enumerate(description_lines):
            text = self.info_font.render(line, True, BLACK)
            self.screen.blit(text, (info_panel_rect.x + 20, info_panel_rect.y + 120 + i * 30))
        
        # Updates section
        y_offset = info_panel_rect.y + 120 + len(description_lines) * 30 + 20
        if self.current_step.updates:
            # Updates header
            updates_bg = pygame.Rect(
                info_panel_rect.x + 10, y_offset - 5, 
                INFO_PANEL_WIDTH - 20, 35
            )
            self.draw_rounded_rect(self.screen, updates_bg, (235, 245, 255), radius=5)
            
            updates_text = self.info_font.render("Updates:", True, BLACK)
            self.screen.blit(updates_text, (info_panel_rect.x + 20, y_offset))
            y_offset += 40
            
            # Draw each update (limited to 10)
            for i, (row, col, val) in enumerate(self.current_step.updates[:10]):
                update_bg = pygame.Rect(
                    info_panel_rect.x + 15, y_offset + i * 30 - 5, 
                    INFO_PANEL_WIDTH - 30, 25
                )
                
                if self.current_step.update_type == "elimination":
                    update_color = (255, 240, 240)  # Light red
                    update_text = self.info_font.render(
                        f"Eliminated candidate {val} from ({row}, {col})", True, RED
                    )
                else:
                    update_color = (240, 255, 240)  # Light green
                    update_text = self.info_font.render(
                        f"Placed value {val} at ({row}, {col})", True, GREEN
                    )
                
                self.draw_rounded_rect(self.screen, update_bg, update_color, radius=5)
                self.screen.blit(update_text, (info_panel_rect.x + 25, y_offset + i * 30))
            
            # Show message for additional updates if more than 10
            if len(self.current_step.updates) > 10:
                more_text = self.info_font.render(
                    f"... and {len(self.current_step.updates) - 10} more", 
                    True, DARK_GRAY
                )
                self.screen.blit(more_text, (
                    info_panel_rect.x + 25, y_offset + 10 * 30
                ))
        
        # Auto-play status
        auto_rect = pygame.Rect(
            info_panel_rect.x + 10, info_panel_rect.y + info_panel_rect.height - 50, 
            INFO_PANEL_WIDTH - 20, 40
        )
        auto_color = (230, 255, 230) if self.auto_play else (245, 245, 255)
        self.draw_rounded_rect(self.screen, auto_rect, auto_color, radius=10)
        
        auto_text = self.info_font.render(
            f"Auto-play: {'ON' if self.auto_play else 'OFF'} (Speed: {self.auto_play_speed:.1f}s)", 
            True, GREEN if self.auto_play else DARK_GRAY
        )
        self.screen.blit(auto_text, (info_panel_rect.x + 20, info_panel_rect.y + info_panel_rect.height - 40))
    
    def draw_buttons(self) -> None:
        """Draw the control buttons with proper styling."""
        mouse_pos = pygame.mouse.get_pos()
        self.hover_button = None
        
        for i, button in enumerate(self.buttons):
            # Determine button state
            is_hovered = button["rect"].collidepoint(mouse_pos)
            if is_hovered:
                self.hover_button = i
            
            # Set colors based on state and button type
            if button["text"] == "Auto Play" and self.auto_play:
                button_color = YELLOW
                text_color = BLACK
            elif "Speed" in button["text"]:
                # Completely distinct styling for speed buttons
                if is_hovered:
                    button_color = (200, 220, 255)  # Lighter blue for hover
                    text_color = BLUE
                    border_color = BLUE
                else:
                    button_color = (225, 225, 245)  # Very light purple for speed buttons
                    text_color = DARK_GRAY
                    border_color = PURPLE
            elif is_hovered:
                button_color = BUTTON_HOVER
                text_color = BLUE
                border_color = DARK_GRAY
            else:
                button_color = LIGHT_GRAY
                text_color = BLACK
                border_color = GRAY
            
            # Draw button base
            self.draw_rounded_rect(
                self.screen, 
                button["rect"], 
                button_color, 
                radius=BUTTON_RADIUS,
                border=2,
                border_color=border_color
            )
            
            if "icon" in button:
                # Draw icon
                icon_text = self.button_font.render(button["icon"], True, text_color)
                
                # Position icon based on button type
                if button["text"] in ["Speed -", "Speed +"]:
                    # For speed buttons, place icon on the left side
                    icon_rect = icon_text.get_rect(
                        center=(button["rect"].left + 25, button["rect"].centery)
                    )
                else:
                    icon_rect = icon_text.get_rect(
                        center=(button["rect"].left + 20, button["rect"].centery)
                    )
                
                self.screen.blit(icon_text, icon_rect)
                
                # Draw button text
                text = self.button_font.render(button["text"], True, text_color)
                
                # Position text based on button type
                if button["text"] in ["Speed -", "Speed +"]:
                    # For speed buttons, center the text more
                    text_rect = text.get_rect(
                        center=(button["rect"].centerx + 8, button["rect"].centery)
                    )
                else:
                    text_rect = text.get_rect(
                        midleft=(button["rect"].left + 40, button["rect"].centery)
                    )
                
                self.screen.blit(text, text_rect)
            else:
                # Button without icon
                text = self.button_font.render(button["text"], True, text_color)
                text_rect = text.get_rect(center=button["rect"].center)
                self.screen.blit(text, text_rect)
    
    def draw_title(self) -> None:
        """Draw the application title with shadow effect."""
        # Larger font size for main title
        title_font = pygame.font.Font(None, 50)
        
        # Create title text
        title_shadow = title_font.render("Sudoku Saga", True, (180, 180, 200))
        title_text = title_font.render("Sudoku Saga", True, PURPLE)
        
        # Position at the very top center of the window
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, PADDING + 15))
        
        # Draw title with enhanced shadow effect
        self.screen.blit(title_shadow, (title_rect.x + 2, title_rect.y + 2))
        self.screen.blit(title_text, title_rect)
    
    def update_display(self) -> None:
        """Update the display with the current step."""
        # Update animation
        self.animation_progress += self.animation_speed
        
        # Clear screen
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw title at the top
        self.draw_title()
        
        # Draw board shadow
        board_shadow_rect = pygame.Rect(PADDING + 5, PADDING + 40, BOARD_SIZE, BOARD_SIZE)
        self.draw_rounded_rect(self.screen, board_shadow_rect, (210, 210, 220), radius=15)
        
        # Draw main board components - adjusted for title space
        self.draw_grid(PADDING, PADDING + 40)
        self.draw_numbers(PADDING, PADDING + 40)
        self.draw_candidates(PADDING, PADDING + 40)
        
        # Draw info panel - adjusted for title space
        info_panel_top = PADDING + 40
        self.draw_info_panel(info_panel_top)
        
        # Draw buttons
        self.draw_buttons()
        
        # Update the display
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
        """Increase auto-play speed (decrease delay)."""
        self.auto_play_speed = max(0.2, self.auto_play_speed - 0.2)
    
    def decrease_speed(self) -> None:
        """Decrease auto-play speed (increase delay)."""
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
                elif event.key == pygame.K_ESCAPE:
                    return False  # Exit on Escape key
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if any button was clicked
                for button in self.buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()
                        pygame.time.delay(50)  # Button click feedback
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
            pygame.time.delay(30)  # Cap frame rate
    
    def close(self) -> None:
        """Close the pygame display."""
        pygame.quit()
    
    def _wrap_text(self, text: str, font, max_width: int) -> List[str]:
        """Wrap text to fit within a given width."""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_width = font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
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