import numpy as np
import itertools
from State import *
from Path import *
from Schedule import *
import typing

class UnderlyingModel:
  """
  Abstract Class (Interface)

  forwardto(state,forwardtime) : expects a state object and a future time; returns a state object sampled at the future time.

  genesis() : Returns a single state---the beginning of the chain.
  """
  def __init__(self): 
    pass
  def forwardto(self,state, forwardtime):
    pass
  def genesis(self):
    pass
  def generatepath(self, initialstate = None, schedule = None ):
    if initialstate is None: initialstate = self.genesis()
    print(self.genesis())
    if schedule is None: schedule = np.linspace(0, 1, 100)
    assert initialstate.get_time() == schedule[0]

    acc = [initialstate]
    for i in range(1,len(schedule)-1):
        newstate =  self.forwardto(acc[i-1],schedule[i])
        acc.append(newstate)
    return Path(acc)

  def generatepaths(self, initialstate= None, schedules = None, n = 7):
      if schedules is None:
        schedules = [Schedule(np.linspace(0,1,100)) for i in range(0,n)] # default generating 7 paths
      return Paths([self.generatepath(initialstate, schedule) for schedule in schedules])

class GeometricBrownianMotion(UnderlyingModel):
  """
  A concrete class of Underlying model.
  """
  def __init__(self, rate = 0.06, sigma = 0.2, dividend = 0):
    # To be modularized ...
    self.name = "Geometric Brownian Motion"
    self.rate = rate
    self.sigma = sigma
    self.dividend = dividend
    self.rng = np.random.default_rng()

  def forwardto(self,state,forwardtime):
    """forwardtime is a real number"""
    dt = forwardtime - state.get_time()
    assert dt >= 0
    stateupdatedcoord = state.get_coord() * np.exp((self.rate - self.dividend - self.sigma ** 2.0 / 2.0) * dt + self.sigma * dt ** 0.5 * self.rng.standard_normal())
    
    return State(forwardtime, stateupdatedcoord)

  def genesis(self): # assumed to be at time 0
    return State(0.0,1.0)

