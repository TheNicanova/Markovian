from UnderlyingModel.UnderlyingGenerator import *
from UnderlyingModel.State import *

um = GeometricBrownianMotion()

path = um.generate_path()
paths = um.generate_paths()
# paths = um.generate_paths(initial_state=State(0.0, 5.0), n=19)

schedule, coord = path.get_time_coord()
schedules, coords = paths.get_time_coord()


from Offer import *

mycall = Call(1.1)
mycall.payoff(3,4)


from Regression import *

mypolyreg = PolynomialRegression()
p = mypolyreg.fit(schedule, coord)

plt.plot(schedule, p(schedule))
path.plot()


from Data import *

mydata = Data(schedules, coords, mycall.payoff)

from Layer import *



myinitlayer = LangstaffInitial()
mylayer = LangstaffLayer()

myinitlayer.update(mydata)
mylayer.update(mydata)

paths.plot()
