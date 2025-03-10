import numpy as np

# This script is used to extract puzzles from the sudoku.csv file.


def load_and_analyze_puzzles(num_puzzles=100):
    """
    Load puzzles from sudoku.csv and return the first num_puzzles puzzles and their solutions.
    
    Args:
        num_puzzles (int): Number of puzzles to load (default: 100)
    
    Returns:
        tuple: (quizzes, solutions) as numpy arrays of shape (num_puzzles, 9, 9)
    
    Raises:
        ValueError: If num_puzzles is greater than the total available puzzles
    """
    # First count total puzzles in the file
    total_puzzles = sum(1 for line in open('puzzles/sudoku.csv')) - 1  # -1 for header
    
    if num_puzzles > total_puzzles:
        raise ValueError(f"Requested {num_puzzles} puzzles but only {total_puzzles} are available in the CSV file")
    
    print(f"Loading {num_puzzles} puzzles from sudoku.csv...")
    
    # Initialize arrays
    quizzes = np.zeros((num_puzzles, 81), dtype=int)
    solutions = np.zeros((num_puzzles, 81), dtype=int)
    
    # Read and parse puzzles
    with open('puzzles/sudoku.csv', 'r') as f:
        next(f)  # Skip header
        for i, line in enumerate(f):
            if i >= num_puzzles:
                break
                
            quiz, solution = line.strip().split(",")
            for j, (q, s) in enumerate(zip(quiz, solution)):
                quizzes[i, j] = int(q)
                solutions[i, j] = int(s)
    
    quizzes = quizzes.reshape((-1, 9, 9))
    solutions = solutions.reshape((-1, 9, 9))
    
    print(f"Successfully loaded {len(quizzes)} puzzles")
    return quizzes, solutions

if __name__ == "__main__":
    # Load 10,000 puzzles for testing
    quizzes, solutions = load_and_analyze_puzzles(10000)
    print(f"Shape of quizzes array: {quizzes.shape}")
    print(f"Shape of solutions array: {solutions.shape}")
    
    # Print an example puzzle and its solution
    print("\nExample puzzle:")
    print(quizzes[0])
    print("\nIts solution:")
    print(solutions[0])