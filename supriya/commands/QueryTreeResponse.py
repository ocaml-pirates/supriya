from supriya.commands.Response import Response


class QueryTreeResponse(Response):

    ### CLASS VARIABLES ###

    __slots__ = ("_node_id", "_query_tree_group")

    ### INITIALIZER ###

    def __init__(self, node_id=None, osc_message=None, query_tree_group=None):
        Response.__init__(self, osc_message=osc_message)
        self._node_id = node_id
        self._query_tree_group = query_tree_group

    ### SPECIAL METHODS ###

    def __str__(self):
        return str(self._query_tree_group)

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        """
        Create response from OSC message.

        ::

            >>> message = supriya.osc.OscMessage('/g_queryTree.reply', 0, 0, 1, 1, 2, 1001, 0, 1000, 1, 1002, 0)
            >>> supriya.commands.QueryTreeResponse.from_osc_message(message)
            QueryTreeResponse(
                node_id=0,
                query_tree_group=QueryTreeGroup(
                    children=(
                        QueryTreeGroup(
                            children=(
                                QueryTreeGroup(
                                    children=(),
                                    node_id=1001,
                                    ),
                                QueryTreeGroup(
                                    children=(
                                        QueryTreeGroup(
                                            children=(),
                                            node_id=1002,
                                            ),
                                        ),
                                    node_id=1000,
                                    ),
                                ),
                            node_id=1,
                            ),
                        ),
                    node_id=0,
                    ),
                )

        ::

            >>> print(supriya.commands.QueryTreeResponse.from_osc_message(message))
            NODE TREE 0 group
                1 group
                    1001 group
                    1000 group
                        1002 group

        """

        def recurse(contents, control_flag):
            node_id = contents.pop(0)
            child_count = contents.pop(0)
            if child_count == -1:
                controls = []
                synthdef_name = contents.pop(0)
                if control_flag:
                    control_count = contents.pop(0)
                    for i in range(control_count):
                        control_name_or_index = contents.pop(0)
                        control_value = contents.pop(0)
                        control = supriya.commands.QueryTreeControl(
                            control_name_or_index=control_name_or_index,
                            control_value=control_value,
                        )
                        controls.append(control)
                controls = tuple(controls)
                result = supriya.commands.QueryTreeSynth(
                    node_id=node_id, synthdef_name=synthdef_name, controls=controls
                )
            else:
                children = []
                for i in range(child_count):
                    children.append(recurse(contents, control_flag))
                children = tuple(children)
                result = supriya.commands.QueryTreeGroup(
                    node_id=node_id, children=children
                )
            return result

        import supriya.commands

        contents = list(osc_message.contents)
        control_flag = bool(contents.pop(0))
        query_tree_group = recurse(contents, control_flag)
        response = cls(
            node_id=query_tree_group.node_id, query_tree_group=query_tree_group
        )
        return response

    def to_dict(self, flat=False):
        """
        Convert QueryTreeResponse to JSON-serializable dictionary.

        ::

            >>> query_tree_response = supriya.commands.QueryTreeResponse(
            ...     node_id=0,
            ...     query_tree_group=supriya.commands.QueryTreeGroup(
            ...         node_id=0,
            ...         children=(
            ...             supriya.commands.QueryTreeGroup(
            ...                 node_id=1,
            ...                 children=(
            ...                     supriya.commands.QueryTreeGroup(
            ...                         node_id=1002,
            ...                         children=(
            ...                             supriya.commands.QueryTreeSynth(
            ...                                 node_id=1105,
            ...                                 synthdef_name='dca557070c6b57164557041ac746fb3f',
            ...                                 controls=(
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='damping',
            ...                                         control_value=0.06623425334692,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='duration',
            ...                                         control_value=3.652155876159668,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='level',
            ...                                         control_value=0.894767701625824,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='out',
            ...                                         control_value=16.0,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='room_size',
            ...                                         control_value=0.918643176555634,
            ...                                         ),
            ...                                     ),
            ...                                 ),
            ...                             supriya.commands.QueryTreeSynth(
            ...                                 node_id=1098,
            ...                                 synthdef_name='cc754c63533fdcf412a44ef6adb1a8f0',
            ...                                 controls=(
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='duration',
            ...                                         control_value=5.701356887817383,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='level',
            ...                                         control_value=0.959683060646057,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='out',
            ...                                         control_value=16.0,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='pitch_dispersion',
            ...                                         control_value=0.040342573076487,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='pitch_shift',
            ...                                         control_value=10.517594337463379,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='time_dispersion',
            ...                                         control_value=0.666014134883881,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='window_size',
            ...                                         control_value=1.014111995697021,
            ...                                         ),
            ...                                     ),
            ...                                 ),
            ...                             supriya.commands.QueryTreeSynth(
            ...                                 node_id=1096,
            ...                                 synthdef_name='5cb6fb104ee1dc44d6b300e13112d37a',
            ...                                 controls=(
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='duration',
            ...                                         control_value=5.892660140991211,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='level',
            ...                                         control_value=0.159362614154816,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='out',
            ...                                         control_value=16.0,
            ...                                         ),
            ...                                     ),
            ...                                 ),
            ...                             supriya.commands.QueryTreeSynth(
            ...                                 node_id=1010,
            ...                                 synthdef_name='da0982184cc8fa54cf9d288a0fe1f6ca',
            ...                                 controls=(
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='out',
            ...                                         control_value=16.0,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='amplitude',
            ...                                         control_value=0.846831738948822,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='frequency',
            ...                                         control_value=1522.9603271484375,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='gate',
            ...                                         control_value=0.0,
            ...                                         ),
            ...                                     supriya.commands.QueryTreeControl(
            ...                                         control_name_or_index='pan',
            ...                                         control_value=0.733410477638245,
            ...                                         ),
            ...                                     ),
            ...                                 ),
            ...                             ),
            ...                         ),
            ...                     supriya.commands.QueryTreeSynth(
            ...                         node_id=1003,
            ...                         synthdef_name='454b69a7c505ddecc5b39762d291a5ec',
            ...                         controls=(
            ...                             supriya.commands.QueryTreeControl(
            ...                                 control_name_or_index='done_action',
            ...                                 control_value=2.0,
            ...                                 ),
            ...                             supriya.commands.QueryTreeControl(
            ...                                 control_name_or_index='fade_time',
            ...                                 control_value=0.019999999552965,
            ...                                 ),
            ...                             supriya.commands.QueryTreeControl(
            ...                                 control_name_or_index='gate',
            ...                                 control_value=1.0,
            ...                                 ),
            ...                             supriya.commands.QueryTreeControl(
            ...                                 control_name_or_index='in_',
            ...                                 control_value=16.0,
            ...                                 ),
            ...                             supriya.commands.QueryTreeControl(
            ...                                 control_name_or_index='out',
            ...                                 control_value=0.0,
            ...                                 ),
            ...                             ),
            ...                         ),
            ...                     ),
            ...                 ),
            ...             supriya.commands.QueryTreeSynth(
            ...                 node_id=1000,
            ...                 synthdef_name='72696657e1216698c415e704ea8ab9a2',
            ...                 controls=(
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_clamp_time',
            ...                         control_value=0.009999999776483,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_postgain',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_pregain',
            ...                         control_value=6.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_relax_time',
            ...                         control_value=0.100000001490116,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_slope_above',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_slope_below',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_1_threshold',
            ...                         control_value=0.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_clamp_time',
            ...                         control_value=0.009999999776483,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_postgain',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_pregain',
            ...                         control_value=3.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_relax_time',
            ...                         control_value=0.100000001490116,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_slope_above',
            ...                         control_value=0.5,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_slope_below',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_2_threshold',
            ...                         control_value=-6.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_clamp_time',
            ...                         control_value=0.009999999776483,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_postgain',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_pregain',
            ...                         control_value=-3.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_relax_time',
            ...                         control_value=0.100000001490116,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_slope_above',
            ...                         control_value=0.25,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_slope_below',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_3_threshold',
            ...                         control_value=-12.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_clamp_time',
            ...                         control_value=0.009999999776483,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_postgain',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_pregain',
            ...                         control_value=-3.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_relax_time',
            ...                         control_value=0.100000001490116,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_slope_above',
            ...                         control_value=0.125,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_slope_below',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='band_4_threshold',
            ...                         control_value=-18.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='frequency_1',
            ...                         control_value=200.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='frequency_2',
            ...                         control_value=2000.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='frequency_3',
            ...                         control_value=5000.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='in_',
            ...                         control_value=0.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='out',
            ...                         control_value=0.0,
            ...                         ),
            ...                     ),
            ...                 ),
            ...             supriya.commands.QueryTreeSynth(
            ...                 node_id=1001,
            ...                 synthdef_name='c1aa521afab5b0c0ce3d744690951649',
            ...                 controls=(
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='level',
            ...                         control_value=1.0,
            ...                         ),
            ...                     supriya.commands.QueryTreeControl(
            ...                         control_name_or_index='out',
            ...                         control_value=0.0,
            ...                         ),
            ...                     ),
            ...                 ),
            ...             ),
            ...         ),
            ...     )

        ::

            >>> import json
            >>> result = query_tree_response.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "server_tree": {
                    "children": [
                        {
                            "children": [
                                {
                                    "children": [
                                        {
                                            "controls": {
                                                "damping": 0.06623425334692,
                                                "duration": 3.652155876159668,
                                                "level": 0.894767701625824,
                                                "out": 16.0,
                                                "room_size": 0.918643176555634
                                            },
                                            "node_id": 1105,
                                            "synthdef": "dca557070c6b57164557041ac746fb3f"
                                        },
                                        {
                                            "controls": {
                                                "duration": 5.701356887817383,
                                                "level": 0.959683060646057,
                                                "out": 16.0,
                                                "pitch_dispersion": 0.040342573076487,
                                                "pitch_shift": 10.517594337463379,
                                                "time_dispersion": 0.666014134883881,
                                                "window_size": 1.014111995697021
                                            },
                                            "node_id": 1098,
                                            "synthdef": "cc754c63533fdcf412a44ef6adb1a8f0"
                                        },
                                        {
                                            "controls": {
                                                "duration": 5.892660140991211,
                                                "level": 0.159362614154816,
                                                "out": 16.0
                                            },
                                            "node_id": 1096,
                                            "synthdef": "5cb6fb104ee1dc44d6b300e13112d37a"
                                        },
                                        {
                                            "controls": {
                                                "amplitude": 0.846831738948822,
                                                "frequency": 1522.9603271484375,
                                                "gate": 0.0,
                                                "out": 16.0,
                                                "pan": 0.733410477638245
                                            },
                                            "node_id": 1010,
                                            "synthdef": "da0982184cc8fa54cf9d288a0fe1f6ca"
                                        }
                                    ],
                                    "node_id": 1002
                                },
                                {
                                    "controls": {
                                        "done_action": 2.0,
                                        "fade_time": 0.019999999552965,
                                        "gate": 1.0,
                                        "in_": 16.0,
                                        "out": 0.0
                                    },
                                    "node_id": 1003,
                                    "synthdef": "454b69a7c505ddecc5b39762d291a5ec"
                                }
                            ],
                            "node_id": 1
                        },
                        {
                            "controls": {
                                "band_1_clamp_time": 0.009999999776483,
                                "band_1_postgain": 1.0,
                                "band_1_pregain": 6.0,
                                "band_1_relax_time": 0.100000001490116,
                                "band_1_slope_above": 1.0,
                                "band_1_slope_below": 1.0,
                                "band_1_threshold": 0.0,
                                "band_2_clamp_time": 0.009999999776483,
                                "band_2_postgain": 1.0,
                                "band_2_pregain": 3.0,
                                "band_2_relax_time": 0.100000001490116,
                                "band_2_slope_above": 0.5,
                                "band_2_slope_below": 1.0,
                                "band_2_threshold": -6.0,
                                "band_3_clamp_time": 0.009999999776483,
                                "band_3_postgain": 1.0,
                                "band_3_pregain": -3.0,
                                "band_3_relax_time": 0.100000001490116,
                                "band_3_slope_above": 0.25,
                                "band_3_slope_below": 1.0,
                                "band_3_threshold": -12.0,
                                "band_4_clamp_time": 0.009999999776483,
                                "band_4_postgain": 1.0,
                                "band_4_pregain": -3.0,
                                "band_4_relax_time": 0.100000001490116,
                                "band_4_slope_above": 0.125,
                                "band_4_slope_below": 1.0,
                                "band_4_threshold": -18.0,
                                "frequency_1": 200.0,
                                "frequency_2": 2000.0,
                                "frequency_3": 5000.0,
                                "in_": 0.0,
                                "out": 0.0
                            },
                            "node_id": 1000,
                            "synthdef": "72696657e1216698c415e704ea8ab9a2"
                        },
                        {
                            "controls": {
                                "level": 1.0,
                                "out": 0.0
                            },
                            "node_id": 1001,
                            "synthdef": "c1aa521afab5b0c0ce3d744690951649"
                        }
                    ],
                    "node_id": 0
                }
            }

        ::

            >>> result = query_tree_response.to_dict(flat=True)
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "server_tree": [
                    {
                        "children": [
                            1,
                            1000,
                            1001
                        ],
                        "node_id": 0,
                        "parent": null
                    },
                    {
                        "children": [
                            1002,
                            1003
                        ],
                        "node_id": 1,
                        "parent": 0
                    },
                    {
                        "children": [
                            1105,
                            1098,
                            1096,
                            1010
                        ],
                        "node_id": 1002,
                        "parent": 1
                    },
                    {
                        "controls": {
                            "damping": 0.06623425334692,
                            "duration": 3.652155876159668,
                            "level": 0.894767701625824,
                            "out": 16.0,
                            "room_size": 0.918643176555634
                        },
                        "node_id": 1105,
                        "parent": 1002,
                        "synthdef": "dca557070c6b57164557041ac746fb3f"
                    },
                    {
                        "controls": {
                            "duration": 5.701356887817383,
                            "level": 0.959683060646057,
                            "out": 16.0,
                            "pitch_dispersion": 0.040342573076487,
                            "pitch_shift": 10.517594337463379,
                            "time_dispersion": 0.666014134883881,
                            "window_size": 1.014111995697021
                        },
                        "node_id": 1098,
                        "parent": 1002,
                        "synthdef": "cc754c63533fdcf412a44ef6adb1a8f0"
                    },
                    {
                        "controls": {
                            "duration": 5.892660140991211,
                            "level": 0.159362614154816,
                            "out": 16.0
                        },
                        "node_id": 1096,
                        "parent": 1002,
                        "synthdef": "5cb6fb104ee1dc44d6b300e13112d37a"
                    },
                    {
                        "controls": {
                            "amplitude": 0.846831738948822,
                            "frequency": 1522.9603271484375,
                            "gate": 0.0,
                            "out": 16.0,
                            "pan": 0.733410477638245
                        },
                        "node_id": 1010,
                        "parent": 1002,
                        "synthdef": "da0982184cc8fa54cf9d288a0fe1f6ca"
                    },
                    {
                        "controls": {
                            "done_action": 2.0,
                            "fade_time": 0.019999999552965,
                            "gate": 1.0,
                            "in_": 16.0,
                            "out": 0.0
                        },
                        "node_id": 1003,
                        "parent": 1,
                        "synthdef": "454b69a7c505ddecc5b39762d291a5ec"
                    },
                    {
                        "controls": {
                            "band_1_clamp_time": 0.009999999776483,
                            "band_1_postgain": 1.0,
                            "band_1_pregain": 6.0,
                            "band_1_relax_time": 0.100000001490116,
                            "band_1_slope_above": 1.0,
                            "band_1_slope_below": 1.0,
                            "band_1_threshold": 0.0,
                            "band_2_clamp_time": 0.009999999776483,
                            "band_2_postgain": 1.0,
                            "band_2_pregain": 3.0,
                            "band_2_relax_time": 0.100000001490116,
                            "band_2_slope_above": 0.5,
                            "band_2_slope_below": 1.0,
                            "band_2_threshold": -6.0,
                            "band_3_clamp_time": 0.009999999776483,
                            "band_3_postgain": 1.0,
                            "band_3_pregain": -3.0,
                            "band_3_relax_time": 0.100000001490116,
                            "band_3_slope_above": 0.25,
                            "band_3_slope_below": 1.0,
                            "band_3_threshold": -12.0,
                            "band_4_clamp_time": 0.009999999776483,
                            "band_4_postgain": 1.0,
                            "band_4_pregain": -3.0,
                            "band_4_relax_time": 0.100000001490116,
                            "band_4_slope_above": 0.125,
                            "band_4_slope_below": 1.0,
                            "band_4_threshold": -18.0,
                            "frequency_1": 200.0,
                            "frequency_2": 2000.0,
                            "frequency_3": 5000.0,
                            "in_": 0.0,
                            "out": 0.0
                        },
                        "node_id": 1000,
                        "parent": 0,
                        "synthdef": "72696657e1216698c415e704ea8ab9a2"
                    },
                    {
                        "controls": {
                            "level": 1.0,
                            "out": 0.0
                        },
                        "node_id": 1001,
                        "parent": 0,
                        "synthdef": "c1aa521afab5b0c0ce3d744690951649"
                    }
                ]
            }

        """

        def recurse(node, parent_node_id, nodes):
            if "synthdef" in node:
                node["parent"] = parent_node_id
                nodes.append(node)
            else:
                group = {
                    "node_id": node["node_id"],
                    "parent": parent_node_id,
                    "children": [x["node_id"] for x in node["children"]],
                }
                nodes.append(group)
                for x in node["children"]:
                    recurse(x, node["node_id"], nodes)

        data = self.query_tree_group.to_dict()
        if not flat:
            return {"server_tree": data}
        nodes = []
        recurse(data, None, nodes)
        return {"server_tree": nodes}

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def query_tree_group(self):
        return self._query_tree_group
