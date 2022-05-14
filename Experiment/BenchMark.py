import numpy as np
import pandas as pd


class BenchMark:

    def __init__(self, underlying_model, option):
        self.underlying_model = underlying_model
        self.option = option
        self.data_generator = underlying_model.generate_paths

    def price(self, model_list, n_list=[100], m=100):

        frames = []

        for model in model_list:

            for n in n_list:

                model_result = []

                for _ in range(m):
                    data = self.data_generator(n=n)
                    model.train(data, self.option)
                    price = model.get_root_value()
                    model_result.append(price)

                model_frame = pd.DataFrame(
                    {
                        "Model Name": model.get_name(),
                        "Price": model_result,
                        "n": n
                    }
                )
                frames.append(model_frame)
        return pd.concat(frames)
