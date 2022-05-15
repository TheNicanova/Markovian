import UnderlyingModel
import Option
import PricingModel

import pandas as pd


# Todo: Make the default parameters a config

def price(underlying_generator=None, option=Option.Put, model_list=None, n_list=[100], m=10, result_frame=None):
    if underlying_generator is None:
        underlying_generator = UnderlyingModel.GeometricBrownianMotion()
    if model_list is None:
        model_list = [PricingModel.Basic()]
    if result_frame is None:
        result_frame = pd.DataFrame()

    frame_list = [result_frame]

    for batch in range(m):
        for n in n_list:
            data = underlying_generator.generate_paths(n=n)
            for model in model_list:
                model.train(data, option)
                root_price = model.get_root_value()

                iteration_frame = pd.DataFrame({
                        "Model Name": [model.get_name()],
                        "Price": [root_price],
                        "Number of Paths": [n],
                        "Batch": [batch],
                        "Option": [option.get_name()]
                    })
                frame_list.append(iteration_frame)

    return pd.concat(frame_list)
