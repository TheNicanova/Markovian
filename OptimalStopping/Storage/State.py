class State:
    """
  The State object acts as storage for one underlying state.

  Attributes:
      time (float) : the total description of a situation includes the time.
      data : the data describing the state.

  """

    def __init__(self, time, data):
        self._time = time
        self._data = data

    def get_time(self):
        """
      Returns:
        the state's coordinate
      """
        return self._time

    def get_coord(self):
        """
    Returns:
        the state's coordinate
    """
        # could do some transformation of data
        return self._data
