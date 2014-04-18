#!/usr/bin/python
# Tobin Fricke 2014-04-12 Berlin

import sys

T = int(sys.stdin.readline())

# Case #1:
# Naomi's blocks: 
# [0.5]
# Ken's blocks: 
# [0.6]

# Case #2:
# Naomi's blocks: 
# [0.7, 0.2]
# Ken's blocks: 
# [0.8, 0.3]

# Case #3:
# Naomi's blocks: 
# [0.5, 0.1, 0.9]
# Ken's blocks: 
# [0.6, 0.4, 0.3]

# Case #4:
# Naomi's blocks: 
# [0.186, 0.389, 0.907, 0.832, 0.959, 0.557, 0.3, 0.992, 0.899]
# Ken's blocks: 
# [0.916, 0.728, 0.271, 0.52, 0.7, 0.521, 0.215, 0.341, 0.458]

def war(naomi, ken):
    # Naomi goes first; the order she chooses her blocks doesn't matter
    ken.sort()
    naomi.sort()
    naomi_points = 0
    while len(naomi):
        naomi_choice = naomi.pop()
        # Ken chooses the smallest block that's heavier than Naomi's
        # block.  If no such block exists, he just chooses the smallest block.
        ken_choices = filter(lambda x : x > naomi_choice, ken)
        if len(ken_choices) == 0:
            ken_choice = ken[0]
        else:
            ken_choices.sort()
            ken_choice = ken_choices[0]
        
        ken.remove(ken_choice)
        print "Naomi chooses %f while Ken chooses %f" % (naomi_choice, ken_choice)
        if naomi_choice > ken_choice:
            naomi_points += 1
    return naomi_points

def deceitful_war(naomi, ken):
    # Naomi goes first; the order she chooses her blocks doesn't matter
    ken.sort()
    naomi.sort()
    naomi_points = 0
    while len(naomi):
        naomi_choice = naomi.pop()
        # Ken chooses the smallest block that's heavier than Naomi's
        # block.  If no such block exists, he just chooses the smallest block.

        ken_choices = filter(lambda x : x > naomi_told, ken)
        if len(ken_choices) == 0:
            ken_choice = ken[0]
        else:
            ken_choices.sort()
            ken_choice = ken_choices[0]
        
        ken.remove(ken_choice)
        print "Naomi chooses %f while Ken chooses %f" % (naomi_choice, ken_choice)

        if (naomi_choice > ken_choice) != (naomi_told > ken_choice):
            print "Error!"

        if naomi_choice > ken_choice:
            naomi_points += 1
    return naomi_points

for t in range(0,T):
    print "Case #%d:" % (t+1)
    N = int(sys.stdin.readline())

    naomi = map(float, sys.stdin.readline().rstrip().split(' '))
    ken   = map(float, sys.stdin.readline().rstrip().split(' '))

    print "Naomi's blocks: "
    print naomi
    print "Ken's blocks: "
    print ken
    print "Naomi wins %d times" % war(naomi, ken)
    print blocks[0]
