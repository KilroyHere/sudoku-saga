# Contributing to the Sudoku Solver Project

Thank you for your interest in contributing to the Sudoku Solver project! This document provides guidelines and information for contributors.

## Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone [your-fork-url]
   cd sudoku
   ```
3. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style
- Follow PEP 8 guidelines for Python code
- Use meaningful variable and function names
- Include docstrings for classes and functions
- Add comments for complex logic

### Adding New Strategies
When implementing a new solving strategy:

1. Create a new file in the `strategies/` directory
2. Inherit from the base `Strategy` class
3. Implement the `process()` method
4. Add the strategy to `StrategicSolver`'s strategy list
5. Add appropriate tests in `test/test_strategies.py`

Example:
```python
from strategies.strategy import Strategy

class NewStrategy(Strategy):
    def __init__(self, board):
        super().__init__(board, name="New Strategy", type="Candidate Eliminator")
    
    def process(self):
        # Implementation here
        pass
```

### Testing
Before submitting a pull request:

1. Test your changes:
   ```bash
   python test/test_framework.py --analyze 100
   ```
2. Add specific test cases:
   ```bash
   python test/test_framework.py --test "your_test_puzzle"
   ```
3. Ensure all existing tests pass
4. Add new test cases for your changes

### Documentation
- Update relevant documentation in `project.md`
- Add strategy descriptions and examples
- Document any new features or changes
- Update README.md if necessary

## Pull Request Process

1. Update the README.md with details of changes if applicable
2. Update the project.md with implementation details
3. Add test cases demonstrating the new functionality
4. Create a pull request with a clear description of the changes

## Strategy Implementation Guidelines

When implementing a new strategy:

1. **Research**: Understand the strategy thoroughly using resources like SudokuWiki.org
2. **Documentation**: Include references and examples
3. **Testing**: Provide test cases that specifically require your strategy
4. **Performance**: Consider computational efficiency
5. **Integration**: Ensure proper integration with existing strategies

## Bug Reports

When reporting bugs:

1. Use the issue tracker
2. Include the puzzle string that caused the issue
3. Provide the exact command used
4. Include the full error message or unexpected behavior
5. Describe the expected behavior

## Feature Requests

For feature requests:

1. Check if the feature is already planned
2. Provide a clear use case
3. Include examples if possible
4. Discuss implementation approaches

## Questions and Discussion

For questions or discussions:

1. Check existing issues and documentation first
2. Create a new issue with the "question" label
3. Provide context and examples

## License

By contributing, you agree that your contributions will be licensed under the same license as the project. 