import BenchMark
import UnderlyingModels
import PricingModels
import Options

result = BenchMark.price(
    underlying_generator=UnderlyingModels.GeometricBrownianMotion(),
    option=Options.Put(0.95),
    model_list=[
        PricingModels.Basic(),
        PricingModels.LongStaff(),
        PricingModels.Rasmussen()
    ],
    n_list=[10, 20, 100, 500],
    m=10
)

result.plot()
