#!/usr/bin/env python

from core import Solver, check_guess
import argparse

def main():
    solver = Solver()

    parser = argparse.ArgumentParser(description='Mastermind')
    parser.add_argument('solution', metavar='s', type=str, nargs='?',
                        help='Guess against a pre-selected solution')
    args = parser.parse_args()

    try:
        if args.solution:
            for guess in solver.solve(args.solution):
                x = "".join(map(str, check_guess(guess, args.solution)))
                print(f"{guess}: {x}")
        else:
            print("2 = green, 1 = yellow, 0 = grey")
            solver.solve()
    except ValueError as e:
        print(e)

main()