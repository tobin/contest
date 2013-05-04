#!/usr/bin/python

# Algorithm:
#
# Eat all the motes we can.  When we get stuck, we can
# (1) Delete the problematic motes
# (2) Add a mote equal to our size - 1


# Returns: the number of edits needed
def solve(A, motes):
    # Eat all the motes we can
    while (len(motes) > 0) and (min(motes) < A):
        # Find an edible mote and eat it
        for ii in xrange(0, len(motes)):
            if motes[ii] < A:
                A += motes[ii]
                del motes[ii]
                break
    # If there are no motes to eat, we are done
    if len(motes) == 0:
        return 0
    # Now try fixing the problem    
    if A>1:
        return min(1 + solve(A, motes + [A-1]), 
                   len(motes))
    else:
        # If our mote already has the minimum size, we can't make any
        # new edible motes.  All we can do is delete all the remaining
        # motes that are too big for us to eat.
        return len(motes)


assert solve(2, [1, 2]) == 0
assert solve(2, [2, 1, 1, 6]) == 1
assert solve(10, [25, 20, 9, 100]) == 2
assert solve(1, [1, 1, 1, 1]) == 4
    

numbers = map(int, raw_input().split())
T = numbers.pop(0)

for t in xrange(0, T):
    numbers = map(int, raw_input().split())
    A = numbers.pop(0)
    N = numbers.pop(0)

    # next line contains the sizes of the N motes
    motes = map(int, raw_input().split())
    assert len(motes) == N

    result = solve(A, motes)

    print "Case #%d: %d" % (t+1, result)
