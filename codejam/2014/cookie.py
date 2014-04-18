#!/usr/bin/python
# Tobin Fricke 2014-04-12 Berlin

import sys

T = int(sys.stdin.readline())

debug = False

for t in range(0, T):

    vals = sys.stdin.readline().rstrip().split(' ')
    C = float(vals[0])  # Cost of a cookie farm
    F = float(vals[1])  # Output rate of cookie farm in cookies/sec
    X = float(vals[2])  # Number of cookies needed to win

    sys.stdout.write("Case #%d: " % (t + 1))

    if debug:
        print "C = %f, F = %f, X = %f\n" % (C,F,X)

    # Cookie farm pays for itself in C/F seconds. 

    # First cookie farm can be bought after C/2 seconds.
    # Next cookie farm after C/(2+F)

    # Interval between (n-1)th and nth cookie farm is
    # C/(2+nF) seconds.

    # Is there a closed form solution? Maybe but for now we'll be
    # lazy.

    S = 0  # Score, i.e. number of cookies
    R = 2  # Rate of production, cookies per second
    T = 0  # Elapsed time
    
    eps = 1e-6

    while S + eps < X:
        if debug:
            print "Time %f, Cookies %f, Rate %f cookies/sec " % (T,S,R)

        # Consider buying a factory if possible

        if (S + eps >=C) and ((X-S)/R > (X-S+C)/(R+F)):
            # The factory will make us win sooner.  Buy it.
            if debug:
                print "Buying a factory"
            S -= C  
            R += F

            # Advance to the next possible factory buying time or win
            dt = min((X-S)/R, C/R)

        else:
            if S + eps >= C:
            # If we didn't buy a factory this time, we won't but any more
                if debug: 
                    print "Advancing to win"

                dt = (X-S)/R
            else:
                if debug: 
                    print "Advancing to next factory buying opportunity (or win)"
                dt = min((X-S)/R, C/R)

        T += dt        # Total elapsed time
        S += dt * R    # Total number of cookies we'll have

    print T
