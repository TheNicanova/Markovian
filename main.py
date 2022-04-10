import UnderlyingGenerator
import Option
import PricingModel

# 1. Get some data.
um = UnderlyingGenerator.GeometricBrownianMotion()
root = um.generate_lattice()

# 2. Get an objective function.
call = Option.Call(0.3)

# 3. Get a pricing model and train it.
root = PricingModel.LangStaff(root, call).train()


# 4. Consume the result
root.plot_descendant()
