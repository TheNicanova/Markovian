import OptimalStopping as ops
import OptimalStopping.BenchMark as benchmark
import OptimalStopping.Plot as my_plot

result = benchmark.price(
    underlying_generator=ops.UnderlyingModels.GeometricBrownianMotion(),
    option=ops.Options.Put(0.95),
    model_list=[
        ops.PricingModels.Basic(),
        ops.PricingModels.LongStaff()
    ],
    n_list=[10, 20],
    m=10
)

result.plot()
