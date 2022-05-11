import numpy as np
import pandas as pd


class BenchMark:

    def __init__(self, underlying_model, option):
        self.underlying_model = underlying_model
        self.option = option
        self.data_generator = underlying_model.generate_paths

    def price(self, model_list, n=100, m=100):
        frames = []
        i = 0
        for model in model_list:

            i += 1
            model_result = []

            for _ in range(m):
                data = self.data_generator(n=n)
                model.train(data, self.option)
                price = model.get_root_value()
                model_result.append(price)

            model_frame = pd.DataFrame(
                {
                    "Model Name": model.get_name() + str(i),
                    "Price": model_result
                }
            )
            frames.append(model_frame)
        return pd.concat(frames)
