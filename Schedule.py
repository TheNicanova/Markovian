
""" Should probably inherit from array/list instead of doing this."""

class Schedule:
  def __init__(self, *args):
        list.__init__(self, *args)


class Schedules:
  def __init__(self, *args):
        list.__init__(self, *args)