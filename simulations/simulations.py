'''
Created on Feb 5, 2012

@author: papadimitriou
'''

import random, time, sys
from math import sqrt
#import matplotlib.pyplot as plt
from collections import defaultdict
from tree_based_random_draw import efficient_gen_rank
from sequential_market import gen_rank2


def zipfian(n, s=2.0):
  return [1 / (i ** float(s)) for i in range(1, n + 1)]
  

def write_numbers(fn, l):
  f = open(fn, 'w')
  for num in l:
    f.write('%s\n' % (str(num)))
  f.close()
  

PERFORMANCE = False

# Performance simulations
if PERFORMANCE:
  f = open('results/performance.csv', 'w')
  for n in (10, 20, 50, 100, 200, 500, 1000):
    random.seed(n)
    merits = [random.random() for y in range(n)]
    write_numbers('data/performance/merits.' + str(n) + '.csv', merits)
    names = range(n)
    visibilities = zipfian(n, s=1.35)
    write_numbers('data/performance/visibilities.' + str(n) + '.csv', visibilities)
    runtimes = []
    for assign in (efficient_gen_rank, gen_rank2):
      start = time.time()
      assignemnt = assign(names, merits)
      end = time.time()
      runtimes.append(end - start)
    f.write(','.join(map(str, [n] + runtimes)) + '\n')
  f.close()
  sys.exit(0)


# Accuracy simulations
def compute_visibilities(assign, merits, n, m):
  total_visibilities = [0.0] * n
  for i in range(m):
    assignment = assign(names, merits)
    for name, position in assignment.iteritems():
      total_visibilities[name] += visibilities[position]
  return total_visibilities  


def static_assign(names, merits):
  assert(len(names) == len(merits))
  assignment = dict([(name, i) for i, (merit, name) in enumerate(sorted(zip(merits, names), reverse=True))])
  return assignment

n = 1000
m = 10000                 # number of different rankings
random.seed(10)
  
# Set visibilities
s = 1.35
visibilities = zipfian(n, s)
write_numbers('data/approximation/visibilities.csv', visibilities)

f = open('results/approximation.csv', 'w')
for alpha in (100, 10, 5, 0.99, 0.5, 0.1):
#for alpha in (0.5, 0.11):
  # Set merits
  random.seed(alpha * 10)
  merits = [random.paretovariate(alpha) for y in range(n)]
  write_numbers('data/approximation/merits.' + str(alpha) + '.csv', visibilities)
  names = range(n)
  errors = []
  for assign in (efficient_gen_rank, static_assign):
    total_visibilities = compute_visibilities(assign, merits, n, m)
    # Calculate relative values
    sum_merits = sum(merits) 
    relative_merits = map(lambda x : x / sum_merits, merits)
    sum_visibilities = sum(total_visibilities)
    relative_visibilities = map(lambda x : x / sum_visibilities, total_visibilities)
    # Errors
    error = sqrt(sum([(x-y) ** 2 for x, y in zip(relative_merits, relative_visibilities)]) / float(n))
    errors.append(error)
  print ','.join(map(str, ([alpha] + errors)))
  f.write(','.join(map(str, ([alpha] + errors))) + '\n')
f.close()
  

#maxxy = max(max(relative_visibilities), max(relative_merits))
#plt.plot(relative_merits, relative_visibilities,'.b')
#plt.plot([0, maxxy], [0, maxxy], 'r')
#plt.show()



#fn = 'results/accuracy.n%d.m%d.s%d.csv' % (n, m, s)
#f = open(fn, 'w')
#for budget, total_value in zip(merits, total_visibilities):
#  f.write('%f,%f\n' % (budget, total_value)) 
#f.close()
  

  
  
