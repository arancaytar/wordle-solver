from core import Solver, reduce


def first(solver):
    return solver.optimize(solver.words)

def second(solver, first_guess):
    reduced = reduce(solver.words, first_guess)
    optimal = {}
    for response, pool in reduced.items():
        optimal[response] = solver.optimize(pool)
    return optimal

def build_table(method):
    solver = Solver(method)
    first_guess = first(solver)
    table = second(solver, first_guess)
    output = [f"{''.join(map(str, response))} {guess}" for response, guess in sorted(table.items())]
    output = "\n".join(output)
    return f"{first_guess}\n{output}"

def main(method):
    open(f"lookup.{method}.txt", 'w').write(build_table(method))

