from UnderlyingModel.UnderlyingGenerator import *

um = GeometricBrownianMotion()
#node = um.generate_paths()
node = um.generate_lattice()
layers = node.bfs()




mylattice = um.generate_lattice()

mylattice[0][0].plot_descendant()

call = Call()

path = um.generate_path()
paths = um.generate_paths()

paths.plot3D(call)

model = LangStaff()

token = model.train(paths, call)
token.plot()

token.plot3D()# Short term

# TODO: Make sure the number of paths and the length of the model is the same

# Long term

from Offer import *
from UnderlyingModel.UnderlyingGenerator import *
from Token import *
from Model import *

um = GeometricBrownianMotion()
call = Call()


paths = um.generate_paths()

model = LangStaff()

token = model.train(paths, call)
token.plot3D()

token.plot()

paths.plot3D(call)


paths.plot3D(call)


