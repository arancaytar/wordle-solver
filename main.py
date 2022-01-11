from core import Solver
import argparse

solver = Solver()

parser = argparse.ArgumentParser(description='Mastermind')
parser.add_argument('solution', metavar='s', type=str, nargs='?',
                    help='Guess against a pre-selected solution')
args = parser.parse_args()

if args.solution:
    print(solver.solve(args.solution))
else:
    solver.solve()