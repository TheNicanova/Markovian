import OptimalStopping as ops
import OptimalStopping.Utility.Schedule as Schedule


# Generate Data
underlying_generator = ops.UnderlyingModels.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)

data = underlying_generator.generate_paths(schedule=Schedule.Linear(6), n=13)

# Specify the option
option = ops.Options.Put(0.9)

# Specify the model
model = ops.PricingModels.Rasmussen()

# Run the model on the data-option pair
model.train(data, option)

# Plot the result
model.plot()

