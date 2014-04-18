#!/usr/bin/python
# Tobin Fricke 2014-04-12 Berlin

import sys

T = int(sys.stdin.readline())

for t in range(0,T):
    sys.stdout.write("Case #%d: " % (t+1))

    A = int(sys.stdin.readline())
    linesA = [[],[],[],[]]
    for ii in range(0,4):
        linesA[ii] = set(map(int, sys.stdin.readline().rstrip().split(' ')))

    B = int(sys.stdin.readline())
    linesB = [[],[],[],[]]
    for ii in range(0,4):
        linesB[ii] = set(map(int, sys.stdin.readline().rstrip().split(' ')))

    rslt = linesA[A-1] & linesB[B-1]
    if len(rslt) == 0:
        print "Volunteer cheated!"
    elif len(rslt) > 1:
        print "Bad Magician!"
    else:
        print list(rslt)[0]




    
    
