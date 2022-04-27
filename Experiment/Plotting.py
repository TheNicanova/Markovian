from Structure.UnderlyingGenerator import *
from Option.Put import *
from PricingModel.Langstaff import *
import copy



# 1. Get some data.
um = GeometricBrownianMotion()
root = um.generate_paths()


# 2. Get an objective function.
option = Put(1.3)


# 3. Get a pricing model and train it.
model = LangStaff(root, option)
model.train()
model.plot()

