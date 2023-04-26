import Utility.Schedule as Schedule
import UnderlyingModels
import PricingModels
import Options

# Generate Data
underlying_generator = UnderlyingModels.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)

data = underlying_generator.generate_paths(schedule=Schedule.Linear(6), n=6)

# Specify the option
option = Options.Put(1.1)

# Specify the model
model = PricingModels.LongStaff()

# Run the model on the data-option pair
model.train(data, option)

# Plot the result
data.get_root().plot()
model.plot()


