class Offer:
  def __init__(self):
    pass
  
  def amount(self,state):
    pass

class Call(Offer):
  def __init__(self,strikeprice):
    self.strike = strikeprice
  def amount(self, state):
    return max(0, state.value - self.strike)

