# -*- encoding: utf-8 -*-
from __future__ import print_function
import abc
import collections
from supriya.tools.synthdeftools.UGenMethodMixin import UGenMethodMixin


class UGen(UGenMethodMixin):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_calculation_rate',
        '_inputs',
        '_output_proxies',
        '_special_index',
        )

    _ordered_input_names = ()

    _unexpanded_input_names = None

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        rate=None,
        special_index=0,
        **kwargs
        ):
        from supriya import synthdeftools
        assert isinstance(rate, synthdeftools.Rate), \
            rate
        self._calculation_rate = rate
        self._inputs = []
        self._special_index = special_index
        for i in range(len(self._ordered_input_names)):
            input_name = self._ordered_input_names[i]
            input_value = kwargs.get(input_name, None)
            if input_name in kwargs:
                input_value = kwargs[input_name]
                del(kwargs[input_name])
            prototype = (
                type(None),
                float,
                int,
                UGen,
                synthdeftools.OutputProxy,
                synthdeftools.Parameter,
                )
            if self._unexpanded_input_names and \
                input_name in self._unexpanded_input_names:
                prototype += (tuple,)
            assert isinstance(input_value, prototype), input_value
            self._configure_input(input_name, input_value)
        if kwargs:
            raise ValueError(kwargs)
        self._validate_inputs()
        self._output_proxies = tuple(
            synthdeftools.OutputProxy(self, i)
            for i in range(len(self))
            )

    ### SPECIAL METHODS ###

    def __getitem__(self, i):
        return self._output_proxies[i]

    def __len__(self):
        return 1

    def __repr__(self):
        from supriya.tools import synthdeftools
        if self.rate == synthdeftools.Rate.DEMAND:
            return '{}()'.format(type(self).__name__)
        calculation_abbreviations = {
            synthdeftools.Rate.AUDIO: 'ar',
            synthdeftools.Rate.CONTROL: 'kr',
            synthdeftools.Rate.SCALAR: 'ir',
            }
        string = '{}.{}()'.format(
            type(self).__name__,
            calculation_abbreviations[self.rate]
            )
        return string

    ### PRIVATE METHODS ###

    def _add_constant_input(self, value):
        self._inputs.append(float(value))

    def _add_ugen_input(self, ugen, output_index=None):
        from supriya import synthdeftools
        if isinstance(ugen, synthdeftools.Parameter):
            output_proxy = ugen
        elif isinstance(ugen, synthdeftools.OutputProxy):
            output_proxy = ugen
        else:
            output_proxy = synthdeftools.OutputProxy(
                output_index=output_index,
                source=ugen,
                )
        self._inputs.append(output_proxy)

    def _check_rate_same_as_first_input_rate(self):
        from supriya import synthdeftools
        first_input_rate = synthdeftools.Rate.from_input(
            self.inputs[0],
            )
        return self.rate == first_input_rate

    def _check_range_of_inputs_at_audio_rate(self, start=None, stop=None):
        from supriya import synthdeftools
        if self.rate != synthdeftools.Rate.AUDIO:
            return True
        for input_ in self.inputs[start:stop]:
            rate = synthdeftools.Rate.from_input(input_)
            if rate != synthdeftools.Rate.AUDIO:
                return False
        return True

    def _configure_input(self, name, value):
        from supriya import synthdeftools
        if isinstance(value, (int, float)):
            self._add_constant_input(value)
        elif isinstance(value, (
            synthdeftools.OutputProxy,
            synthdeftools.Parameter,
            synthdeftools.UGen,
            )):
            self._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        elif isinstance(value, tuple) and \
            all(isinstance(_, (int, float)) for _ in value):
            assert self._unexpanded_input_names
            assert name in self._unexpanded_input_names
            for x in value:
                self._add_constant_input(x)
        else:
            raise Exception(value)

    def _get_output_number(self):
        return 0

    def _get_outputs(self):
        return [self.rate]

    def _get_source(self):
        return self

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
        special_index=0,
        **kwargs
        ):
        import sys
        from supriya import synthdeftools
        if sys.version_info[0] == 2:
            import funcsigs
            get_signature = funcsigs.signature
        else:
            import inspect
            get_signature = inspect.signature
        input_dicts = UGen.expand_dictionary(
            kwargs, unexpanded_input_names=cls._unexpanded_input_names)
        ugens = []
        signature = get_signature(cls.__init__)
        has_custom_special_index = 'special_index' in signature.parameters
        for input_dict in input_dicts:
            if has_custom_special_index:
                ugen = cls._new_single(
                    rate=rate,
                    special_index=special_index,
                    **input_dict
                    )
            else:
                ugen = cls._new_single(
                    rate=rate,
                    **input_dict
                    )
            ugens.append(ugen)
        if len(ugens) == 1:
            return ugens[0]
        return synthdeftools.UGenArray(ugens)

    @classmethod
    def _new_single(
        cls,
        rate=None,
        **kwargs
        ):
        ugen = cls(
            rate=rate,
            **kwargs
            )
        return ugen

    def _optimize_graph(self):
        pass

    def _validate_inputs(self):
        pass

    ### PUBLIC METHODS ###

    @staticmethod
    def as_audio_rate_input(expr):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        if isinstance(expr, (int, float)):
            if expr == 0:
                return ugentools.Silence.ar()
            return ugentools.DC.ar(expr)
        elif isinstance(expr, (synthdeftools.UGen, synthdeftools.OutputProxy)):
            if expr.rate == synthdeftools.Rate.AUDIO:
                return expr
            return ugentools.K2A.ar(source=expr)
        elif isinstance(expr, collections.Iterable):
            return synthdeftools.UGenArray(
                UGen.as_audio_rate_input(x)
                for x in expr
                )
        raise ValueError(expr)

    def compile(self, synthdef):
        def compile_input_spec(i, synthdef):
            from supriya.tools import synthdeftools
            result = []
            if isinstance(i, float):
                result.append(SynthDef._encode_unsigned_int_32bit(0xffffffff))
                constant_index = synthdef._get_constant_index(i)
                result.append(SynthDef._encode_unsigned_int_32bit(
                    constant_index))
            elif isinstance(i, synthdeftools.OutputProxy):
                ugen = i.source
                output_index = i.output_index
                ugen_index = synthdef._get_ugen_index(ugen)
                result.append(SynthDef._encode_unsigned_int_32bit(ugen_index))
                result.append(SynthDef._encode_unsigned_int_32bit(output_index))
            else:
                raise Exception('Unhandled input spec: {}'.format(i))
            return bytes().join(result)
        from supriya.tools.synthdeftools import SynthDef
        from supriya.tools.synthdeftools import SynthDefCompiler
        outputs = self._get_outputs()
        result = []
        result.append(SynthDefCompiler.encode_string(type(self).__name__))
        result.append(SynthDefCompiler.encode_unsigned_int_8bit(self.rate))
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.inputs)))
        result.append(SynthDef._encode_unsigned_int_32bit(len(outputs)))
        result.append(SynthDef._encode_unsigned_int_16bit(int(self.special_index)))
        for i in self.inputs:
            result.append(compile_input_spec(i, synthdef))
        for o in outputs:
            result.append(SynthDefCompiler.encode_unsigned_int_8bit(o))
        result = bytes().join(result)
        return result

    @staticmethod
    def expand_dictionary(dictionary, unexpanded_input_names=None):
        r'''Expands a dictionary into multichannel dictionaries.

        ::

            >>> import supriya
            >>> dictionary = {'foo': 0, 'bar': (1, 2), 'baz': (3, 4, 5)}
            >>> result = supriya.synthdeftools.UGen.expand_dictionary(
            ...     dictionary)
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bar', 1), ('baz', 3), ('foo', 0)]
            [('bar', 2), ('baz', 4), ('foo', 0)]
            [('bar', 1), ('baz', 5), ('foo', 0)]

        ::

            >>> dictionary = {'bus': (8, 9), 'source': (1, 2, 3)}
            >>> result = supriya.synthdeftools.UGen.expand_dictionary(
            ...     dictionary,
            ...     unexpanded_input_names=('source',),
            ...     )
            >>> for x in result:
            ...     sorted(x.items())
            ...
            [('bus', 8), ('source', (1, 2, 3))]
            [('bus', 9), ('source', (1, 2, 3))]

        '''
        dictionary = dictionary.copy()
        cached_unexpanded_inputs = {}
        if unexpanded_input_names is not None:
            for input_name in unexpanded_input_names:
                if input_name not in dictionary:
                    continue
                cached_unexpanded_inputs[input_name] = \
                    dictionary[input_name]
                del(dictionary[input_name])
        maximum_length = 1
        result = []
        for name, value in dictionary.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(maximum_length, len(value))
        for i in range(maximum_length):
            result.append({})
            for name, value in dictionary.items():
                if isinstance(value, collections.Sequence):
                    value = value[i % len(value)]
                    result[i][name] = value
                else:
                    result[i][name] = value
        for expanded_inputs in result:
            expanded_inputs.update(cached_unexpanded_inputs)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def has_done_action(self):
        return 'done_action' in self._ordered_input_names

    @property
    def inputs(self):
        return tuple(self._inputs)

    @property
    def signal_range(self):
        from supriya.tools import synthdeftools
        return synthdeftools.SignalRange.BIPOLAR

    @property
    def rate(self):
        return self._calculation_rate

    @property
    def special_index(self):
        return self._special_index
