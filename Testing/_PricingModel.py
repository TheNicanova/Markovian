import UnderlyingModel
import Option
import PricingModel

import Utility.Regression
import Utility.Schedule as Schedule

# Generate Data

underlying_generator = UnderlyingModel.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)

paths = underlying_generator.generate_paths(schedule=Schedule.Linear(6), n=23)
lattice = underlying_generator.generate_lattice(schedule=Schedule.Linear(9))

# Specify the options
in_the_money_put = Option.Put(1.1)
out_the_money_put = Option.Put(0.9)

# Specify the model
model = PricingModel.Basic()

# Run the model on the data-option pair
model.train(paths, in_the_money_put)

# Plot the result
model.plot()
paths.plot()

