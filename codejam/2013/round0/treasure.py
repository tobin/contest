#!/usr/bin/python

# Google Code Jam 2013 - Qualification Round - Problem D
#
# This code is able to solve the "small" input correctly in less than
# 0.1 seconds, and the "large" input (also correctly) in about 1.5 
# seconds on a Thinkpad T410.
#
# Tobin Fricke 2013-04-13

import sys
from collections import Counter

debug = 0

# For some test cases there are not sufficient keys present in the
# problem to unlock all of the chests.  This can be checked trivially
# before beginning the solution search.
def enough_keys_exist(chests, keys, key_req, keys_inside):
    keys_needed = Counter([key_req[c] for c in chests])

    keys_available = keys

    for c in chests:
        keys_available += keys_inside[c]

    for k in keys_needed:
        if keys_available[k] < keys_needed[k]:
            if debug:
                print "Need %d of key %d but only have %d" % (keys_needed[k], k, keys_available[k])
            return False  # no solution exists
    return True

# Verify that all needed key types may still be reachable
def still_possible(chests, keys, key_req, keys_inside):
    keys = set(keys)
    chests = chests.copy()

    def openable(chest):
        return key_req[chest] in keys

    openable_chests = filter(openable, chests)
    while openable_chests:
        for chest in openable_chests:
            keys |= set(keys_inside[chest])
            chests.remove(chest)
        openable_chests = filter(openable, chests)
    return not chests

# Greedy, iterative algorithm
def solve(chests, keys, key_req, keys_inside):

    # First check the global constraint to make sure a solution isn't obviously impossible
    if not enough_keys_exist(chests, keys, key_req, keys_inside):
        return False, None

    # Make sure all keys are potentially reachable
    if not still_possible(chests, keys, key_req, keys_inside):
        return False, None

    solution = []

    for position in range(0, len(chests)):
        for c in sorted(chests):
            # Skip this chest if we can't open it:
            if not key_req[c] in keys:
                continue
            # Open the chest:
            keys[key_req[c]] -= 1
            chests.remove(c)
            keys += keys_inside[c]
            # Make sure there's still a way to obtain all needed keys:
            if still_possible(chests, keys, key_req, keys_inside):
                break
            # Re-wind before trying the next chest
            chests.add(c)
            keys -= keys_inside[c]
            keys[key_req[c]] += 1
        else:
            # Could not open any chest --> no solution
            # This code will never be reached!
            print "FAIL"
            return False, None  

        solution.append(c)

    return True, solution


# "The first line of the input gives the number of test cases, T."
T = int(raw_input())
if debug:
    print "=== %d test cases ===" % T

# "T test cases follow."
for t in range(0,T):
    if debug:
        print ""
    sys.stdout.write("Case #%d: " % (t+1))
    if debug:
        print ""

    # "Each test case begins with a single line containing two
    # positive integers K and N, representing the number of keys you
    # start with and the number of chests you need to open."
    (K,N) = map(int, raw_input().split())

    # "This is followed by a line containing K integers, representing
    # the types of the keys that you start with."
    keys = Counter(map(int, raw_input().split()))
    if debug:
        print "I have these keys: " + str(keys)

    # "After that, there will be N lines, each representing a single
    # chest. Each line will begin with integers Ti and Ki, indicating
    # the key type needed to open the chest and the number of keys
    # inside the chest. These two integers will be followed by Ki more
    # integers, indicating the types of the keys contained within the
    # chest."
    key_req = {};
    keys_inside = {};
    for n in range(1, N+1):
        numbers = map(int, raw_input().split())
        Ti = numbers.pop(0)
        Ki = numbers.pop(0)
        key_req[n] = Ti;
        keys_inside[n] = Counter({})
        for k in range(0, Ki):
            keys_inside[n] = keys_inside[n] + Counter([numbers.pop(0)])
        if debug:
            print ("Chest #%d needs key %d, contains %d keys: " % (n, Ti, Ki)) + str(keys_inside[n])
    chests = set(range(1, N+1))
    sys.stdout.flush()

    solution_exists, solution = solve(chests, keys, key_req, keys_inside)

    if solution_exists:
        print " ".join(map(str,solution))
    else:
        print "IMPOSSIBLE"

    sys.stdout.flush()
