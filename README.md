sidefit
=======

This is a fitting package that (currently) only supports a brute-force
calculation. It is designed to provide an alternative chi-squared; this
package fits the 'radial' distance to the line rather than just the 
vertical distance. This is particularly tricky, as often the parameterspace
is very noisy meaning most fitting packages do not converge well (hence
the brute-force nature).

In the future, we hope to use a tree structure to significantly reduce the
computational impact of fitting in this way.


Requirements
------------

+ `python3.5` or above
+ `scipy`
+ `numpy`

For tests:

+ `matplotlib`
+ `pytest`


Usage
-----

The frontend is available through the `Fitter` class. See below.

```
from sidefit import Fitter

fit = Fitter(linex, liney, pointsx, pointsy)
interp = fit.interpolate_function(kind="linear")
dr = fit.brute_force(N_lr=100, N=10000)
```


Test plots
----------

The package produces a number of test plots. Find a description of them below.

+ `test_plot_heaviside.png`: this shows two panels. On the top panel, the
  distance between the point and the line at a value of dx. This is essentially
  a plot of the cost function. On the bottom, we show the point (dot) and the
  line it is being fit to.
+ `test_integration_heaviside.png`: this shows two panels. On the bottom panel
  we show dr, the minimal distance between the point at x-value x and the line.
  The top panel shows the points in thick blue (these are stacked points) and
  the line in blue.
