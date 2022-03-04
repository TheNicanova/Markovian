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

ppath.plot()

paths = um.generatepaths()
ppaths = PPaths(paths)
ppaths.plot()