# Lecture 4-5 - Plotting

\[TOC\]

## Plotting

* Just an example.

```python
import pylab

pylab.figure('lin quad') # give a name to this figure
pylab.clf() # clean the figure, avoid overlapping
# mySample: X values
# myLinear/myQuadratic/myCubic/myExponential: Y values 
# b-/ro/g^/r-- : line's style. 
pylab.plot(mySamples, myLinear, 'b-', label = 'linear', linewidth = 2.0)
pylab.plot(mySamples, myQuadratic,'ro', label = 'quadratic', linewidth = 3.0)
pylab.legend(loc = 'upper left')
pylab.title('Linear vs. Quadratic')

pylab.figure('cube exp')
pylab.clf()
pylab.plot(mySamples, myCubic, 'g^', label = 'cubic', linewidth = 4.0)
pylab.plot(mySamples, myExponential, 'r--',label = 'exponential', linewidth = 5.0)
pylab.legend()
pylab.title('Cubic vs. Exponential')
```

* ![](../.gitbook/assets/unit-2-1%20%281%29.jpg)

