import _config
import Utility.Regression.Regression as Interface
import numpy as np
from sklearn.neighbors import KNeighborsRegressor


class NearestNeighbors1D(Interface.Regression):

    def __init__(self, param=_config.default["num_neighbor"]):
        super().__init__(param)
        self.param = param

    def fit(self, coord, target):
        knnr = KNeighborsRegressor(n_neighbors=self.param)
        knnr.fit(np.array(coord).reshape(-1, 1), target)
        return lambda x: knnr.predict([[x]])[0]

    def can_fit(self, coord, targets):
        return len(coord) > self.param
