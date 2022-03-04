import numpy as np
import matplotlib.pyplot as plt
import Offer
import Schedule
from Path import *
from UnderlyingModel import *
from Path import *

um = GeometricBrownianMotion()
path = um.generatepath()
ppath = PPath(path)

paths = um.generatepaths()
ppaths = PPaths(paths)

paths = um.generatepaths(initialstate=State(0.0,5.0),n=7)
ppaths = PPaths(paths)
ppaths.plot()