from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Basic import *
from PricingModel.Langstaff import *
import copy

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_lattice()

root2 = copy.deepcopy(root)

# 2. Get an objective function.
option = Put(1.1)

# 3. Get a pricing model and train it.
model = LangStaff(regression_model=NearestNeighbors1D(1))
model2 = Basic()

model.train(root, option)
model2.train(root2, option)

# 4. Consume the result

model2.get_root_value()
model2.plot()

model.get_root_value()
model.plot()