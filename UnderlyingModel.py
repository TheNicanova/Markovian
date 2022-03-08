import numpy as np
import itertools
from State import *
from Path import *
from Schedule import *
import typing

class UnderlyingModel:
  """
  Abstract Class (Interface)

  forward_to(state,forward_time) : expects a state object and a future time; returns a state object sampled at the future time.

  genesis() : Returns a single state---the beginning of the chain.
  """
  def __init__(self): 
    pass
  def forward_to(self,state, forward_time):
    pass
  def genesis(self):
    pass
  def generate_path(self, inital_state = None, schedule = None ):
    if inital_state is None: inital_state = self.genesis()
    print(self.genesis())
    if schedule is None: schedule = np.linspace(0, 1, 100)
    assert inital_state.get_time() == schedule[0]

    acc = [inital_state]
    for i in range(1,len(schedule)-1):
        newstate =  self.forward_to(acc[i-1],schedule[i])
        acc.append(newstate)
    return Path(acc)

  def generate_paths(self, inital_state= None, schedules = None, n = 7):
      if schedules is None:
        schedules = [Schedule(np.linspace(0,1,101)) for i in range(0,n)] # default generating 7 paths
      return Paths([self.generate_path(inital_state, schedule) for schedule in schedules])

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

  def forward_to(self,state,forward_time):
    """forward_time is a real number"""
    dt = forward_time - state.get_time()
    assert dt >= 0
    stateupdatedcoord = state.get_coord() * np.exp((self.rate - self.dividend - self.sigma ** 2.0 / 2.0) * dt + self.sigma * dt ** 0.5 * self.rng.standard_normal())
    
    return State(forward_time, stateupdatedcoord)

  def genesis(self): # assumed to be at time 0
    return State(0.0,1.0)

