import collections
from supriya.enums import CalculationRate
from supriya.ugens.UGen import UGen


class Timer(UGen):
    """

    ::

        >>> timer = supriya.ugens.Timer.ar(
        ...     trigger=0,
        ...     )
        >>> timer
        Timer.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        trigger=0,
        ):
        """
        Constructs an audio-rate Timer.

        ::

            >>> timer = supriya.ugens.Timer.ar(
            ...     trigger=0,
            ...     )
            >>> timer
            Timer.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        trigger=0,
        ):
        """
        Constructs a control-rate Timer.

        ::

            >>> timer = supriya.ugens.Timer.kr(
            ...     trigger=0,
            ...     )
            >>> timer
            Timer.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def trigger(self):
        """
        Gets `trigger` input of Timer.

        ::

            >>> timer = supriya.ugens.Timer.ar(
            ...     trigger=0,
            ...     )
            >>> timer.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
