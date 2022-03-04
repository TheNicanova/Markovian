import numpy as np

class Schedule(np.ndarray):
    def __new__(cls, arg):
        obj = np.asarray(arg).view(cls)
        return obj

    def __array_finalize__(self, obj):
        pass

class Schedules(list):
    def __init__(self, *args):
        list.__init__(self, *args)