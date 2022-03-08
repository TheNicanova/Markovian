import numpy as np
import itertools

class State:
  """
  Treated as an interface and storage.
  """
  def __init__(self, time, coord):
      self.time = time
      self.coord = coord

  def get_time(self):
    return self.time

  def get_coord(self):
    return self.coord
