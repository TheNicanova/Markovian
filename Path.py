""" Should probably inherit from array/list instead of doing this."""
class Path:
  def __init__(self, statearray):
    self.statearray = statearray
  
  def atindex(self,i):
    return self.statearray[i]

class Paths:
  def __init__(self, arrayofpaths):
    self.arrayofpaths = arrayofpaths
  
  def atpath(self,j):
    return self.arrayofpaths[j]
  




  