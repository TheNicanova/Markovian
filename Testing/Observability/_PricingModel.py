from Testing.Observability._UnderlyingModel import *


import Option
import PricingModel



#### Options
out_of_money_put = Option.Put(1.1)
in_the_money_put = Option.Put(0.9)


model_list = [
    PricingModel.Basic(),
    PricingModel.LangStaff()
]

for model in model_list:
    model.train(paths, in_the_money_put)

for model in model_list:
    model.plot()

