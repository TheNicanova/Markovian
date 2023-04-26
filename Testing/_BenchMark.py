import OptimalStopping.UnderlyingModel
import Option
from PricingModel import *
import BenchMark
import Plot
import Utility

""" Something to be checked out"""

result_frame = BenchMark.price(
    underlying_generator=UnderlyingModel.GeometricBrownianMotion(),
    option=Option.Put(),
    model_list=[Basic(), LongStaff(), Rasmussen()],
    n_list=[10, 20, 40, 80, 160],
    m=30)


Plot.RidgePlot.plot(result_frame)

