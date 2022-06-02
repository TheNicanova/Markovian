import pandas as pd
import OptimalStopping as ops
import copy


# Todo: Make the default parameters a config

def price(underlying_generator=None, option=ops.Options.Put(), model_list=None, n_list=None, m=10):
    if n_list is None:
        n_list = [100]
    if underlying_generator is None:
        underlying_generator = ops.UnderlyingModels.GeometricBrownianMotion()
    if model_list is None:
        model_list = [ops.PricingModels.Basic()]

    result_dict = {
        "Model Name": [],
        "Price": [],
        "Number of Paths": [],
        "Batch": [],
        "Options": []
    }

    for batch in range(m):
        for n in n_list:
            data = underlying_generator.generate_paths(n=n)
            for model in model_list:
                model.train(copy.deepcopy(data), option)
                root_price = model.get_root_value()

                result_dict["Model Name"].append(model.get_name())
                result_dict["Price"].append(root_price)
                result_dict["Number of Paths"].append(n)
                result_dict["Batch"].append(batch)
                result_dict["Options"].append(option.get_name())

    return pd.DataFrame(result_dict)
