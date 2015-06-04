__author__ = 'Joshua Zosky'

from numpy import percentile, nonzero, ones, size

def z_scale(x,ub,lb, perc=[]):
    # ZSCALE (X,UB,LB)
    #
    # This function scales  X into Y such that
    #	its maximum value is UB
    #	and minimum value is LB
    # If perc is specified, then clipping is done
    # at the percentile range specified (e.g. [2, 98])
    # before scaling.
    # If X is all constants, it gets scaled to UB;
    #
    #			Ziad, Oct 30 96 / modified March 18 97

    y = []

    if ub < lb:
        print'Error z_scale: Upper bound < Lower bound'
        return
    if perc:
        pr = percentile(x,perc)
        iclip = nonzero(x < pr[0])
        x[iclip] = pr[0]
        iclip = nonzero(x > pr[1])
        x[iclip] = pr[1]

    xmin = min(x)
    xmax = max(x)

    if xmin == xmax:
        y = ones(size(x)) * ub
    else:
        y = (((x - xmin) / (xmax - xmin)) * (ub - lb)) + lb

    return y