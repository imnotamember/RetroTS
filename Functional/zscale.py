__author__ = 'Joshua Zosky'

from numpy import percentile, size, clip, array


def z_scale(x, lower_bound, upper_bound, perc=[]):
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

    if type(x) != type(array):
        x = array(x)
    if upper_bound < lower_bound:
        print'Error z_scale: Upper bound < Lower bound'
        return
    if perc:
        lower_clip = percentile(x, perc[0])
        upper_clip = percentile(x, perc[1])
        x = x.clip(lower_clip, upper_clip)

    xmin = min(x)
    xmax = max(x)

    if xmin == xmax:
        # If x is all constants, then scale up to upper_bound value
        y = array(size(x))
        y.fill(upper_bound)
    else:
        # If x is not all constants, then scale to bounds
        y = (((x - xmin) / (xmax - xmin)) * (upper_bound - lower_bound)) + lower_bound
    return y