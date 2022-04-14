import numpy as np
from config import *


class Schedule(list):
    """
    Usage:
        Instantiation:
        Schedule(): A default schedule, e.g. [0.  , 0.05, ... ,  1.]
        Schedule(6):    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        Schedule(_,np.linspace(0,1,2)):     [0.0,1.0]
    """
    def __new__(cls, n=None, schedule=None):
        if schedule is not None:
            return list(schedule)

        if n is None and schedule is None:
            return list(np.linspace(default["initial_time"], default["terminal_time"], default["num_of_timestamps"]))

        if n is not None and schedule is None:
            return list(np.linspace(default["initial_time"], default["terminal_time"], n))


class Schedules(list):
    """
    Usage:
        Instantiation:
        Schedules(): A default list of schedule, e.g. [[0.  , 0.05, ... ,  1.], ...]
        Schedules(somelist): somelist
    """
    def __new__(cls, args):
        if args is None:
            return [Schedule() for _ in range(default["num_of_paths"])]
        else:
            return list(args)