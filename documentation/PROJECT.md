# Sudoku Solver Project

## Project Overview
A Python-based Sudoku solver implementing various solving techniques from basic to advanced strategies. The project follows a structured approach using both backtracking and strategic methods, with a comprehensive set of solving strategies organized by complexity level.

## Directory Structure
```
sudoku/
├── board/
│   ├── board.py        # Main Board class implementation
│   ├── validator.py    # Validates Sudoku board state
│   └── colors.py       # ANSI color handling for display
├── solvers/
│   ├── solver.py          # Base Solver class
│   ├── solver_factory.py  # Factory for creating solver instances
│   ├── backtracking_solver.py  # Recursive backtracking implementation
│   ├── strategic_solver.py     # Strategy-based solving
│   └── csp_solver.py          # Constraint satisfaction solver
├── strategies/
│   ├── strategy.py        # Base Strategy class
│   ├── single_candidate.py
│   ├── hidden_singles.py
│   ├── pointing_pairs.py  # Recently implemented
│   ├── box_line_intersection.py  # Recently implemented
│   ├── naked_pairs.py
│   ├── hidden_pairs.py
│   ├── naked_triples.py
│   ├── hidden_triples.py
│   ├── naked_quads.py
│   └── hidden_quads.py
├── sudoku/
│   └── sudoku.py      # Main game logic and state machine
├── test/
│   └── test_framework.py  # Comprehensive testing framework
└── puzzles/
    ├── sudoku.csv          # Database of 1M puzzles
    ├── extract_puzzles.py  # Puzzle processing
    └── selected_puzzles.json  # Curated test cases
```

## Data Flow
1. Puzzle Input
   - Represented as 81-character string (0-9, 0 for empty)
   - Board class converts to 2D grid with candidate tracking
2. Solver Selection and Initialization
   - Factory creates appropriate solver instance
   - Initializes strategy hierarchy for strategic solving
3. Strategic Solving Process
   - Strategies applied from simplest to most complex
   - Each strategy either places values or eliminates candidates
   - Process continues until solved or unsolvable
4. State Machine Control
   - Manages solving process through defined states
   - Handles strategy selection and application
   - Tracks solving progress and completion

## Main Classes and Functions

### Board Class (board/board.py)
- Manages grid representation and candidate tracking
- Provides validation and visualization functions
- Key methods:
  ```python
  - update_candidates_on_insert(row, col)
  - check_placement(row, col, value)
  - display_board()
  ```

### Solver Hierarchy
- **Solver** (solvers/solver.py) - Base abstract class
- **BacktrackingSolver** (solvers/backtracking_solver.py) - Uses recursive backtracking
- **StrategicSolver** (solvers/strategic_solver.py) - Uses human-like strategies
- **SolverFactory** (solvers/solver_factory.py) - Creates appropriate solvers

### Strategy Hierarchy
- **Strategy** (strategies/strategy.py) - Base class for all strategies
  - **SingleCandidateStrategy** - Finds cells with only one possible value
  - **NakedPairsStrategy** - Identifies and applies the Naked Pairs strategy
  - **NakedTriplesStrategy** - Identifies and applies the Naked Triples strategy
  - **NakedQuadsStrategy** - Identifies and applies the Naked Quads strategy
  - **HiddenSinglesStrategy** - Identifies numbers that can only go in one cell in a unit
  - **HiddenPairsStrategy** - Identifies pairs of numbers that can only go in two cells in a unit
  - **HiddenTriplesStrategy** - Identifies three numbers that can only go in three cells in a unit
  - **HiddenQuadsStrategy** - Identifies four numbers that can only go in four cells in a unit

### Sudoku (sudoku/sudoku.py)
- Manages the overall game
- Uses a state machine (SudokuStateMachine) to control the solving process
- States:
  - finding_best_strategy
  - applying_strategy
  - checking_if_solved
  - solved
  - unsolvable

## Test Framework (test/test_framework.py)
The project includes a comprehensive test framework for analyzing and validating Sudoku solving strategies.

### Key Features
- **Puzzle Analysis**: Can analyze large batches of puzzles to gather statistics about strategy usage
- **Strategy Testing**: Tests individual strategies and tracks their effectiveness
- **Detailed Logging**: Shows step-by-step solving process with board state and candidates
- **Statistics Collection**: Tracks strategy usage patterns and success rates

