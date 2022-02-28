
class Layer:
  """
  The builder interface. It declared product construction steps that are common to all types of builders.
  """
  def __init__(self):
    pass
  def continuation(self, state, layerbelow = None):
    pass
  def offer(self,state, layerbelow= None):
    return self.offer(state)
  def policy(self,state, layerbelow = None):
    if self.continuation(state) > self.offer(state): return False
    else: return True
  def value(self, state, layerbelow = None):
    return max(self.offer(state), self.continuation(state))

class BaseLayer(Layer):
  def __init__(self, offer): # offer is a function of state
    self.offer = offer
  
  def continuation(self,state, layerbelow): # Assuming offers are positive
    return - float('inf')

  def policy(self,state):
    return True


  


