# Lecture 10 - 11

[TOC]

## Experimental Data

* These lectures are talking about the interplay between statistics and  experimental science. And how to get a valid statistical conclusion.

### The Behavior of Springs

* **Hooke’s law** of elasticity: `F = -kx`
    * In other words, the force, `F`, stored in a spring is linearly related to the distance, `x`, the spring has been compressed(or stretched).
    * `k` is called the spring constant.
    * All springs have an **elastic limit**, beyond which the law fails.

* For example, How much does a rider have to weigh to compress the spring  on motorbike 1cm? (\\(k \approx 35,000𝑁/𝑚\\))
    * \\(F = 0.01m * 35,000N/m\\)
    * \\(F = 350N\\) 
    * \\(F = mass * acc\\), \\(F = mass * 9.81m/s^2\\)
    * \\(mass * 9.81m/s^2 = 350N\\)
    * \\(mass \approx 35.68kg\\)

* Finding `k`
    * We can't conduct the experiment perfectly, so, to hang a series of increasingly heavier weights on the spring, measure the stretch of the spring each time, and plot the results will be a better way.

    * First we should know: 
        * `F=-kx`
        * `k=-F/x`
        * `k=9.81*m/x`
        * <img src="media/15026205788878.jpg" width=200 />

   * Then, we got some data

        ```
        0.0865 0.1
        0.1015 0.15
        ...
        0.4263 0.65
        0.4562 0.7
        ```
        
   * Plot the data, we got:

       * <img src="media/15026267364688.jpg" width=250 />
       * It has some measurement errors.
    
   * Next step is to fit curves to data.
       * When we fit a curve to a set of data, we are finding a fit that relates an independent variable (the mass) to an estimated value of a dependent variable (the distance)
       * To fit curves to data, we need to define an **objective function** that provides a quantitative assessment of how well the curve fits the data. In this case, a straight line, that is **linear function**. 
       * Then, finding the best fit is an optimization problem. most commonly used **objective function** is called **least squares**:
           * \\(\displaystyle\sum_{i=0}^{len(observed)-1}(observed[i] - predicted[i])^2\\)
       * Next is to use a successive approximation algorithm to find the best least-squares fit. **PyLab** provides a built-in function, **polyfit**:
            
            ```python
            pylab.polyfit(observedXVals, observedYVals, n)
            ```
            
            * this function finds the coefficients of a polynomial of degree `n` that provides a best least-squares fit for the set of points defined by the arrays observedXVals and observedYVals.
            * The algorithm used by polyfit is called **linear regression**.

    * Visualizing the Fit

        ```python
        def getData(fileName):
            dataFile = open(fileName, 'r')
            distances = []
            masses = []
            dataFile.readline() #discard header
            for line in dataFile:
                d, m = line.split()
                distances.append(float(d))
                masses.append(float(m))
            dataFile.close()
            return (masses, distances)
            
        def labelPlot():
            pylab.title('Measured Displacement of Spring')
            pylab.xlabel('|Force| (Newtons)')
            pylab.ylabel('Distance (meters)')
        
        def plotData(fileName):
            xVals, yVals = getData(fileName)
            xVals = pylab.array(xVals)
            yVals = pylab.array(yVals)
            xVals = xVals*9.81  #acc. due to gravity
            pylab.plot(xVals, yVals, 'bo',
                       label = 'Measured displacements')
            labelPlot()
            
        def fitData(fileName):
            xVals, yVals = getData(fileName)
            xVals = pylab.array(xVals)
            yVals = pylab.array(yVals)
            xVals = xVals*9.81 #get force
            pylab.plot(xVals, yVals, 'bo',
                       label = 'Measured points')
            labelPlot()                 
            a,b = pylab.polyfit(xVals, yVals, 1)
            # estYVals = a*xVals + b
            estYVals = pylab.polyval(model, xVals)
            print('a =', a, 'b =', b)
            pylab.plot(xVals, estYVals, 'r',
                       label = 'Linear fit, k = '
                       + str(round(1/a, 5)))
            pylab.legend(loc = 'best')
            
        fitData('springData.txt')
        ```

        * <img src="media/15026310672144.jpg" width=250 />

        * `k = 21.53686`

### Another Experiment
    
* to fit curves to these mystery data: 

   * <img src="media/15026317050419.jpg" width=250 />

   * <img src="media/15026317968585.jpg" width=250 />

* how good are these fits

   * we can see that quadratic model is better than linear model, but how bad a fit is the line and how good is the quadratic fit?
   * comparing **mean squared error**

       ```python
       def aveMeanSquareError(data, predicted):
           error = 0.0
           for i in range(len(data)):
               error += (data[i] - predicted[i])**2
           return error/len(data)
       ```
       
       * then we got:
           * Ave. mean square error for linear model = 9372.73078965
           * Ave. mean square error for quadratic model = 1524.02044718
       * Seems like, quadratic model is better than linear model. But we still have to ask, is the quadratic fit good in an absolute sense?
       * The mean square error is useful for comparing two different models of the same data, but it's not actually very useful for getting the absolute goodness of fit.

* **Coefficient of Determination**, written as \\(R^2\\)

   * \\(R^{2}=1-\frac{\sum_{i}(y_i-p_i)^2}{\sum_{i}(y_i-\mu_i)^2}\\)
       * By comparing the estimation errors (the numerator) with the variability of the original values (the denominator), R 2 is intended to capture the proportion of variability in a data set that is accounted for by the statistical model provided by the fit
       * Always between 0 and 1 when fit generated by a linear regression and tested on training data
       * If R^2 = 1, the model explains all of the variability in the data. If R^2 = 0, there is no relationship between the values predicted by the model and the actual data.

        ```python
        def rSquared(observed, predicted):
            error = ((predicted - observed)**2).sum()
            meanError = error/len(observed)
            return 1 - (meanError/numpy.var(observed))
        ```
  
   * Testing Goodness of Fits
        
       ```python
       def genFits(xVals, yVals, degrees):
           models = []
           for d in degrees:
               model = pylab.polyfit(xVals, yVals, d)
               models.append(model)
           return models
       
       def testFits(models, degrees, xVals, yVals, title):
           pylab.plot(xVals, yVals, 'o', label = 'Data')
           for i in range(len(models)):
               estYVals = pylab.polyval(models[i], xVals)
               error = rSquared(yVals, estYVals)
               pylab.plot(xVals, estYVals,
                          label = 'Fit of degree '\
                          + str(degrees[i])\
                          + ', R2 = ' + str(round(error, 5)))
           pylab.legend(loc = 'best')
           pylab.title(title)
       
       xVals, yVals = getData('mysteryData.txt')
       degrees = (1, 2)
       models = genFits(xVals, yVals, degrees)
       testFits(models, degrees, xVals, yVals, 'Mystery Data')
       ```
       
       <img src="media/15026333280446.jpg" width=250 />

       * Quadratic model get 84%, and Linear get almost 0%.
       * Since the degree of polynomial can affect the Goodness of Fits, what if we use some bigger ones? Can we get a tighter Fit?
           * <img src="media/15026337479826.jpg" width=250 />


