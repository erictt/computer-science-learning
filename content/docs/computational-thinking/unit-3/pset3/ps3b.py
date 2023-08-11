# Problem Set 3: Simulating the Spread of Disease and Virus Population Dynamics 

import random
import pylab
import numpy as np

''' 
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        clearProb: Maximum clearance probability (a float between 0-1).
        """
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def getMaxBirthProb(self):
        """
        Returns the max birth probability.
        """
        return self.maxBirthProb

    def getClearProb(self):
        """
        Returns the clear probability.
        """
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step. 
        returns: True with probability self.getClearProb and otherwise returns
        False.
        """
        return random.random() < self.clearProb
    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException
        else:
            return SimpleVirus(self.maxBirthProb, self.clearProb)

class Patient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        """
        Returns the viruses in this Patient.
        """
        return self.viruses

    def getMaxPop(self):
        """
        Returns the max population.
        """
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)


    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:
        
        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.   
        
        - The current population density is calculated. This population density
          value is used until the next call to update() 
        
        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.                    

        returns: The total virus population at the end of the update (an
        integer)
        """
        newViruses = []
        for virus in self.getViruses():
            if not virus.doesClear():
                newViruses.append(virus);
                try:
                    newViruses.append(virus.reproduce(self.getTotalPop()/self.maxPop))           
                except NoChildException as e:
                    continue
                        # print("doesn't reproduce")
        self.viruses = newViruses
        return self.getTotalPop()

#random.seed(0)
#v1 = SimpleVirus(0.96, 0.75)
#popDensity = 0.02
#while True:
#    try:
#        v1.reproduce(popDensity)
#        print("Reproduced successfully")
#    except NoChildException as e:
#        print("Raised 'NoChildException'")     
#        break

#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb,
                          numTrials):
    """
    Run the simulation and plot the graph for problem 3 (no drugs are used,
    viruses do not have any drug resistance).    
    For each of numTrials trial, instantiates a patient, runs a simulation
    for 300 timesteps, and plots the average virus population size as a
    function of time.

    numViruses: number of SimpleVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: Maximum clearance probability (a float between 0-1)
    numTrials: number of simulation runs to execute (an integer)
    """
    
    averageVirusPops = np.zeros(300)
    for trial in range(numTrials):
        viruses = []
        for vnum in range(numViruses):
            viruses.append(SimpleVirus(maxBirthProb, clearProb))
        p = Patient(viruses, maxPop)
        for i in range(300):
            p.update()
            averageVirusPops[i] += p.getTotalPop()
        
    pylab.figure('average virus population[no drugs]')
    pylab.plot(list(averageVirusPops/numTrials), label = 'No drugs')
    pylab.title('SimpleVirus simulation')
    pylab.xlabel('Tiems Steps')
    pylab.ylabel('Average virus population')
    pylab.legend()
    pylab.show()

#random.seed(0)
#simulationWithoutDrug(100, 1000, 0.1, 0.05, 20)


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        
        self.resistances = resistances
        self.mutProb = mutProb


    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        if drug in self.resistances:
            return self.resistances[drug]
        return False

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        for drugName, doesResistance in self.resistances.items():
            if drugName in activeDrugs and not doesResistance:
                raise NoChildException
        
        if random.random() > self.maxBirthProb * (1 - popDensity):
            raise NoChildException
        else:
            offSpringResistances = self.resistances
            for drugName in offSpringResistances.keys():
                if random.random() >= 1-self.mutProb:
                   offSpringResistances[drugName] = False if offSpringResistances[drugName] else True

            return ResistantVirus(self.maxBirthProb, self.clearProb, 
                                  offSpringResistances, self.mutProb)
#random.seed(0)
##v1 = ResistantVirus(0.96, 0.75, {'guttagonol':True, 'srinol':False}, 0.4)
#v1 = ResistantVirus(1.0, 0.0, {'drug1':True, 'drug2': True, 'drug3': True, 'drug4': True, 'drug5': True, 'drug6': True}, 0.5)
#popDensity = 0.02
#while True:
#    try:
#        v1.reproduce(popDensity, [])
#        print("Reproduced successfully")
#    except NoChildException as e:
#        print("Raised 'NoChildException'")     
#        break


#
# PROBLEM 4
#
class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """
        Patient.__init__(self, viruses, maxPop)
        self.postcondition = []


    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: The list of drugs being administered to a patient is updated
        """
        if newDrug not in self.postcondition:
            self.postcondition.append(newDrug)


    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.postcondition


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        numResistViruses = self.getTotalPop()
        for virus in self.viruses:
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    numResistViruses -= 1
                    break
        return numResistViruses

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly

        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Based on this value of population density, determine whether each 
          virus particle should reproduce and add offspring virus particles to 
          the list of viruses in this patient.
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """
        newViruses = []
        for virus in self.viruses:
            if not virus.doesClear():
                newViruses.append(virus);
                try:
                    newViruses.append(virus.reproduce(self.getTotalPop()/self.maxPop, self.postcondition))
                except NoChildException as e:
                    continue
                        # print("doesn't reproduce")
        self.viruses = newViruses
        return self.getTotalPop()

#random.seed(0)
#virus1 = ResistantVirus(1.0, 0.0, {"drug1": True}, 0.0)
#virus2 = ResistantVirus(1.0, 0.0, {"drug1": False, "drug2": True}, 0.0)
#virus3 = ResistantVirus(1.0, 0.0, {"drug1": True, "drug2": True}, 0.0)
#patient = TreatedPatient([virus1, virus2, virus3], 100)
#print(patient.getResistPop(['drug1']))
#print(patient.getResistPop(['drug2']))
#print(patient.getResistPop(['drug1','drug2']))
#print(patient.getResistPop(['drug3']))
#print(patient.getResistPop(['drug1', 'drug3']))
#print(patient.getResistPop(['drug1','drug2', 'drug3']))

#
# PROBLEM 5
#
def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances,
                       mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                 (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
             (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """

    sumVirusPops = np.zeros(300)
    resistantSumVirusPops = np.zeros(300)

    for trial in range(numTrials):

        # inintial viruses
#        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances.copy(), mutProb) 
#            for v in range(numViruses)]
        viruses = []
        for num in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb, clearProb, resistances.copy(), mutProb))
        
        # initial patient with precription
        p = TreatedPatient(viruses, maxPop)

        for i in range(150):
            sumVirusPops[i] += p.update()
            resistantSumVirusPops[i] += p.getResistPop(["guttagonol"])

        p.addPrescription("guttagonol")
            
        for i in range(150):
            sumVirusPops[150+i] += p.update()
            resistantSumVirusPops[150+i] += p.getResistPop(["guttagonol"])
            
    averageVirusPops = sumVirusPops / float(numTrials)
    averageVirusPops = [float('{:.1f}'.format(i)) for i in averageVirusPops]
    
    resistantAverageVirusPops = resistantSumVirusPops / float(numTrials)
    resistantAverageVirusPops = [float('{:.1f}'.format(i)) for i in resistantAverageVirusPops]
    
    pylab.figure('average virus population[with drugs]')
    pylab.plot(averageVirusPops, label = 'Total Pop')
    pylab.plot(resistantAverageVirusPops, label = 'Resistant Pop')
    pylab.title('ResistantVirus simulation')
    pylab.xlabel('Tiems Steps')
    pylab.ylabel('Average virus population')
    pylab.legend()
    pylab.show()


random.seed(0)
simulationWithDrug(1, 10, 1.0, 0.0, {}, 1.0, 5)
# [2.0, 3.6, 5.2, 7.4, 8.8, 9.0, 9.8, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10

#simulationWithDrug(1, 20, 1.0, 0.0, {"guttagonol": True}, 1.0, 5)
# [1.8, 3.6, 6.2, 10.2, 15.2, 18.0, 19.6, 20.8, 20.8, 20.8, 20.8, 20.8, 20.8, 20.8
# [1.0, 1.8, 3.2, 5.0, 7.6, 9.0, 10.0, 10.8, 10.8, 10.8, 10.8, 10.8, 10.8, 

#simulationWithDrug(75, 100, .8, 0.1, {"guttagonol": True}, 0.8, 1)
# [87.0, 100.0, 97.0, 89.0, 96.0, 99.0, 96.0, 97.0, 99.0, 99.0, 98.0, 91.0, 95.0,
# [71.0, 69.0, 68.0, 59.0, 61.0, 61.0, 57.0, 55.0, 53.0, 49.0, 46.0, 40.0, 41.0, 

#simulationWithDrug(100, 1000, 0.1, 0.05, {'guttagonol': False}, 0.005, 100)
