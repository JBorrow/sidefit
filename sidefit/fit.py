"""
Main fitting functions.
"""

import scipy.interpolate as si
import scipy.optimize as so

import numpy as np

from typing import List

try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x

class Fitter(object):
    """
    The main object that handles a lot of the i/o of data.
    """

    def __init__(
            self,
            x: np.ndarray,
            y: np.ndarray,
            points_x: np.ndarray,
            points_y: np.ndarray,
            tol: float,
        ):
        """
        Inputs
        ------

        @param x | np.ndarray | the x-values of the _model_.
        @param y | np.ndarray | the y-values of the _model_.
        @param points | np.ndarray | the points to find nearest values
                                     in the interpolated model to.
        @param tol | float | controls how fine-grained interpolation
                             of the model values is.


        Outputs
        -------

        @output self.r | np.ndarray | closest distances between your model 
                                      and 'points'.
        """

        self.x = x
        self.y = y
        self.points_x = points_x
        self.points_y = points_y
        self.tol = tol


        return


    def interpolate_function(self, kind="linear"):
        """
        Interpolate the function; this is essentailly just a local wrapper 
        over scipy.intepolate.

        Inputs
        ------

        @param kind | str | the kind of interpolation to use

        Outputs
        -------

        @param interp | callable | the interpolated function y(x).
        """

        self.interp = si.interp1d(self.x, self.y, kind=kind)

        return self.interp


    def brute_force(
            self,
            N_lr=100,
            N=10000,

        ) -> np.ndarray:
        """
        The 'brute force' implementation of neighbor finding. This is
        O(n), as we search through the function self.interp to find 
        the closest 'point'.

        Inputs
        ------

        @param N_lr | int | The number of particles to consider left/right
                            when doing the brute force solutionm
        @param N | int | The number of values to interpolate between l and r.
        """

        def r2(x, px, py):
            return (x - px)**2 + (self.interp(x) - py)**2

        # Because points iterator
        N_out = len(self.points_x)
        self.r = np.empty(N_out)

        for index in tqdm(range(N_out)):
            try:
                N_i = N

                # We need to choose the bounds for brute force finding of
                # the minima. Regular iteration methods _do not work_.

                if index < N_lr:
                    lower = min(self.x)
                    upper = self.x[N_lr+index]
                    N_i *= (N_lr - index) / N_lr
                elif index > (len(self.x) - (N_lr + 1)):
                    lower = self.x[index-N_lr]
                    upper = self.x[-1]
                    N_i *= (len(self.x) - index)/N_lr
                else:
                    lower = self.x[index-N_lr]
                    upper = self.x[index+N_lr]

                x0, fval, _, _ = so.brute(
                    r2,
                    ranges=[(lower,upper)],
                    args=(self.points_x[index], self.points_y[index]),
                    Ns=N,
                    full_output=True
                )

                self.r[index] = np.sqrt(fval)
            except ValueError:
                # Must be edge of box.

                self.r[index] = 0.0

        return self.r


