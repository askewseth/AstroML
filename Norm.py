import numpy as np
import matplotlib.pyplot as plt

def norm(twodarray, emission_start, emission_end):
    """private method."""
    rel_array = twodarray[:emission_start] + twodarray[emission_end:]
    xvals = [i[0] for i in rel_array]
    yvals = [i[1] for i in rel_array]
    fits = {}
    for x in range(1, 6):
        coeff = np.polyfit(xvals, yvals, x)
        poly = np.poly1d(coeff)
        ys = poly(xvals)
        fits[x] = {
            'coefficients': coeff,
            'polynomial': poly,
            'y_values': ys
        }
    return fits
