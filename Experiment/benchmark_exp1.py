from Plotting.RidgePlot import *
from Experiment.BenchMark import *

bm = BenchMark(GeometricBrownianMotion(regression_model=Regression(4)), Put(0.9))


model_list = [
            Basic(),
            LangStaff()
              ]

result = bm.price(model_list, n_list=[10, 20], m=50)



RidgePlot.plot(result)


