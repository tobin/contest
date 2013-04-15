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

# chests: set of unopened chests
# keys: multiset of keys that I have
# keys_req: dictionary chest-->key req
# keys_inside: dictionary chest-->set of keys inside

# Really, this only needs to be called once for a given problem
def impossible(chests, keys, key_req, keys_inside):
    keys_needed = Counter([key_req[c] for c in chests])
    keys_available = keys
    for c in chests:
        keys_available = keys_available + keys_inside[c]
    for k in keys_needed:
        if keys_available[k] < keys_needed[k]:
            if debug:
                print "Need %d of key %d but only have %d" % (keys_needed[k], k, keys_available[k])
            return 1  # impossible
    return 0 # not impossible

# see if we can succeed with "simultaneous unlocking"    
def possible(chests, keys, key_req, keys_inside):
    def openable(chest):
        return key_req[chest] in keys
    # Open everything we can without consuming keys:
    o = filter(openable, chests)
    while o:
        for c in o:
            keys = keys + keys_inside[c]
            chests = chests - {c}
        o = filter(openable, chests)
    return not chests

def solve(chests, keys, key_req, keys_inside):
    if not possible(chests, keys, key_req, keys_inside):
        return 0

    if not chests:
        return []

    for c in sorted(list(chests)):
        k = key_req[c]
        if k in keys:
            n = keys_inside[c]
            result = solve(chests - {c}, (keys - Counter({k})) + n, key_req, keys_inside)
            if isinstance(result, list):
                return [c] + result

    return 0

# T: number of test cases
T = int(raw_input())
if debug:
    print "=== %d test cases ===" % T

for t in range(0,T):
    if debug:
        print ""
    sys.stdout.write("Case #%d: " % (t+1))
    if debug:
        print ""
    # K: number of keys that I have
    # N: number of chests
    (K,N) = map(int, raw_input().split())

    # "This is followed by a line containing K integers, representing
    # the types of the keys that you start with."
    keys = Counter(map(int, raw_input().split()))
    if debug:
        print "I have these keys: " + str(keys)

    # After that, there will be N lines, each representing a single
    # chest. Each line will begin with integers Ti and Ki, indicating
    # the key type needed to open the chest and the number of keys
    # inside the chest. These two integers will be followed by Ki more
    # integers, indicating the types of the keys contained within the
    # chest.
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
        if numbers:
            print "Error: unconsumed input: " + str(numbers)
    chests = set(range(1, N+1))
    sys.stdout.flush()
    if impossible(chests, keys, key_req, keys_inside):
        solution = 0
    else:
        solution = solve(frozenset(chests), keys, key_req, keys_inside)
    if isinstance(solution, list):
        print " ".join(map(str,solution))
    else:
        print "IMPOSSIBLE"
    sys.stdout.flush()


