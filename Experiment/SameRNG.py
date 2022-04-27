from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Langstaff import *
from PricingModel.Basic import *
import copy

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_paths(n=8)
root2 = copy.deepcopy(root)
root3 = um.generate_lattice()


# 2. Get an objective function.
option = Put(0.9)

# 3. Get pricing models
model_array = [LangStaff(root, option), Basic(root2, option), Basic(root3, option)]
for model in model_array:
    model.train()

# 4. Consume the result

values = [model.get_root_value() for model in model_array]

model_array[1].plot()