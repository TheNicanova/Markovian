from Plotting.RidgePlot import *
from Experiment.BenchMark import *

bm = BenchMark(GeometricBrownianMotion(), Put(0.9))


model_list = [
              LangStaff(regression_model=NearestNeighbors1D(1)),
              Basic()
              ]

result = bm.price(model_list, n=10, m=100)

RidgePlot.plot(result)

model_list[0].plot()
model_list[1].plot()
