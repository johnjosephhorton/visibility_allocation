# John Horton 
# January 4th, 2011
# oDesk 

import time, random

NOTES = """ 
This code implements the "sequential market"
approach to the algorithm problem.   

We probably don't want to store a simplex of length a million -
we probably want to create a data structure like this:

{(0.0,.1):{1,2,3}, (1.0, 2.0):{4,5,6}...}

I.e, bin the workers by merits, then do a weighted selection of the bins, then select randomly
from everyone in that bin. This will scale much better---like O(1) I think once the partiion of
[0,1] is sufficiently refined.  
"""

def cumsum(l):
    return [sum(l[:(1+i)]) for i in range(len(l))]

def random_choice(options, weights):
    """Options is vector of options and weights are the weights you want the options sampled at.""" 
    r = random.random()
    for i, c in enumerate(cumsum(weights)):
        if r <= c:
            return options[i]

def norm(l): return [y/sum(l) for y in l]
            
def gen_rank(names, merits):
    """This function returns a ranking of users according to the sequential 
       market approach. We assign positions in value descending rank, i.e., 
       position 1 is worth more than 2, which is worth more than 3 etc.  

       'names' is the name of the names of the agents to match 
       'merits' is a simplex (i.e., a vector sum(l)
       of floats that sums to 1, with no value less than 0 or greater than 1
       
       The function takes a random draw from 'names,' weighted by their merits. The 
       drawn agent is given that position. The winner is removed from 
       'names' and 'merits' and then the function is called on the smaller
       group. Once no one is left, the recursion terminates.   

       Need to re-write this so it's not recursive. I wrote it recursively because I'm shaky
       about what happens when you mutate vectors in Python in a loop. 
    """
    if len(names) > 1:
        winner = random_choice(range(len(names)), merits)
        winner_name = names.pop(winner)
        re_scale_factor = 1.0/(1.0-merits.pop(winner))
        merits = [y*re_scale_factor for y in merits]
        return [winner_name] + gen_rank(names, merits)
    else: 
        return [names[0]]


# Non-recursive version
def gen_rank2(names, merits, verbose = False):
    assert(len(names)==len(merits))
    name_to_budget = dict(zip(names,merits))
    matched = []
    assignments = dict(zip(names, [None]*len(names)))
    num_positions = len(names) 
    for p in range(num_positions):
        un_matched = [agent for agent in names if agent not in matched]
        if verbose:
            print "Unmatched:", un_matched, "Matched:", matched  
        un_matched_budgets = norm([name_to_budget[agent] for agent in un_matched])
        winner = random_choice(range(len(un_matched)), un_matched_budgets)
        assignments[un_matched[winner]] = p
        matched.append(un_matched[winner])
    return assignments 


#n = 10
#B = norm([random.random() for y in range(n)])
#ranking = gen_rank(range(n), B)

if __name__ == '__main__':
  n = 2000
  B = norm([random.random() for y in range(n)])

  start = time.time()
  ranking2 = gen_rank2(range(n),B)
  end = time.time()

  print "It took %s seconds to do %s matches" % (str(round(end - start,2)), n)

