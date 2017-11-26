# Lecture 6-7 - Stochastic Programs & Inferential Statistics

[TOC]

## Stochastic Programs

* A stochastic model is one in which randomness is present, and variable states are not described by unique values, but rather by **probability distributions**. The behavior of this model cannot be entirely predicted.
    * events are **independent** of each other
    * Probabilities are always in the range **0 to 1**. 0 if impossible, and 1 if guaranteed.
    * If the probability of an event occurring is **p**, the probability of it not occurring must be **1-p**.

## Random Walk 

* The reason we look at random walk is:
    * it is a good example of how to use abstract data types and inheritance to structure programs in general and simulations in particular.

### Defines

* Location
    * `x`, `y` : coordinates.
    * `move(deltaX, deltaY)`: move self with deltaX, deltaY
    * `getX()`, `getY()`
    * `distFrom(otherLocation)`: check the distance between current location with otherLocation
* Field
    * `drunks`: list of drunk objects
    * `addDrunk(drunk, loc)`: add a drunk with its location into Fields' `drunks`
    * `moveDrunk(drunk)`: move the drunk's `location`
    * `getLoc(drunk)`: get the drunk's `location`
* Drunk(object)
    * `name`: it's name
* UsualDrunk(Drunk)
    * `takeStep()`: move one step to left/right/up/down direction
* ColdDrunk(Drunk)
    * `takeStep()`: move two steps towards south, the others are the same with UsualDrunk

### Simulations

* try 10, 100, 1000, 10000 steps with UsualDrunk and ColdDrunk

```python
def walk(f, d, numSteps):
    """Assumes: f a Field, d a Drunk in f, and numSteps an int >= 0.
       Moves d numSteps times, and returns the distance between
       the final location and the location at the start of the 
       walk."""
    start = f.getLoc(d)
    for s in range(numSteps):
        f.moveDrunk(d)
    return start.distFrom(f.getLoc(d))
    
def simWalks(numSteps, numTrials, dClass):
    """Assumes numSteps an int >= 0, numTrials an int > 0,
         dClass a subclass of Drunk
       Simulates numTrials walks of numSteps steps each.
       Returns a list of the final distances for each trial"""
    Homer = dClass()
    origin = Location(0, 0)
    distances = []
    for t in range(numTrials):
        f = Field()
        f.addDrunk(Homer, origin)
        distances.append(round(walk(f, Homer, numSteps), 1))
    return distances

class styleIterator(object):
    def __init__(self, styles):
        self.index = 0
        self.styles = styles

    def nextStyle(self):
        result = self.styles[self.index]
        if self.index == len(self.styles) - 1:
            self.index = 0
        else:
            self.index += 1
        return result
    
def simDrunk(numTrials, dClass, walkLengths):
    meanDistances = []
    for numSteps in walkLengths:
        print('Starting simulation of',
              numSteps, 'steps')
        trials = simWalks(numSteps, numTrials, dClass)
        mean = sum(trials)/len(trials)
        meanDistances.append(mean)
    return meanDistances

def simAll(drunkKinds, walkLengths, numTrials):
    styleChoice = styleIterator(('m-', 'b--', 'g-.'))
    for dClass in drunkKinds:
        curStyle = styleChoice.nextStyle()
        print('Starting simulation of', dClass.__name__)
        means = simDrunk(numTrials, dClass, walkLengths)
        pylab.plot(walkLengths, means, curStyle,
                   label = dClass.__name__)
    pylab.title('Mean Distance from Origin ('
                + str(numTrials) + ' trials)')
    pylab.xlabel('Number of Steps')
    pylab.ylabel('Distance from Origin')
    pylab.legend(loc = 'best')

random.seed(0)
numSteps = (10,100,1000,10000)
simAll((UsualDrunk, ColdDrunk), numSteps, 100)
```

<img src='media/unit-2-3.jpg' width=400/>

* plot every final locations

```python
def getFinalLocs(numSteps, numTrials, dClass):
    locs = []
    d = dClass()
    for t in range(numTrials):
        f = Field()
        f.addDrunk(d, Location(0, 0))
        for s in range(numSteps):
            f.moveDrunk(d)
        locs.append(f.getLoc(d))
    return locs

def plotLocs(drunkKinds, numSteps, numTrials):
    styleChoice = styleIterator(('k+', 'r^', 'mo'))
    for dClass in drunkKinds:
        locs = getFinalLocs(numSteps, numTrials, dClass)
        xVals, yVals = [], []
        for loc in locs:
            xVals.append(loc.getX())
            yVals.append(loc.getY())
        xVals = pylab.array(xVals)
        yVals = pylab.array(yVals)
        meanX = sum(abs(xVals))/len(xVals)
        meanY = sum(abs(yVals))/len(yVals)
        curStyle = styleChoice.nextStyle()
        pylab.plot(xVals, yVals, curStyle,
                      label = dClass.__name__ +\
                      ' mean abs dist = <'
                      + str(meanX) + ', ' + str(meanY) + '>')
    pylab.title('Location at End of Walks ('
                + str(numSteps) + ' steps)')
    pylab.ylim(-1000, 1000)
    pylab.xlim(-1000, 1000)
    pylab.xlabel('Steps East/West of Origin')
    pylab.ylabel('Steps North/South of Origin')
    pylab.legend(loc = 'upper left')

random.seed(0)
plotLocs((UsualDrunk, ColdDrunk), 10000, 1000)
```

