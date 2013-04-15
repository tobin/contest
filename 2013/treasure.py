#!/usr/bin/python

# Google Code Jam 2013 - Qualification Round - Problem D
#
# This code is able to solve the "small" input correctly in less than
# 0.1 seconds, and the "large" input (also correctly) in about 10
# seconds.
#
# Tobin Fricke 2013-04-13

import sys
from collections import Counter

debug = 0

def enough_keys_exist(chests, keys, key_req, keys_inside):
    keys_needed = Counter([key_req[c] for c in chests])

    keys_available = keys

    for c in chests:
        keys_available = keys_available + keys_inside[c]

    for k in keys_needed:
        if keys_available[k] < keys_needed[k]:
            if debug:
                print "Need %d of key %d but only have %d" % (keys_needed[k], k, keys_available[k])
            return False  # no solution exists
    return True

# Verify that all needed key types may still be reachable
def still_possible(chests, keys, key_req, keys_inside):
    def openable(chest):
        return key_req[chest] in keys

    openable_chests = filter(openable, chests)
    while openable_chests:
        for chest in openable_chests:
            keys = keys + keys_inside[chest]
            chests = chests - {chest}
        openable_chests = filter(openable, chests)
    return not chests

# Backtracking depth-first search
def solve(chests, keys, key_req, keys_inside):

    # If no more chests remain to be opened, then a solution has been found.
    if not chests:
        return True, []

    # Check whether we should pursue this branch at all
    if not still_possible(chests, keys, key_req, keys_inside):
        return False, None

    # Try to open chests...
    for c in sorted(list(chests)):
        k = key_req[c]
        if k in keys:
            n = keys_inside[c]
            success, solution = solve(chests - {c}, (keys - Counter({k})) + n, key_req, keys_inside)
            if success:
                return True, [c] + solution

    return False, None


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

    # First check the global constraint to make sure a solution isn't obviously impossible
    if not enough_keys_exist(chests, keys, key_req, keys_inside):
        solution_exists = False
    else:
        # Now begin the search:
        solution_exists, solution = solve(frozenset(chests), keys, key_req, keys_inside)

    if solution_exists:
        print " ".join(map(str,solution))
    else:
        print "IMPOSSIBLE"

    sys.stdout.flush()


