import collections
from supriya import CalculationRate
from supriya.ugens.PureUGen import PureUGen


class BufDelayL(PureUGen):
    """
    A buffer-based linear-interpolating delay line unit generator.

    ::

        >>> buffer_id = 0
        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.BufDelayL.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        BufDelayL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Delay UGens"

    _ordered_input_names = collections.OrderedDict(
        [
            ("buffer_id", None),
            ("source", None),
            ("maximum_delay_time", 0.2),
            ("delay_time", 0.2),
        ]
    )

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
