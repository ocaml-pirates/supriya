# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class BRF(Filter):
    r'''A 2nd order Butterworth band-reject filter.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.In.ar(bus=0)
        >>> ugentools.BRF.ar(source=source)
        BRF.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'reciprocal_q',
        )

    ### PUBLIC METHODS ###

    def __init__(
        self,
        frequency=440,
        rate=None,
        reciprocal_q=1.0,
        source=None,
        ):
        Filter.__init__(
            self,
            frequency=frequency,
            rate=rate,
            reciprocal_q=reciprocal_q,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        reciprocal_q=1.0,
        source=None,
        ):
        r'''Creates an audio-rate band-reject filter.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.BRF.ar(
            ...     frequency=440,
            ...     reciprocal_q=1.0,
            ...     source=source,
            ...     )
            BRF.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_q=reciprocal_q,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        reciprocal_q=1.0,
        source=None,
        ):
        r'''Creates a control-rate band-reject filter.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.BRF.kr(
            ...     frequency=440,
            ...     reciprocal_q=1.0,
            ...     source=source,
            ...     )
            BRF.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            frequency=frequency,
            rate=rate,
            reciprocal_q=reciprocal_q,
            source=source,
            )
        return ugen