class UnderlyingModel:
  """
  Abstract Class (Interface)

  forwardto(state,forwardtime) : takes a state object and return a randomly generated state object at a future time.

  genesis() : Returns a default state or genesis state.
  """
  def __init__(self): 
    pass
  def forwardto(self,state, forwardtime):
    pass
  def genesis(self):
    pass
  
  def generatepath(self,initialstate, schedule):
    assert initialstate.time <= schedule[0]
    iterpath = itertools.accumulate(schedule, self.forwardto, initial=initialstate)
    return [initialstate] +[state for state in iterpath if state.time != initialstate.time ]  

class GeometricBrownianMotion(UnderlyingModel):
  def __init__(self, rate = 0.06, sigma = 0.2, dividend = 0):
    # To be modularized ...
    self.name = "Geometric Brownian Motion"
    self.rate = rate
    self.sigma = sigma
    self.dividend = dividend
    self.rng = np.random.default_rng()

  def forwardto(self,state,forwardtime):
    dt = forwardtime - state.time
    assert dt >= 0
    stateupdatedvalue = state.value * np.exp((self.rate - self.dividend - self.sigma ** 2.0 / 2.0) * dt + self.sigma * dt ** 0.5 * self.rng.standard_normal())
    
    return State(forwardtime, stateupdatedvalue)
  
  def genesis(self):
    return State(0.0,1.0)