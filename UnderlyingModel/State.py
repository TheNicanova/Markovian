class State:
  """
  The state object

  Attributes:
      time (float) : the total description of a situation includes the time
      data : the data describing the state

  """
  def __init__(self, time, data):
      self.time = time
      self.data = data

  def get_time(self):
      """
      Returns:
        the state's coordinate
      """
      return self.time

  def get_coord(self):
    '''
    Returns:
        the state's coordinate
    '''
    # could do some transformation of data
    return self.data