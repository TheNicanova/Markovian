# Short term
# TODO: Plot the continuation function of the trained model.
# TODO: Plotter function for Token and for payload
# TODO: Make sure the number of paths and the length of the model is the same

# Long term
# TODO: Testing if we observe "early stopping" in the case of a call.

from Offer import *
from UnderlyingModel.UnderlyingGenerator import *
from Token import *
from Model import *

um = GeometricBrownianMotion()
call = Call()

path = um.generate_path()
paths = um.generate_paths()

model = LangStaff()

token = model.train(paths, call)
token.plot()

token.plot3D()


