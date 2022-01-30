import argparse
from core import Solver, reduce


def first(solver):
    return solver.optimize(solver.solutions)


def second(solver, first_guess):
    reduced = reduce(solver.solutions, first_guess)
    optimal = {}
    for response, pool in reduced.items():
        optimal[response] = solver.optimize(pool)
        print(".", end="", flush=True)
    return optimal


def build_table(solver):
    print("Optimizing first guess... ", end="", flush=True)
    first_guess = first(solver)
    print(first_guess)
    print("Optimizing second guess...", end="", flush=True)
    table = second(solver, first_guess)
    print("Done")
    output = [f"{''.join(map(str, response))} {guess}" for response, guess in sorted(table.items())]
    output = "\n".join(output)
    return f"{first_guess}\n{output}"


def main():
    parser = argparse.ArgumentParser(description='Wordle Solver -- Prebuild tables')
    parser.add_argument('source', type=str,
                        help='Select the data source. Files should be in data/{name}.(guesses,solutions|words).txt')
    parser.add_argument('--method', type=str,
                        help='Select the method (max_entropy, min_max_pool, min_avg_pool).',
                        default='all')
    args = parser.parse_args()

    methods = ('max_entropy', 'min_avg_pool', 'min_max_pool') if args.method == 'all' else [args.method]
    for method in methods:
        solver = Solver(source=args.source, method=method, skip_lookup=True, randomize=False)
        table = build_table(solver)
        open(f"lookup/{args.source}.{method}.txt", 'w').write(table)

main()
