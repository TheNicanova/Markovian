import UnderlyingModel
import Option
import PricingModel

import Utility.Regression
from Utility.Schedule import *

# Generate Data

underlying_generator = UnderlyingModel.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)

data = underlying_generator.generate_paths(schedule=Linear(6), n=23)

# Specify the options
in_the_money_put = Option.Put(1.1)
out_the_money_put = Option.Put(0.9)

# Specify the model
model = PricingModel.Basic()

# Run the model on the data-option pair
model.train(data, in_the_money_put)

# Plot the result
model.plot()
data.get_root().plot()

