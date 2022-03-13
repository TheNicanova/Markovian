from UnderlyingModel.UnderlyingGenerator import *
from UnderlyingModel.State import *
from Offer import *
from Regression import *
from Layer import *
from Model import *

um = GeometricBrownianMotion()

paths = um.generate_paths()
mycall = Call(1.1)
mymodel = LangStaff()

payload, token = mymodel.train(paths, mycall)



# Short term
# TODO: Plot the continuation function of the trained model.
# TODO: Plotter function for Token and for payload
# TODO: Make sure the number of paths and the length of the model is the same

# Long term
# TODO: Testing if we observe "early stopping" in the case of a call.

