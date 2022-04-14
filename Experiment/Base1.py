from Structure.UnderlyingGenerator import *
from Option.Call import *
from PricingModel.Langstaff import *

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_lattice()

# 2. Get an objective function.
call = Call(1.3)

# 3. Get a pricing model and train it.
model = LangStaff(root, call)
model.train()

# 4. Consume the result

model.get_root_value()