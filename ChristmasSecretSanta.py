#!/usr/bin/python

import sys
import random

# Place given argument names into list.
givers = sys.stdin.readline().split()
receivers = list(givers)

# Shuffle receivers list.
random.shuffle(receivers)

# Loop through and make sure no one has themselves.
for i in range(0,len(givers)):
    if (givers[i] == receivers[i]):
        if (i == len(givers)-1):
            receivers[i] = receivers[0]
            receivers[0] = givers[i]
        else:
            receivers[i] = receivers[i+1]
            receivers[i+1] = givers[i]

# Print files named after who is the giver.
for person in range(0,len(givers)):
    f = open(givers[person]+'.txt', 'w')
    f.write('{} is giving a gift to {}'.format(givers[person], receivers[person]))



