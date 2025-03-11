# Sudoku Solver

A comprehensive Python-based Sudoku solver implementing human-like solving strategies, from basic techniques to advanced solving methods.

## Features

- 🧩 Multiple solving strategies from basic to advanced
- 🔍 Human-like solving approach
- 📊 Detailed solving process visualization
- 📈 Performance analysis and statistics
- 🧪 Comprehensive testing framework

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

<!-- ## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sudoku-solver.git
cd sudoku-solver
``` -->

## Usage

### Basic Usage

1. Solve a single puzzle:
```bash
python test/test_framework.py --test "000921003009000060000000500080403006007000800500700040003000000020000700800195000"
```

2. Analyze multiple puzzles:
```bash
python test/test_framework.py --analyze 100
```

3. Test from a file:
```bash
python test/test_framework.py --test-file puzzles/selected_puzzles.json
```

### Advanced Usage

#### Verbose Output
Add `--verbose` for detailed solving process:
```bash
python test/test_framework.py --test "puzzle_string" --verbose
```

#### Strategy Analysis
View strategy usage statistics:
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



## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Strategy definitions from [SudokuWiki.org](https://www.sudokuwiki.org)
- Testing puzzles from various online resources

