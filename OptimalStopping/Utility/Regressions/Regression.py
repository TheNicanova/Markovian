class Regression:

    def __init__(self, param=None):
        self.param = param

    def fit(self, source, target):
        pass

    def get_name(self) -> str:
        return self.__class__.__name__ + "(" + str(self.param) + ")"

    def can_fit(self, source, target) -> bool:
        return False

