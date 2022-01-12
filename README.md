# wordle-solver
Sample implementation of an entropy-maximizing solver for Wordle

## Problem
The objective is to guess a five-letter word in as few guesses as possible (using most six). Each guess must be a valid word. The letters in the guess are marked green if they occur in the correct position, yellow if they occur somewhere else, and grey if they do ot occur anywhere.

## Solver
A near-optimal solution can be achieved by maximizing the Shannon entropy of the answer to each guess. This implementation can run in two modes:

1. In default (interactive) mode, it will print the optimal guess and read the answer from user input, continuing until it finds the correct answer.
2. When given an argument, it will simulate the game with the given solution.

## Usage

    ./main.py [<solution>]

## Word lists

The solver can use a custom word lists, which should
be placed in a line-separated text file in `data/`.

Separate word-lists for allowed guesses and solutions should
be named `{name}.guesses.txt` and `{name}.solutions.txt`;
a single file should be named `{name}.words.txt`, which
will be used for both guesses and solutions.

The following word lists are included in the repository:

- **scowl**: A list of English five-letter words sourced from [SCOWL](http://wordlist.aspell.net/).
- **hello-wordl**: The lists used by the [hello-wordl](http://foldr.moe/hello-wordl/) page maintained at https://github.com/lynn/hello-wordl.