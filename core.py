import random
from collections import defaultdict, Counter
from math import log
import typing
from typing import Dict


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

def optimize(solutions, guesses=None, method='max_entropy'):
    # With at most possibilities, brute-force is optimal.
    if len(solutions) <= 2:
        return solutions[0]

    if method == 'max_entropy':
        optimal = Opt(max=True)
    else:
        optimal = Opt()

    for guess in guesses or solutions:
        tree = Counter({x: len(y) for x, y in reduce(solutions, guess).items()})
        match method:
            case 'min_max_pool':
                score = max(tree.values())
            case 'min_avg_pool':
                score = sum(tree.values()) / len(tree.values())
            case 'max_entropy':
                score = entropy(tree.values())
            case _:
                score = entropy(tree.values())
        optimal.check(guess, score)
    if guesses:
        best = set(guesses) & optimal.key
        if best:
            return sorted(best)[0]
    print(optimal)
    return sorted(optimal.key)[0]


class Solver:

    def __init__(self, method='max_entropy'):
        self.words = open('words.txt').read().strip().split("\n")
        self.method = method
        self.first = self.second = None
        try:
            lines = open(f"lookup.{method}.txt").read().strip().split("\n")
            self.first = lines[0]
            pairs = (tuple(line.split()[:2]) for line in lines[1:])
            self.second = dict((x, y) for x, y in pairs)
        except FileNotFoundError as e:
            print(e)
            print("Warning: Lookup index not found. Solver will run very slowly.")

    def optimize(self, solutions):
        return optimize(solutions, self.words, self.method)

    def solve(self, solution: str = None):
        guesses = []
        read_answer = (
            (lambda g: check_guess(g, solution)) if solution
            else (lambda g: tuple(map(int, input(f"{g}: ").strip())))
        )

        solutions = self.words

        if self.first and self.second:
            guess = self.first
            guesses.append(guess)
            reduced = reduce(solutions, guess)
            answer = read_answer(guess)

            if set(answer) == {2} and guess in self.words:
                return guesses  # solved in one guess
            solutions = reduced[answer]
            if not solutions:
                raise ValueError("Answers not consistent with any word in the list.")
            # use a lookup table for the second guess (much faster, and only requires 243 entries)
            guess = self.second["".join(map(str, answer))]
        else:
            guess = self.optimize(solutions)

        guesses.append(guess)
        reduced = reduce(solutions, guess)

        while True:
            answer = read_answer(guess)
            if set(answer) == {2}:  # correct, stop
                return guesses

            solutions = reduced[answer]
            if not solutions:
                raise ValueError("Answers not consistent with any word in the list.")

            guess = self.optimize(solutions)
            guesses.append(guess)
            reduced = reduce(solutions, guess)

            if len(solutions) <= 1 and solution:  # only one possibility left, stop
                return guesses

