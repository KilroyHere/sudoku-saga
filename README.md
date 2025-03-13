# Sudoku Solver

A comprehensive Python-based Sudoku solver implementing human-like solving strategies, from basic techniques to advanced solving methods. The solver now features a centralized logging system with both verbose and non-verbose output modes.

## Features

- 🧩 Multiple solving strategies from basic to advanced
- 🔍 Human-like solving approach
- 📊 Detailed solving process visualization
- 📈 Performance analysis and statistics
- 🧪 Comprehensive testing framework
- 🔄 Centralized logging system with verbosity control
- 🖥️ User-friendly command-line interface

### Implemented Strategies

#### Basic Strategies
- ✓ Single Candidate (Naked Singles)
- ✓ Hidden Singles
- ✓ Pointing Pairs
- ✓ Box/Line Intersection
- ✓ Naked Pairs/Triples/Quads
- ✓ Hidden Pairs/Triples/Quads

#### In Development
- X-Wing Strategy
- Swordfish Strategy


## Usage

### Basic Usage

1. Solve a puzzle with default settings:
```bash
python main.py
```

2. Solve a specific puzzle:
```bash
python main.py -p "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
```

3. Enable verbose output:
```bash
python main.py -v
```

4. Provide a puzzle description:
```bash
python main.py -p "puzzle_string" -d "My difficult puzzle"
```

### Command-line Arguments

- `-v, --verbose`: Enable verbose output with detailed solving steps
- `-p, --puzzle`: Specify a Sudoku puzzle string (81 characters, use 0 or . for empty cells)
- `-d, --description`: Provide a description for the puzzle

### Output Modes

#### Non-verbose Mode
- Shows initial and final board states
- Displays strategies applied and their effects
- Provides a summary of strategies used

#### Verbose Mode
- Shows detailed step-by-step solving process
- Displays board state after each strategy application
- Shows candidate eliminations and value insertions
- Provides comprehensive solving statistics

### Advanced Usage

#### Testing Framework
```bash
python test/test_framework.py --test "puzzle_string" --verbose
```

#### Strategy Analysis
```bash
python test/test_framework.py --analyze 100 
```

## Solving Strategies

### Basic Strategies
1. **Single Candidate (Naked Singles)**
   - Finds cells with only one possible value

2. **Hidden Singles**
   - Identifies numbers that can only go in one cell in a unit

3. **Pointing Pairs/Triples**
   - When candidates in a box are restricted to one row/column

4. **Box/Line Intersection**
   - When candidates in a row/column are restricted to one box

5. **Naked/Hidden Pairs/Triples/Quads**
   - Groups of cells sharing the same candidates

### Advanced Strategies (In Development)
- X-Wing
- Swordfish
- Simple Coloring
- Y-Wing
- XYZ-Wing
- Rectangle Patterns

## Testing Framework

The project includes a comprehensive testing framework for:
- Strategy validation
- Performance analysis
- Puzzle difficulty assessment
- Solving process visualization

## Documentation

For detailed documentation, see the [PROJECT.md](documentation/PROJECT.md) file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Strategy definitions from [SudokuWiki.org](https://www.sudokuwiki.org)
- Testing puzzles from various online resources

