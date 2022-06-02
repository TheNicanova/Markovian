import OptimalStopping.BenchMark as benchmark
import OptimalStopping.Plot as plot
import OptimalStopping as ops

result = benchmark.price(
    underlying_generator=ops.UnderlyingModels.GeometricBrownianMotion(),
    option=ops.Options.Put(0.95),
    model_list=[
        ops.PricingModels.Basic(),
        ops.PricingModels.LongStaff()
    ],
    n_list=[10, 20, 30, 40],
    m=20
)

plot.RidgePlot.plot(result)
