from random import sample
from collections import Counter
from core import Solver
import argparse

parser = argparse.ArgumentParser(description='Wordle Solver')

parser.add_argument('--method', type=str,
                        help='Select the method (max_entropy, min_max_pool, min_avg_pool).',
                        default='max_entropy')
parser.add_argument('--source', type=str,
                        help='Select the data source (scowl, hello-wordl, wordle)',
                        default='scowl')
parser.add_argument('--sample', type=int,
                        help='Sample size',
                        default=50)
args = parser.parse_args()

solver = Solver(method=args.method, source=args.source)
results = []

for word in sample(list(solver.solutions), args.sample):
    x = len(solver.solve(word))
    results.append(x)

def mean(z):
    return sum(z)/len(z)

def median(z):
    z = sorted(z)
    return mean(z[(len(z)-1)//2:(len(z)+2)//2])

def sd(z):
    m = mean(z)
    return (mean([(x - m)**2 for x in z])*(len(z)+1)/len(z))**0.5

r = results
c = Counter(r)
print(f"{args.method}: min={min(r)}, avg={mean(r)}, max={max(r)}, med={median(r)}, sd={sd(r)}")
for i in range(1, max(sorted(c.keys()))+1):
     print(f"{i}: {c[i]:2} {c[i]/args.sample*100:4.1f}% {'#'*int(c[i]/args.sample*50)}")
