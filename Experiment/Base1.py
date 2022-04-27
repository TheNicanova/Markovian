from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Basic import *

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_lattice()

# 2. Get an objective function.
option = Put(1.3)

# 3. Get a pricing model and train it.
model = Basic(root, option)
model.train()

# 4. Consume the result

model.get_root_value()