### Using the Test Framework
The test framework can be used in several ways:

1. **Analyze Multiple Puzzles**:
   ```bash
   python test/test_framework.py --analyze N
   ```
   Where N is the number of puzzles to analyze (e.g., 100, 1000, etc.)
   Add --verbose for detailed output.

2. **Test a Specific Puzzle**:
   ```bash
   python test/test_framework.py --test "puzzle_string"
   ```
   Where puzzle_string is an 81-character string representing the puzzle (use 0 for empty cells).
   Example:
   ```bash
   python test/test_framework.py --test "000000000001900500560310090100600028004000700270004003040068035002005900000000000"
   ```

3. **Test from JSON File**:
   ```bash
   python test/test_framework.py --test-file path/to/test_cases.json
   ```
   The JSON file should contain an array of test cases with puzzle strings.

### Output Information
The test framework provides:
- Initial board state and candidates
- Step-by-step strategy application
- Board state after each move
- Candidate updates
- Final statistics including:
  - Strategy usage counts
  - Success rates
  - Strategy combinations used

### Results Storage
Analysis results are saved to `puzzles/analysis_results.json`, including:
- Summary statistics
- Strategy counts
- Strategy combinations
- Individual puzzle results

## Project Status
- Core solving strategies implemented and tested
- Test framework complete with comprehensive analysis capabilities
- Successfully solving puzzles of varying difficulty levels

### Implemented Strategies
- [x] Basic Strategies
  - Single Candidate (Naked Singles)
  - Hidden Singles
  - Pointing Pairs
  - Box/Line Intersection
  - Naked/Hidden Pairs
  - Naked/Hidden Triples
  - Naked/Hidden Quads

### In Progress
- [ ] X-Wing Strategy
  - Core algorithm designed
  - Initial implementation started
- [ ] Swordfish Strategy
  - Design phase complete
  - Implementation pending

### Planned Implementations
1. Tough Strategies
   - Simple Coloring
   - Y-Wing
   - XYZ-Wing
   - W-Wing
   - Rectangle Patterns
   - BUG (Bivalue Universal Grave)
2. Diabolical Strategies
   - X-Cycles
   - XY-Chains
   - 3D Medusa
   - Jellyfish
   - Unique Rectangles
3. Extreme Strategies
   - Almost Locked Sets
   - Finned X-Wing/Swordfish
   - Inference Chains
   - Sue-de-Coq
   - Death Blossom

## Implementation Notes

### Strategy Hierarchy
Strategies ordered by complexity and effectiveness:
1. Basic Strategies (implemented)
   - Single candidates
   - Hidden singles
   - Pointing pairs
   - Box/line intersection
   - Naked/Hidden pairs/triples/quads
2. Tough Strategies (in progress)
   - X-Wing and variants
   - Wings (XY, XYZ, W)
   - Rectangle patterns
3. Diabolical/Extreme Strategies (planned)
   - Chains and cycles
   - Advanced pattern recognition
   - Complex inference techniques

### Recent Updates
1. Basic Strategy Completion
   - Implemented Pointing Pairs
   - Implemented Box/Line Intersection
   - Integrated with existing strategy framework
   - Verified against test cases

2. Performance Optimizations
   - Ordered strategies by computational complexity
   - Optimized candidate elimination routines
   - Enhanced strategy selection process

### Testing Framework
Features:
- Puzzle analysis with statistics
- Strategy effectiveness tracking
- Step-by-step visualization
- Performance benchmarking

Usage:
```bash
# Analyze multiple puzzles
python test/test_framework.py --analyze N

# Test specific puzzle
python test/test_framework.py --test "puzzle_string"

# Test from file
python test/test_framework.py --test-file path/to/test_cases.json
```

## Component Interfaces

### Strategy Interface
```python
Interface: Strategy
Methods:
  - process(): Returns List[Tuple[int, int, int]]
  - _get_cells_with_candidate()
  + strategy-specific helper methods
```

### Solver Interface
```python
Interface: StrategicSolver
Methods:
  - find_strategy()
  - apply_strategy()
  - _eliminate_candidates()
  - _insert_values()
```

## Dependencies
- Strategy classes → Board class
- StrategicSolver → Strategy implementations
- Test framework → Solver and Board implementations
- State machine → Strategy execution control



