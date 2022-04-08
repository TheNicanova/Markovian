from Token import *
from Layer import *


class Model:

    def get_token(self, paths, offer):
        pass

    def get_layer(self, paths, offer=None):
        pass


    def train(self, paths, offer):
        layers = self.get_layer(paths, offer)
        token = self.get_token(paths, offer)

        # payload = []

        for layer in layers:
            layer.update(token)
            token.update_cursor()
        return token


class LangStaff(Model):
    # TODO: Add the regression model in the input

    def get_token(self, paths, offer):
        return LangStaffToken(paths, offer)

    def get_layer(self, paths, offer=None):
        n = paths.get_length()
        layers = [LangStaffInitial(), *LangStaffLayer.wrap(n - 2), LangStaffTerminal()]
        return layers
