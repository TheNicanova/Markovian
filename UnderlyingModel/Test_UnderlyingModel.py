import UnderlyingModel
import Utility

underlying_generator = UnderlyingModel.GeometricBrownianMotion(rate=0.0, sigma=0.2, dividend=None)


paths_root, paths_layers = underlying_generator.generate_paths(schedule=Utility.Linear(6), n=13)
lattice_root, lattice_layers = underlying_generator.generate_lattice(schedule=Utility.Linear(50))

paths_root.plot()
lattice_root.plot()

