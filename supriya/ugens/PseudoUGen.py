import abc
import collections

from supriya import CalculationRate
from supriya.system.SupriyaObject import SupriyaObject


class PseudoUGen(SupriyaObject):

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError
