from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Langstaff import *
from PricingModel.Basic import *
import copy

# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_paths(n=100)
root2 = copy.deepcopy(root)
root.plot_descendant()
root_lattice = um.generate_lattice()

# 2. Get an objective function.
option = Put(1.3)

# 3. Get pricing models
model_array = [LangStaff(root, option), Basic(root_lattice, option)]
for model in model_array:
    model.train()

# 4. Consume the result

a = Basic(root2, option)
a.train()


values = [model.get_root_value() for model in model_array]
