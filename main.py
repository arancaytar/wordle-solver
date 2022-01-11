#!/usr/bin/env python

from core import Solver, check_guess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Mastermind')
    parser.add_argument('solution', metavar='s', type=str, nargs='?',
                        help='Guess against a pre-selected solution')
    parser.add_argument('--method', type=str,
                        help='Select the method (max_entropy, min_max_pool, min_avg_pool).',
                        default='max_entropy')
    args = parser.parse_args()

    solver = Solver(args.method)
    try:
        if args.solution:
            for guess in solver.solve(args.solution):
                x = "".join(map(str, check_guess(guess, args.solution)))
                print(f"{guess}: {x}")
        else:
            print("2 = green, 1 = yellow, 0 = grey, eg. 01020")
            print("Manually override suggested guess, eg: 'guess01020'")
            solver.solve()
    except ValueError as e:
        print(e)

main()