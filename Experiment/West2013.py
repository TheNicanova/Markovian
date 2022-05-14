from Utility.Schedule import *
from UnderlyingModel import *
from Storage.NodeData import *
from Option.Put import *


gm = GeometricBrownianMotion(rate=0.1, sigma=0.3, dividend=0.02)

initial = NodeData(State(0, 135))

# Lattice

root = gm.generate_lattice(node=initial, schedule=Schedule(20))
root_2 = gm.generate_lattice(node=initial, schedule=Schedule(20))

binomial_tree = Basic()
binomial_tree.train(root, Put(135))


langstaff = LangStaff(regression_model=NearestNeighbors1D(5))
langstaff.train(root_2, Put(135))

lattice_price_bt = binomial_tree.get_root_value()
lattice_price_langstaff = langstaff.get_root_value()

# MonteCarlo

gm.generate_paths(node=initial, schedule=Schedule(20), n=4096)
langstaff = LangStaff(regression_model=NearestNeighbors1D(5))
langstaff.train(root_2, Put(135))

mc_price_langstaff = langstaff.get_root_value()





