class Data():
  def __init__(self,schedules,coords, offer_model, pricing_model):
    self.schedules = schedules # a reference to the initial object
    self.coords = coords # a reference to the initial object
    self.offer_model = offer_model
    self.offers = np.zeros(coords.shape)  # 1
    self.policy = np.zeros(coords.shape) #

    self.continuation = np.zeros(coords.shape) # 3
    self.value = np.zeros(coords.shape) #4
    self.cursor = coords.shape[1] - 1