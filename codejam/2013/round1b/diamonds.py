#!/usr/bin/python

# Google Code Jam
# Round 1B
#
# 2013-05-04
#
# This program is an insane overkill approach to the problem.  As one
# might expect, the result of piling up a bunch of diamonds all
# dropped from the same X position is a big triangular heap of
# diamonds.  The only uncertainty is how many diamonds are on the right
# and left uncompleted sides of the heap.  This we can figure out with
# simple probability using the binomial formula.

# Because I was dumb, I didn't actually think about the above, and
# instead implemented the straight-forward diamond-dropping simulator.
# The solution is kind of cool, because it maintains an "ensemble"
# which maps all possible configurations after N diamond drops to the
# probability of those configurations occurring, and it operates on
# those ensembles.
#
# This is totally unnecessary and it's too slow to operate on anything
# but small inputs.

import sys
import matplotlib.pyplot as plt
import numpy as numpy

def combine_ensembles(a, b):
    for x in b:
        if x in a:
            a[x] += b[x]
        else:
            a[x] = b[x]
    return a

def occupied(conf, x, y):
    return (x,y) in conf

memo = dict()

# An ensemble is a mapping from configurations to probabilities
def add_diamond(conf, x, y):    
    problem = (conf, x, y)
    if problem in memo:
        sys.stdout.write('+')
        return memo[problem]
    sys.stdout.write('x')
    #print "Adding a diamond to " + str(conf) + " at (%d, %d) " % (x,y)
    # Add a diamond at position x, y.  Return resulting ensemble

    # Fall until blocked directly below, or have hit the ground
    while (y>0):
        if occupied(conf, x-1, y-1) and occupied(conf, x+1, y-1):
            break # we're stuck
        elif occupied(conf, x-1, y-1) and not occupied(conf, x+1, y-1):
            # slide to the right
            x += 1
            y -= 1
        elif not occupied(conf, x-1, y-1) and occupied(conf, x+1, y-1):
            # slide to the left
            x -= 1
            y -= 1
        elif occupied(conf, x, y-2):  # Now we're free -- maybe -- to hop down two spaces
            # Here we have to do a non-deterministic branch.  We already know that both of
            # these spots are free - otherwise we would have had to slide.
            a = add_diamond(conf, x-1, y-1) 
            b = add_diamond(conf, x+1, y-1)
            for x in a: a[x] *= 0.5
            for x in b: b[x] *= 0.5
            result = combine_ensembles(a, b)
            memo[problem] = result
            return result
        else:
            # we're free to fall directly downwards
            y -= 2
    # Now we're either stuck or in the ground.  This is a definite result.
    assert (x,y) not in conf
    conf = set(conf) | {(x,y)}
    result = { frozenset(conf) : 1.0 }
    memo[problem] = result
    return result
        
def calculate_probability(ensemble, x, y):
    # Find the probability that there's a diamond at (x,y) given
    # ensemble of configurations
    p = 0
    for conf in ensemble:
        if (x,y) in conf:
            p += ensemble[conf]
    return p

def simulate(X, Y, N):
    # The initial state definitely contains nothing:
    ensemble = { frozenset([]) : 1.0  } 
    # Now add diamonds one-by-one:
    for n in xrange(0, N):
        sys.stdout.write(".")
        sys.stdout.flush()
        new_ensemble = dict()
        for conf in ensemble:
            max_height = max([y for (x,y) in conf]) if conf else 0
            max_height += (max_height % 2)   # must be even!
            e = add_diamond(conf, 0, max_height + 2)
            for c in e: 
                e[c] *= ensemble[conf]   # multiply by the prior
                if c in new_ensemble:
                    new_ensemble[c] += e[c]
                else:
                    new_ensemble[c] = e[c]
#            new_ensemble = combine_ensembles(new_ensemble, e)   # add to our collection
        ensemble = new_ensemble
        if False:
            print "Currently tracking %d configurations: " % len(ensemble)
            print "Most probable has prob  = %f" % max(ensemble.values())
            print "Least probable has prob = %g" % min(ensemble.values())
            print "Ratio                   = %g" % (max(ensemble.values()) / min(ensemble.values()))
            print "Sum of probabilities    = %f" % sum(ensemble.values())
            c = ensemble.keys()[0]
            x = map(lambda coord : coord[0], c)
            y = map(lambda coord : coord[1], c)
            plt.plot(x, y, 'd')
            plt.grid('on')
            plt.xlim([-20, 20])
            plt.ylim([-1, 20])
            plt.show()

        # Cull ensemble, removing configurations that are very improbable
        cull = filter(lambda c : ensemble[c] < 1e-5, ensemble)
        for unwanted_key in cull:
            del ensemble[unwanted_key]
        #print ensemble
        # If a block already is known to land at the chosen spot, we
        # can quit now:
        p = calculate_probability(ensemble, X, Y)
        if p > (1.0 - 1e-6):
            return p

    return p
        
        
        
def main():
    numbers = map(int, raw_input().split())
    T = numbers.pop(0)

    for t in xrange(0, T):
        numbers = map(int, raw_input().split())
        N = numbers.pop(0)
        X = numbers.pop(0)
        Y = numbers.pop(0)

        print "Case #%d: "        
#        print "N = %d, X = %d, Y = %d" % (N, X, Y)
        result = simulate(X, Y, N)
        print result


main()
