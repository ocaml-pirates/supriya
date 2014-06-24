# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControl(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_rate',
        '_range',
        '_unit',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        range_=None,
        rate=None,
        unit=None,
        value=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        self._name = str(name)
        self._range = servertools.Range(range_)
        self._rate = synthdeftools.Rate.from_expr(rate)
        self._unit = unit
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def rate(self):
        return self._rate

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, expr):
        from supriya.tools import servertools
        if isinstance(expr, servertools.Bus):
            self._value = expr
        else:
            self._value = float(expr)
