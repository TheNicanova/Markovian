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
out_of_money_put = Option.Put(1.1)
in_the_money_put = Option.Put(0.9)

# Specify the models

model_list = [
    PricingModel.Basic(),
    PricingModel.LongStaff(regression_model=Utility.Regression.Polynomial(2))
]

for model in model_list:
    model.train(paths, in_the_money_put)

for model in model_list:
    model.plot()
