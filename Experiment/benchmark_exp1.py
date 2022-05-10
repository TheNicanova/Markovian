from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Langstaff import *
from PricingModel.Basic import *
from Plotting.RidgePlot import *
import copy
from Experiment.BenchMark import *
import matplotlib.pyplot as plt
import numpy as np

bm = BenchMark(GeometricBrownianMotion(), Put(0.9))

result = bm.price([LangStaff, Basic], n=100, m=100)

RidgePlot.plot(result)

#TODO Automate the naming of different models