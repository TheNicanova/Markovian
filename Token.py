import numpy as np

class Token:
  def update_cursor(self):
    self.cursor = self.cursor - 1

  def get_precedent_cursor(self):
    return self.cursor + 1

  def set_cursor(self, i):
    self.cursor = i

class LangStaffToken(Token):
  def __init__(self, paths, offer):

    # References to the inital objects
    self.schedules = paths.get_time()
    self.coords = paths.get_coord()
    self.offers = offer.payoff(self.schedules, self.coords)
    self.offer = offer # Storing the pay_off model used


    self.policy = np.zeros(self.coords.shape)
    self.continuation = np.zeros(self.coords.shape)
    self.value = np.zeros(self.coords.shape)
    self.length = paths.get_length()
    self.cursor = self.length - 1

    # The cursor keeps track of where the Data is during it's initialization

