import numpy as np

class Data():

  def __init__(self, schedules, coords, payoff_model):

    # References to the inital objects
    self.schedules = schedules
    self.coords = coords
    self.payoff_model = payoff_model

    # Allocating the relevant memory
    self.offers = payoff_model(schedules, coords)

    self.policy = np.zeros(coords.shape)
    self.continuation = np.zeros(coords.shape)
    self.value = np.zeros(coords.shape)

    # The cursor keeps track of where the Data is during it's initialization
    self.cursor = -1 # Initializing at the end

  def update_cursor(self):
    self.cursor = self.cursor - 1

  def get_precedent_cursor(self):
    return self.cursor + 1
