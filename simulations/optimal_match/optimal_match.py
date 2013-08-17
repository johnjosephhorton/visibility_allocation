import os 
import sys
import math 
import numpy as np 
import random 

def m(b,q): 
    """Match probability when a seller with a per-match 
probability of match q gets exposed to b buyers."""
    return 1.0 - math.exp(-b*q) 

def mm(b,q): 
    """Gets the marginal effect of b on m. 
    """
    return q*math.exp(-b*q) 

def create_row(Q, i, n): 
    """Creates the i'th row of an n row matrix in the system of linear
    equations M*x = b. 
    """
    if i < n: 
        return [0.0]*(i - 1) + [ -Q[i - 1], Q[i]] + [0]*(n - 1 - i)
    else:
        return [1.0]*n

def create_matrix(Q,n):
    """Creates the actual matrix M in the M*x = b formulation."""
    return np.array( [create_row(Q,i,n) for i in range(1,n + 1)] )

def create_column(Q,n,A): 
    """ Creates the column 'b' in the M*x = b formulation of a system of 
    linear equations. 
    """
    top_part = [math.log(Q[i + 1]/Q[i]) for i in range(n-1)]
    top_part.append(A)
    return np.array(top_part)

def solve_linear(Q,A): 
    """ 
    Solves the assocaited system of linear equations.  
    """
    n = len(Q) 
    M = create_matrix(Q, n)
    v = create_column(Q, n, A)
    return np.linalg.solve(M, v) 

def shadow_value(bstar, Q):
    """
    At the optimum, all sellers offer the same marginal benefit (i.e., shadow value).
    For simplicity, this just calculates the slope for the first seller. 
    """
    return mm(bstart[0],Q[0])

def find_goat(Q, A):
    """
    The "goat" is cadet ranked last in their class at USMA but still manages to 
    graduate. This function finds the lowest q seller that still gets a positive 
    amount of visibility. 

    NOTE: Right now, this is just iterates from the highest to lowest ranked, solving
    the linear program each time. There are two obvious ways to optimize this: 

    a) Use binary search (obviously)
 
    b) I'm guessing some kind of memoization of the solution to the system of 
    k linear equations could speed up calculation of the the k + 1 system.  
    """
    n = len(Q) 
    for index in range(2,n):
        Qsub = [Q[y] for y in range(index)]
        sol = solve_linear(Qsub, A)
        if sol[-1] < 0.0: 
            return index - 1 
    return index

if __name__ == '__main__':
    n, A = 500, 850
    print("Running demo for n = %s, A = %s" % (n, A))
    Q = [random.random() for y in range(n)]
    Q.sort()
    Q.reverse() 
    print("Looking for goat")
    goat = find_goat(Q,A)
    print("Goat (last seller to get any visibility) is %s " % goat)
    print("Optimal allocation is:")
    astar = solve_linear(Q[:goat], A)
    for index, a in enumerate(astar):
        if (index < 10) or (index > (goat - 10)):
            print("Seller: %s gets allocation %s" % (index + 1, a))
        else:
            if index % 10 == 0:
                print "(skipping some)" 
