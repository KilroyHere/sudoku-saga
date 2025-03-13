import sys
import json
import traceback
import numpy as np
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from puzzles.extract_puzzles import load_and_analyze_puzzles
from sudoku.solver_util import SolverUtil

class SudokuTestFramework:
    def __init__(self):
        self.results = []
        self.strategy_counts = {}
        
    def analyze_puzzles(self, num_puzzles=100, verbose=False):
        """Analyze multiple puzzles to gather statistics about strategy usage."""
        print(f"Loading {num_puzzles} puzzles...")
        quizzes, solutions = load_and_analyze_puzzles(num_puzzles)
        
        # Convert numpy arrays to strings
        puzzle_strings = [''.join(str(x) for x in quiz.flatten()) for quiz in quizzes]
        
        # Process each puzzle
        for idx, puzzle_str in enumerate(puzzle_strings):
            if verbose and idx % 100 == 0:
                print(f"\rProcessed {idx+1}/{len(puzzle_strings)} puzzles", end="")
            
            # Solve the puzzle
            result = SolverUtil.solve_puzzle(puzzle_str, verbose=False)
            
            # Update strategy counts
            for strategy in result["strategies_used"]:
                if strategy not in self.strategy_counts:
                    self.strategy_counts[strategy] = 0
                self.strategy_counts[strategy] += 1
            
            # Store result
            self.results.append({
                "id": idx,
                "puzzle": puzzle_str,
                "solution": ''.join(str(x) for x in solutions[idx].flatten()),
                "strategies_used": result["strategies_used"],
                "solved": result["solved"]
            })
        
        if verbose:
            print(f"\nFinished processing {len(self.results)} puzzles")
            self.print_statistics()
    
    def test_puzzle(self, puzzle_str, description="", verbose=False):
        """Test a single puzzle with detailed output of each step."""
        try:
            result = SolverUtil.solve_puzzle(puzzle_str, verbose=verbose, description=description)
        
                
        except Exception as e:
            print(f"\nError testing puzzle {description}:")
            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {str(e)}")
            print("\nTraceback:")
            traceback.print_exc()
    
    def print_statistics(self):
        """Print statistics about analyzed puzzles."""
        print("\nStrategy usage:")
        total_uses = sum(self.strategy_counts.values())
        for strategy, count in self.strategy_counts.items():
            percentage = (count / total_uses) * 100 if total_uses > 0 else 0
            print(f"{strategy}: {count} times ({percentage:.1f}%)")
        
        solved_count = sum(1 for r in self.results if r["solved"])
        total_count = len(self.results)
        if total_count > 0:
            print(f"\nSolved {solved_count} out of {total_count} puzzles ({(solved_count/total_count)*100:.1f}%)")
        
        if solved_count > 0:
            print("\nStrategy combinations:")
            strategy_combinations = {}
            for result in self.results:
                if result["solved"]:
                    combo = tuple(sorted(set(result["strategies_used"])))  # Get unique strategies used
                    strategy_combinations[combo] = strategy_combinations.get(combo, 0) + 1
            
            # Sort by frequency and print top 10
            sorted_combos = sorted(strategy_combinations.items(), key=lambda x: x[1], reverse=True)
            print("\nTop 10 most common strategy combinations:")
            for combo, count in sorted_combos[:10]:
                percentage = (count / solved_count) * 100
                print(f"{' + '.join(combo)}: {count} puzzles ({percentage:.1f}%)")
    
    def save_results(self, filename="puzzles/analysis_results.json"):
        """Save analysis results to a JSON file."""
        # Create strategy combinations data
        strategy_combinations = {}
        for result in self.results:
            if result["solved"]:
                combo = tuple(sorted(set(result["strategies_used"])))
                strategy_combinations[' + '.join(combo)] = strategy_combinations.get(' + '.join(combo), 0) + 1
        
        # Save detailed results
        print(f"\nSaving detailed results to {filename}")
        with open(filename, 'w') as f:
            json.dump({
                "summary": {
                    "total_puzzles": len(self.results),
                    "puzzles_solved": sum(1 for r in self.results if r["solved"]),
                    "strategy_counts": self.strategy_counts,
                    "strategy_combinations": strategy_combinations
                },
                "results": self.results
            }, f, indent=2)

def main():
    framework = SudokuTestFramework()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Sudoku Testing Framework')
    parser.add_argument('--analyze', type=int, metavar='N', help='Analyze N puzzles')
    parser.add_argument('--test', type=str, metavar='PUZZLE', help='Test a specific puzzle string')
    parser.add_argument('--test-file', type=str, help='Test puzzles from a JSON file')
    parser.add_argument('--verbose', action='store_true', help='Print detailed progress')
    args = parser.parse_args()
    
    if args.analyze:
        framework.analyze_puzzles(args.analyze, verbose=args.verbose)
        framework.save_results()
    
    elif args.test:
        framework.test_puzzle(args.test, "Command line puzzle", verbose=args.verbose)
    
    elif args.test_file:
        try:
            with open(args.test_file, "r") as f:
                data = json.load(f)
                test_cases = data["test_cases"]
                print(f"Loaded {len(test_cases)} test cases")
                
                for case in test_cases:
                    framework.test_puzzle(case["puzzle"], f"ID: {case['id']}", verbose=args.verbose)
                    try:
                        input("\nPress Enter to continue to next puzzle...")
                    except KeyboardInterrupt:
                        print("\nTesting interrupted by user")
                        break
        except FileNotFoundError:
            print(f"Error: {args.test_file} not found")
        except Exception as e:
            print(f"Error loading test cases: {str(e)}")
            traceback.print_exc()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 
    