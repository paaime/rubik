import argparse
import time
import sys
from cube import Cube
from utils import make_mix
from move import spin
from solver import RubikSolver
from tables.tables import make_tables
from utils import half_turn_metric
from visualizer import CubeVisualizer

RESET = "\033[0m"
BRIGHT = "\033[1m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('mix', nargs='?', help='Mix string')
    parser.add_argument('-r', '--random', nargs='?', const=-1, type=int,
                        help='Generate random mix of specified length')
    parser.add_argument('-v', '--visualizer', action='store_true',
                        help='Show visualization')
    
    args = parser.parse_args()
    
    if not args.mix and not args.random:
        print("./rubik.py \"Cube mix\"")
        sys.exit(1)
    
    mix = args.mix if args.mix else "-r"
    length = args.random if args.random else -1
    
    return mix, args.visualizer, length

def main():
    """Main function that runs the Rubik's cube solver"""
    mix, visualizer, length = parse_args()
    mix = make_mix(mix, length)

    if not mix:
        print("Invalid mix string, must be a sequence of moves (e.g. U R2 F' D)")
        sys.exit(1)
    
    tables = make_tables()
    cube = Cube()
    viz = None

    if visualizer:
        viz = CubeVisualizer()
    
    moves = mix.split()
    for move in moves:
        spin(move, cube)
        if viz:
            viz.apply_move(move, cube)
            time.sleep(1)

    # Create solver instance
    solver = RubikSolver(tables)
    
    start_time = time.time()
    solution = solver.solve(cube)
    elapsed = time.time() - start_time
    
    print("\n" + "="*50)
    print(f"{BRIGHT}RESULTS{RESET}".center(50))
    print("="*50 + "\n")
    
    if not cube.is_solved():
        print(f"Status: {RED}Cube not solved - Solution incorrect!{RESET}")
    else:
        print(f"Status: {GREEN}Success - Cube solved!{RESET}")
    
    print(f"\nMetrics:")
    print(f"  • HTM (Half Turn Metric): {YELLOW}{half_turn_metric(solution)}{RESET}")
    print(f"  • Time to solve: {YELLOW}{elapsed:.3f}s{RESET}")
    
    print(f"\nSolution:")
    print(f" {BRIGHT}{solution}{RESET}\n")
    print("="*50 + "\n")

     # Animate solution
    if viz:
        print("\nVisualizing solution...")
        solution_moves = solution.split()
        for move in solution_moves:
            spin(move, cube)
            viz.apply_move(move)
            time.sleep(0.3)  # Pause between moves

if __name__ == "__main__":
    main()