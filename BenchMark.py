import OptimalStopping as stop

import pandas as pd


# Todo: Make the default parameters a config

def price(underlying_generator=None, option=Option.Put, model_list=None, n_list=[100], m=10):
    if underlying_generator is None:
        underlying_generator = UnderlyingModel.GeometricBrownianMotion()
    if model_list is None:
        model_list = [PricingModel.Basic()]

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
                model.train(data, option)
                root_price = model.get_root_value()

                result_dict["Model Name"].append(model.get_name())
                result_dict["Price"].append(root_price)
                result_dict["Number of Paths"].append(n)
                result_dict["Batch"].append(batch)
                result_dict["Options"].append(option.get_name())

    return pd.DataFrame(result_dict)
