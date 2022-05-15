import UnderlyingModel
import Option
import PricingModel
import BenchMark
import Plot

result_frame = BenchMark.price(
    underlying_generator=UnderlyingModel.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None),
    option=Option.Put(0.8),
    model_list=[PricingModel.Basic(), PricingModel.LongStaff()],
    n_list=[10, 20],
    m=10)

Plot.RidgePlot.plot(result_frame)
