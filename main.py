#!/usr/bin/env python

from core import Solver, check_guess
import argparse


def output(s, format):
    format = {
                'u': ['⬜️', '🟨', '🟩'],
                'c': 'wyg',
                'n': '012',
                'b': ['⬛️', '🟨', '🟩'],
    }[format]
    return "".join(format[int(i)] for i in s)


def main():
    parser = argparse.ArgumentParser(description='Wordle Solver')
    parser.add_argument('solution', metavar='S', type=str, nargs='?',
                        help='Guess against a pre-selected solution')
    parser.add_argument('--method', type=str,
                        help='Select the method (max_entropy, min_max_pool, min_avg_pool).',
                        default='max_entropy')
    parser.add_argument('--source', type=str,
                        help='Select the data source (scowl, hello-wordl)',
                        default='scowl')
    parser.add_argument('--format', type=str,
                        help='Select the output format (n=number, c=color, u=unicode, b=unicode with black box)',
                        default='n')
    parser.add_argument('--pool', type=int, metavar='N',
                        help='Show the remaining pool size (and first N elements)',
                        default=-1)
    parser.add_argument('--randomize', action='store_const',
                        help='Consider only a sample of candidates for the next guess',
                        default=False, const=True)
    args = parser.parse_args()

    solver = Solver(source=args.source, method=args.method, randomize=args.randomize)
    try:
        if args.solution:
            pool = None
            for guess in solver.solve(args.solution, pool=args.pool):
                if args.pool >= 0:
                    guess, pool = guess
                x = "".join(map(str, check_guess(guess, args.solution)))
                print(f"{guess}: {output(x, args.format)}")
                if pool:
                    print(pool)
        else:
            print("2 = green, 1 = yellow, 0 = grey, eg. 01020")
            print("Manually override suggested guess, eg: 'guess01020'")
            solver.solve(pool=args.pool)
    except ValueError as e:
        print(e)

main()
