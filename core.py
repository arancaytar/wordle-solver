import random
from collections import defaultdict, Counter
from math import log
import typing

def check_guess(guess: str, solution: str):
    answer = [0] * len(solution)
    if len(solution) != len(guess):
        raise ValueError(f"Guess {guess} must be {len(solution)} characters.")
    s, g = Counter(), defaultdict(list)
    for i, (a, b) in enumerate(zip(solution, guess)):
        if a == b:
            answer[i] = 2
        else:
            s[a] += 1
            g[b].append(i)
    for character, positions in g.items():
        for position in positions[:s[character]]:
            answer[position] = 1
    return tuple(answer)

class Opt:
    def __init__(self, max=False):
        self.key = set()
        self.value = None
        self.sign = -1 if max else 1

    def check(self, key, value):
        if self.value is None or (value * self.sign) < (self.value * self.sign):
            self.key = {key}
            self.value = value
            return True
        elif (value * self.sign) <= (self.value * self.sign):
            self.key.add(key)
        return False

    def __str__(self):
        return f"{self.key} {self.value}"

def entropy(z: typing.Iterable, b=2):
    n = sum(z)
    return log(n,b) - sum(v * log(v,b) for v in z) / n

def reduce(candidates, guess):
    tree = defaultdict(list)
    for solution in candidates:
        tree[check_guess(guess, solution)].append(solution)
    return tree


def maximize_entropy(solutions, guesses=None):
    # With at most possibilities, brute-force is optimal.
    if len(solutions) <= 2:
        return solutions[0]

    max_entropy = Opt(max=True)
    for guess in guesses or solutions:
        tree = Counter({x: len(y) for x, y in reduce(solutions, guess).items()})
        max_entropy.check(guess, entropy(tree.values()))
    if guesses:
        best = set(guesses) & max_entropy.key
        if best:
            return sorted(best)[0]
    print(max_entropy)
    return sorted(max_entropy.key)[0]

class Solver:
    def __init__(self):
        self.words = open('words.txt').read().strip().split("\n")
        pairs = (tuple(line.split()[:2]) for line in open('lookup-1.txt').read().strip().split("\n"))
        self.lookup = dict((x, y) for x, y in pairs)

    def solve(self, solution: str = None):
        guesses = []
        read_answer = (
            (lambda guess: check_guess(guess, solution)) if solution
            else (lambda guess: tuple(map(int, input(f"{guess}: ").strip())))
        )
        guess = 'tares'  # first guess.
        guesses.append(guess)
        reduced = reduce(self.words, guess)
        answer = read_answer(guess)

        if set(answer) == {2}:
            return guesses  # solved in one guess

        solutions = reduced[answer]
        if not solutions:
            raise ValueError("Answers not consistent with any word in the list.")
        # use a lookup table for the second guess (much faster, and only requires 243 entries)
        guess = self.lookup["".join(map(str, answer))]
        guesses.append(guess)
        reduced = reduce(solutions, guess)

        while True:
            answer = read_answer(guess)
            if set(answer) == {2}:  # correct, stop
                return guesses

            solutions = reduced[answer]
            if not solutions:
                raise ValueError("Answers not consistent with any word in the list.")
            #print(f"{solutions[:5]} and {max(0, len(solutions) - 5)} others")

            guess = maximize_entropy(solutions, self.words)
            guesses.append(guess)
            reduced = reduce(solutions, guess)

            if len(solutions) <= 1 and solution: # only one possibility left, stop
                return guesses

