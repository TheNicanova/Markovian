import numpy as np
import itertools
from Path import *
from Schedule import *


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
  def generatepath(self, schedule):
    patharray = itertools.accumulate(schedule, self.forwardto, initial=schedule[0])
    return Path(patharray)

  def generatepaths(self, schedules):
    return Paths([self.generatepath(schedule) for schedule in schedules])

class GeometricBrownianMotion(UnderlyingModel):
  """A concrete class of Underlying model."""
  def __init__(self, rate = 0.06, sigma = 0.2, dividend = 0):
    # To be modularized ...
    self.name = "Geometric Brownian Motion"
    self.rate = rate
    self.sigma = sigma
    self.dividend = dividend
    self.rng = np.random.default_rng()

  def forwardto(self,state,forwardtime):
    """forwardtime is a real number"""
    dt = forwardtime - state.time()
    assert dt >= 0
    stateupdatedcoord = state.coord() * np.exp((self.rate - self.dividend - self.sigma ** 2.0 / 2.0) * dt + self.sigma * dt ** 0.5 * self.rng.standard_normal())
    
    return State(forwardtime, stateupdatedcoord)
  
  def genesis(self):
    return State(0.0,1.0)

