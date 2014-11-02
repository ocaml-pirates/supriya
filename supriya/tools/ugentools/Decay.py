# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Decay(Filter):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decay_time=None,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of Decay.

        ::

            >>> decay_time = 1.0
            >>> source = ugentools.In.kr(bus=0)
            >>> decay = ugentools.Decay.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay.decay_time
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Decay.

        ::

            >>> decay_time = 1.0
            >>> source = ugentools.In.kr(bus=0)
            >>> decay = ugentools.Decay.ar(
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    rate=<Rate.CONTROL: 1>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]