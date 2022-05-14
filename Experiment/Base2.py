from UnderlyingModel import *
from Option.Put import *
from PricingModel.Basic import *
from PricingModel.Langstaff import *
import copy

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_paths()

root2 = copy.deepcopy(root)

# 2. Get an objective function.
option = Put()

# 3. Get a pricing model and train it.
#model = LangStaff(regression_model=NearestNeighbors1D(1))

model = Rasmussen()

model.train(root, option)


# 4. Consume the result

model.get_root_value()
model.plot()
