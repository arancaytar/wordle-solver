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
    return "".join(map(str, answer))

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

def print_pool(solutions, size):
    elements = f"{', '.join(solutions[:size])}"
    if size >= len(solutions):
        return f"{elements} remaining"
    elif size:
        return f"{elements} and {len(solutions)} others remaining"
    else:
        return f"{len(solutions)} remaining"


def get_source(source):
    def get_words(file):
        return open(file).read().strip().split("\n")
    try:
        guesses = solutions = get_words(f"data/{source}.words.txt")
    except FileNotFoundError:
        guesses = get_words(f"data/{source}.guesses.txt")
        solutions = get_words(f"data/{source}.solutions.txt")
    return guesses, solutions


class Solver:
    def __init__(self, source, method, skip_lookup=False):
        self.guesses, self.solutions = get_source(source)
        self.method = method
        self.first = self.second = None

        if not skip_lookup:
            try:
                lines = open(f"lookup/{source}.{method}.txt").read().strip().split("\n")
                self.first = lines[0]
                pairs = (tuple(line.split()[:2]) for line in lines[1:])
                self.second = dict((x, y) for x, y in pairs)
            except FileNotFoundError as e:
                print(e)
                print("Warning: Lookup table not found. First two guesses will be slow.")

    def optimize(self, solutions):
        return optimize(solutions, self.guesses, self.method)

    @staticmethod
    def read_answer(guess, solution):
        if solution:
            return check_guess(guess, solution), guess
        answer = input(f"{guess}: ").strip()
        match len(answer):
            case 5:
                return answer, guess
            case 10:
                return answer[5:], answer[:5]
            case _:
                raise ValueError("Answer must be 5 digits, or 5 letters and 5 digits.")

    def solve(self, solution: str = None, pool=-1):
        guesses = []
        solutions = self.solutions

        guess = None

        if self.first:
            guess = self.first
            answer, guess = self.read_answer(guess, solution)
            if guess != self.first:
                print("Warning: Overriding first guess; discarding lookup table. Next guess is slow.")
            guesses.append(guess)
            reduced = reduce(solutions, guess)
            if set(answer) == {"2"} and guess in self.solutions:
                return guesses  # solved in one guess
            solutions = reduced[answer]
            if not solutions:
                raise ValueError("Answers not consistent with any word in the list.")
            if pool >= 0:
                p = print_pool(solutions, pool)
                if solution:
                    guesses[-1] = (guesses[-1], p)
                else:
                    print(p)
            if self.second and self.first == guess:
                # use a lookup table for the second guess (much faster, and only requires 243 entries)
                # but only use it if we kept the first guess.
                guess = self.second[answer]
            else:
                guess = None

        if guess is None:
            guess = self.optimize(solutions)

        while True:
            answer, guess = self.read_answer(guess, solution)
            guesses.append(guess)
            reduced = reduce(solutions, guess)
            if set(answer) == {"2"}:  # correct, stop
                return guesses

            solutions = reduced[answer]
            if not solutions:
                raise ValueError("Answers not consistent with any word in the list.")
            if pool >= 0:
                p = print_pool(solutions, pool)
                if solution:
                    guesses[-1] = (guesses[-1], p)
                else:
                    print(p)
            guess = self.optimize(solutions)

