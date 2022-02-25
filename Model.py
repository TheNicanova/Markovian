class Layer:
  def __init__(self):
    pass
  def continuation(self,state):
    pass
  def offer(self,state):
    return self.offer(state):
  def policy(self,state):
    if self.continuation(state) > self.offer(state): return False
    else: return True
  def value(self, state):
    return max(self.offer(state), self.continuation(state))

class BaseLayer(Layer):
  def __init__(self, offer): # offer is a function of state
    self.offer = offer
  
  def continuation(self,state, layerbelow): # Assuming offers are positive
    return - float('inf')

  def policy(self,state):
    return True

class Wrapper(Layer):
  def __init(self, offer, layerbelow):
    self.layerbelow = layerbelow
    self.offer = offer
    self.continuation
  


