import UnderlyingModel

import Utility.Schedule as Schedule

underlying_generator = UnderlyingModel.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)


paths = underlying_generator.generate_paths(schedule=Schedule.Linear(6), n=13)
lattice = underlying_generator.generate_lattice(schedule=Schedule.Linear(50))

paths.plot()
lattice.plot()

