import numpy as np
import matplotlib.pyplot as plt
import Offer
import Schedule
from Path import *
from UnderlyingModel import *
from Path import *

um = GeometricBrownianMotion()
path = um.generate_path()
ppath = PPath(path)

paths = um.generate_paths()
schedules, coords = paths.get_schedule_coord()


paths = um.generate_paths(initialstate=State(0.0,5.0),n=19)
