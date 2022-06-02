import OptimalStopping.BenchMark as benchmark
import OptimalStopping.Plot as plot

result = benchmark.price()

plot.RidgePlot.plot(result)
