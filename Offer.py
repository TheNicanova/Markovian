class Offer:
  """
  A function of state. The reward, or the value/amount offered.
  """
  def __init__(self):
    pass
  
  def amount(self,state):
    pass

class Call(Offer):
  """
  A call option
  """
  def __init__(self,strikeprice):
    self.strike = strikeprice
  def amount(self, state):
    return max(0, state.value - self.strike)

