from UnderlyingGenerator import *
from Offer import *
from PricingModel import *

um = GeometricBrownianMotion()
root = um.generate_lattice()
root2 = um.generate_paths()

call = Call(0.3)

my_model = LangStaff(root, call)

my_model.train()
a = my_model.get_root_value()

root.plot_descendant()
