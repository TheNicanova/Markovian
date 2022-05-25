class Regression:

    def __init__(self, param=None):
        self.param = param

    def fit(self, coord, targets):
        pass

    def get_name(self) -> str:
        return self.__class__.__name__ + "(" + str(self.param) + ")"

    def can_fit(self, coord, targets) -> bool:
        return False