<img src='media/unit-2-4.jpg' width=400/>


* [complete code](https://github.com/erictt/computer-science-learning/blob/master/computational-thinking/unit-2/lecture6-segment3.py)


## Inferential Statistics

* Definition:
    * use simulations to estimate the value of an unknown quantity by making use of the principle of **inferential statistics**.
* Detail explanation
    * `Population`: a set of examples
    * `Sample`: a proper subset of a population
    * `Goal`: Estimate some statistic about the population based on statistics about the sample
    * `Key fact`: If the sample is **random**, it tends to exhibit the same properties as the population from which it is drawn
* **Law of Large Number**: In repeated independent experiments (e.g., flipping a fair coin 100 times and counting the fraction of heads) with the same expected value (0.5 in this case), the average value of the experiments approaches the expected value(平均值趋近于期望值) as the number of experiments goes to infinity.
    * **Gambler's Fallacy**: If deviations from expected behavior occur, these deviations are likely to be evened out by opposite deviations in the future.
        1. that “large” is a relative concept.
        2. the law of large numbers does not imply that the absolute difference between the number of heads and the number of tails decreases as the number of flips increases. In fact, we can expect that number to increase.
        3. What decreases is the ratio of the absolute difference to the number of flips.

### Simulation

#### The ratio heads/tails (the law of large number)
* How many samples do we need to look at before we can have justified confidence in our answer?
* **variance** is measure of how much spread there is in the possible different outcomes, which can help us to justify.
    * \\(variance(X) = \frac{\sum_{x\in{X}}{(x-\mu)^{2}}}{\lvert{X}\rvert}\\)
* **standard deviation** tells us what fraction of the values are close to the mean. If many values are relatively close to the mean, the standard deviation is relatively small.
    * \\(\sigma(X) = \sqrt{\frac{1}{\lvert{X}\rvert}\sum_{x\in{X}}{(x-\mu)^{2}}}\\)
        *  where |X| is the size of the collection and (\\(\mu\\)) its mean.

        ```python
        def stdDev(X):
            """Assumes that X is a list of numbers.
                Returns the standard deviation of X"""
            mean = float(sum(X))/len(X) 
            tot = 0.0 
            for x in X:
                tot += (x - mean)**2 
            return (tot/len(X))**0.5 #Square root of mean difference
        ```
* For example, flip coins exponentially, from 2^4 to 2^20, each times we flip 20 times to get the mean values with standard deviation function.

    ```python
    #Page 160, Figure 12.4
    def stdDev(X):
        """Assumes that X is a list of numbers.
           Returns the standard deviation of X"""
        mean = float(sum(X))/len(X)
        tot = 0.0
        for x in X:
            tot += (x - mean)**2
        return (tot/len(X))**0.5 #Square root of mean difference
    
    #Page 161, Figure 12.5
    def makePlot(xVals, yVals, title, xLabel, yLabel, style,
                 logX = False, logY = False):
        """Plots xVals vs. yVals with supplied titles and labels."""
        pylab.figure()
        pylab.title(title)
        pylab.xlabel(xLabel)
        pylab.ylabel(yLabel)
        pylab.plot(xVals, yVals, style)
        if logX:
            pylab.semilogx()
        if logY:
            pylab.semilogy()
    
    def runTrial(numFlips):
        numHeads = 0
        for n in range(numFlips):
            if random.random() < 0.5:
                numHeads += 1
        numTails = numFlips - numHeads
        return (numHeads, numTails)
        
    def flipPlot1(minExp, maxExp, numTrials):
        """Assumes minExp and maxExp positive ints; minExp < maxExp
             numTrials a positive integer
           Plots summaries of results of numTrials trials of
             2**minExp to 2**maxExp coin flips"""
        ratiosMeans, diffsMeans, ratiosSDs, diffsSDs = [], [], [], []
        xVals = []
        for exp in range(minExp, maxExp + 1):
            xVals.append(2**exp)
        for numFlips in xAxis:
            ratios = []
            diffs = []
            for t in range(numTrials):
                numHeads, numTails = runTrial(numFlips)
                ratios.append(numHeads/float(numTails))
                diffs.append(abs(numHeads - numTails))
            ratiosMeans.append(sum(ratios)/float(numTrials))
            diffsMeans.append(sum(diffs)/float(numTrials))
            ratiosSDs.append(stdDev(ratios))
            diffsSDs.append(stdDev(diffs))
        numTrialsString = ' (' + str(numTrials) + ' Trials)'
        title = 'Mean Heads/Tails Ratios' + numTrialsString
        makePlot(xVals, ratiosMeans, title,
                'Number of flips', 'Mean Heads/Tails', 'bo', logX = True)
        title = 'SD Heads/Tails Ratios' + numTrialsString
        makePlot(xVals, ratiosSDs, title,
                'Number of Flips', 'Standard Deviation', 'bo',
                logX = True, logY = True)
            
        title = 'Mean abs(#Heads - #Tails)' + numTrialsString 
        makePlot(xVals, diffsMeans, title, 
                'Number of Flips', 'Mean abs(#Heads - #Tails)', 'bo', 
                logX = True, logY = True) 
        title = 'SD abs(#Heads - #Tails)' + numTrialsString 
        makePlot(xVals, diffsSDs, title,
                'Number of Flips', 'Standard Deviation', 'bo',
                logX = True, logY = True)
        
        flipPlot1(4, 20, 20)
    ```
    
    <img src='media/unit-2-2.jpg' width=600/>
    <img src='media/15043566360658.jpg' width=600/>

* Conclusion 
    * The ratio heads/tails is converging towards 1 and log of standard deviation is falling linearly with the log of the number of flips per trail. 
    * By the time we get to about 10^6 coin flips per trail, the standard deviation is roughly three decimal orders of magnitude smaller than the mean. 
    * As we flip more coins, not only do we have a more precise answer, but more important, we also have reason to be more confident that it is close to the right answer.
    * The absolute difference between the numbers of heads and tails grows with the number of flips. Talk more in next section.

#### The absolute difference between heads and tails (gambler's fallacy)

* **coefficient of variation** is the standard deviation divided by the mean, commonly used in fields such as engineering or physics when doing quality assurance studies. In general, distributions with a coefficient of variation of less than 1 are considered low-variance.
    * For example, the expression “The standard deviation is 15% of the mean” is a CV.
    
```python
#Page 163, Figure 12.7
def CV(X):
    mean = sum(X)/float(len(X))
    try:
        return stdDev(X)/mean
    except ZeroDivisionError:
        return float('nan')
   
#Page 164, Figure 12.8
def flipPlot1(minExp, maxExp, numTrials):
    """Assumes minExp and maxExp positive ints; minExp < maxExp
         numTrials a positive integer
       Plots summaries of results of numTrials trials of
         2**minExp to 2**maxExp coin flips"""
    ratiosMeans, diffsMeans, ratiosSDs, diffsSDs = [], [], [], []
    ratiosCVs, diffsCVs = [], []
    xAxis = []
    for exp in range(minExp, maxExp + 1):
        xAxis.append(2**exp)
    for numFlips in xAxis:
        ratios = []
        diffs = []
        for t in range(numTrials):
            numHeads, numTails = runTrial(numFlips)
            ratios.append(numHeads/float(numTails))
            diffs.append(abs(numHeads - numTails))
        ratiosMeans.append(sum(ratios)/float(numTrials))
        diffsMeans.append(sum(diffs)/float(numTrials))
        ratiosSDs.append(stdDev(ratios))
        diffsSDs.append(stdDev(diffs))
        ratiosCVs.append(CV(ratios))
        diffsCVs.append(CV(diffs))
    numTrialsString = ' (' + str(numTrials) + ' Trials)'
    title = 'Mean Heads/Tails Ratios' + numTrialsString
    makePlot(xAxis, ratiosMeans, title,
             'Number of flips', 'Mean Heads/Tails', 'bo', logX = True)
    title = 'SD Heads/Tails Ratios' + numTrialsString
    makePlot(xAxis, ratiosSDs, title,
             'Number of Flips', 'Standard Deviation', 'bo',
             logX = True, logY = True)
    title = 'Mean abs(#Heads - #Tails)' + numTrialsString
    makePlot(xAxis, diffsMeans, title,
         'Number of Flips', 'Mean abs(#Heads - #Tails)', 'bo',
         logX = True, logY = True)
    title = 'SD abs(#Heads - #Tails)' + numTrialsString
    makePlot(xAxis, diffsSDs, title,
         'Number of Flips', 'Standard Deviation', 'bo',
         logX = True, logY = True)
    title = 'Coeff. of Var. abs(#Heads - #Tails)' + numTrialsString
    makePlot(xAxis, diffsCVs, title, 'Number of Flips',
             'Coeff. of Var.', 'bo', logX = True)
    title = 'Coeff. of Var. Heads/Tails Ratio' + numTrialsString
    makePlot(xAxis, ratiosCVs, title, 'Number of Flips',
             'Coeff. of Var.', 'bo', logX = True, logY = True)
```

<img src='media/15016457519417.jpg' width=600/>
    
* Conclusion
    * the plot of coefficient of variation for the heads/tails ratio is not much different from the plot of the standard deviation, cause the mean is close to 1.
    * **dispersion** in the values of `abs(heads – tails)` is independent of the number of flips. As the numbers of tails goes up, the mean of `abs(heads – tails)` also keep growing, which proves **Gambler's Fallacy** that `abs(heads – tails)` will never be even, only gets bigger.

### Distributions

* A **histogram** is a plot designed to show the distribution of values in a set of data.

    ```python
    vals = [1, 200] #guarantee that values will range from 1 to 200 for i in range(1000):
    num1 = random.choice(range(1, 100))
    num2 = random.choice(range(1, 100))
    vals.append(num1+num2) 
    pylab.hist(vals, bins = 10)
    ```
    
    <img src='media/15017304680216.jpg' width=300/>

    
#### Normal Distributions and Confidence Levels

* formula of normal distribution: \\(f(x)=\frac{1}{\sigma\sqrt{2\pi}}*e^{-\frac{(x-\mu)^2}{2\sigma^2}}\\)  ( μ is the mean, σ the standard deviation)
* Normal distributions are frequently used in constructing probabilistic models for three reasons:
    1. they have nice mathematical properties, 
    2. many naturally occurring distributions are indeed close to normal
    3. they can be used to produce **confidence intervals**.
        * a confidence interval provides a range that is likely to contain the unknown value and a confidence that the unknown value lays within that range. 

    ```python
    def flip(numFlips):
    heads = 0.0
    for i in range(numFlips):
        if random.random() < 0.5:
            heads += 1
    return heads/numFlips

    def flipSim(numFlipsPerTrial, numTrials):
        fracHeads = []
        for i in range(numTrials):
            fracHeads.append(flip(numFlipsPerTrial))
        mean = sum(fracHeads)/len(fracHeads)
        sd = stdDev(fracHeads)
        return (fracHeads, mean, sd)
    
    def labelPlot(numFlips, numTrials, mean, sd):
        pylab.title(str(numTrials) + ' trials of '
                    + str(numFlips) + ' flips each')
        pylab.xlabel('Fraction of Heads')
        pylab.ylabel('Number of Trials')
        xmin, xmax = pylab.xlim()
        ymin, ymax = pylab.ylim()
        pylab.text(xmin + (xmax-xmin)*0.02, (ymax-ymin)/2,
                   'Mean = ' + str(round(mean, 4))
                   + '\nSD = ' + str(round(sd, 4)), size='x-large')
    
    def makePlots(numFlips1, numFlips2, numTrials):
        val1, mean1, sd1 = flipSim(numFlips1, numTrials)
        pylab.hist(val1, bins = 20)
        xmin,xmax = pylab.xlim()
        ymin,ymax = pylab.ylim()
        labelPlot(numFlips1, numTrials, mean1, sd1)
        pylab.figure()
        val2, mean2, sd2 = flipSim(numFlips2, numTrials)
        pylab.hist(val2, bins = 20)
        pylab.xlim(xmin, xmax)
        labelPlot(numFlips2, numTrials, mean2, sd2)
    
    random.seed(0)
    makePlots(100,1000,100000)
    ```
    
    <img src='media/15017329340640.jpg' width=600/>


* **empirical rule** for normal distributions:
    * 68% of the data will fall within 1 standard deviation of the mean,
    * 95% of the data will fall within 2 standard deviations of the mean, 
    * 99.7% of the data will fall within 3 standard deviations of the mean.
* For example:
    * a political poll might indicate that a candidate is likely to get 52% of the vote ±4% (i.e., the confidence interval is of size 8) with a confidence level of 95%. What this means is that the pollster believes that 95% of the time the candidate will receive between 48% and 56% of the vote.
* Normal distributions can be easily generated by calling `random.gauss(mu, sigma)`, which returns a randomly chosen floating point number from a normal distribution with mean `mu` and standard deviation `sigma`.
    * the function `gauss` is short for `Gaussian Distribution` which is the same as `Normal Distribution`.
    
#### Extension
* Uniform Distribution
    * If one were to plot the probability of each possible lottery number being chosen, it would be a flat line. Such distributions are called uniform.
* Exponential and Geometric Distributions
    * check page 173 for more details
* [Benford’s Distribution](https://en.wikipedia.org/wiki/Benford%27s_law)

## Words

* Law of Large Number 大数定律
* Gambler’s Fallacy 赌徒谬误
* Coefficient of Variation 变异系数
* Gaussian Distribution 高斯分布



