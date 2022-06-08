import OptimalStopping as ops
import OptimalStopping.BenchMark as benchmark


result = benchmark.price(
    underlying_generator=ops.UnderlyingModels.GeometricBrownianMotion(),
    option=ops.Options.Put(0.95),
    model_list=[
        ops.PricingModels.Basic(),
        ops.PricingModels.LongStaff(),
        ops.PricingModels.Rasmussen()
    ],
    n_list=[10, 20],
    m=10
)

result.plot()
