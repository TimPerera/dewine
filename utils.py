"""
`utils.py`
This module contains helper functions utilized within other modules
of this project.
"""
import random
from math import ceil

def generate_rand(mean,mode, prob_of_mode, sd=1, size = 1,precision=2, non_zero = True):
    # a function that generates values based on a specified distribution.
    # value returned will always be positive.
    res = []
    rand_val = 0
    for _ in range(size):
        if non_zero:
            while rand_val == 0:
                rand_val = random.gauss(mu=mean,sigma=sd)
        if random.random() <= prob_of_mode:
            if precision == 0:
                res.append(ceil(abs(mode)))
            else:
                res.append(abs(round(mode,precision)))
        else:
            if precision == 0:
                res.append(abs(ceil(round(rand_val, precision))))
            else:
                res.append(abs(round(rand_val,precision)))
    return res

