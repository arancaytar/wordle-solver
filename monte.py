from random import sample

from core import Solver

solvers = {method: Solver(method) for method in ('max_entropy', 'min_max_pool', 'min_avg_pool')}
results = {method: [] for method in solvers}

for word in sample(solvers['max_entropy'].words, 500):
    print(word,end=' ')
    for method in solvers:
        x = len(solvers[method].solve(word))
        print(x,end=' ')
        results[method].append(x)
    print()

def mean(z):
    return sum(z)/len(z)

def median(z):
    z = sorted(z)
    return mean(z[(len(z)-1)//2:(len(z)+2)//2])

def sd(z):
    m = mean(z)
    return (mean([(x - m)**2 for x in z])*(len(z)+1)/len(z))**0.5

for method, r in results.items():
    print(f"{method}: min={min(r)}, avg={mean(r)}, max={max(r)}, med={median(r)}, sd={sd(r)}")