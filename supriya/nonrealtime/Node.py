import bisect
import collections
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import supriya  # noqa
from supriya import utils
from supriya.nonrealtime.NodeAction import NodeAction
from supriya.nonrealtime.SessionObject import SessionObject
from supriya.nonrealtime.State import State


class Node(SessionObject):
    """
    A non-realtime node.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Session Objects"

    __slots__ = ("_duration", "_events", "_session", "_session_id", "_start_offset")

    _valid_add_actions: Tuple[int, ...] = ()

    ### INITIALIZER ###

    def __init__(
        self,
        session,
        session_id: int,
        duration: float = None,
        start_offset: float = None,
    ) -> None:
        SessionObject.__init__(self, session)
        self._session_id = int(session_id)
        start_offset = start_offset or 0
        self._start_offset = float(start_offset)
        if duration is None:
            duration = float("inf")
        self._duration = duration
        self._events: Dict[str, List[Tuple[float, float]]] = {}

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        return "<{} #{} @{}:{}>".format(
            type(self).__name__, self.session_id, self.start_offset, self.stop_offset
        )

    ### SPECIAL METHODS ###

    def __getitem__(self, item: str) -> float:
        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        return self._get_at_offset(offset, item) or 0

    def __setitem__(
        self,
        item: str,
        value: Union[float, "supriya.nonrealtime.Bus", "supriya.nonrealtime.BusGroup"],
    ) -> None:
        import supriya.nonrealtime

        assert self.session._active_moments
        offset = self.session._active_moments[-1].offset
        assert isinstance(
            value, (int, float, supriya.nonrealtime.Bus, supriya.nonrealtime.BusGroup)
        )
        self._set_at_offset(offset, item, value)

    ### PRIVATE METHODS ###

    def _add_node(self, node: "Node", add_action: int) -> "Node":
        state = self.session._find_state_at(node.start_offset, clone_if_missing=True)
        state.start_nodes.add(node)
        if node not in state.nodes_to_children:
            state.nodes_to_children[node] = None
        state = self.session._find_state_at(node.stop_offset, clone_if_missing=True)
        state.stop_nodes.add(node)
        self.move_node(node, add_action=add_action)
        self.session.nodes.insert(node)
        self.session._apply_transitions([node.start_offset, node.stop_offset])
        return node

    def _collect_settings(self, offset: float, id_mapping=None, persistent=False):
        settings: Dict[str, float] = {}
        if persistent:
            for key in self._events:
                value = self._get_at_offset(offset, key) or 0.0
                if id_mapping and value in id_mapping:
                    value = id_mapping[value]
                settings[key] = value
        else:
            for key, events in self._events.items():
                events = events[:]
                for i, (event_offset, value) in enumerate(events):
                    # TODO: This is dreadfully inefficient.
                    if id_mapping and value in id_mapping:
                        value = id_mapping[value]
                        events[i] = (event_offset, value)
                index = bisect.bisect_left(events, (offset, 0.0))
                if len(events) <= index:
                    continue
                event_offset, value = events[index]
                if offset == event_offset:
                    settings[key] = value
        return settings

    def _fixup_duration(self, new_duration: float) -> None:
        old_duration = self._duration
        if old_duration == new_duration:
            return
        with self.session.at(self.stop_offset, propagate=False) as moment:
            if self in moment.state.stop_nodes:
                moment.state.stop_nodes.remove(self)
            moment.state._sparsify()
        self.session.nodes.remove(self)
        self._duration = new_duration
        self.session.nodes.insert(self)
        with self.session.at(self.stop_offset, propagate=False) as moment:
            moment.state.stop_nodes.add(self)

    def _fixup_events(self, new_node: "Node", split_offset: float) -> None:
        left_events: Dict[str, List[Tuple[float, float]]] = {}
        right_events: Dict[str, List[Tuple[float, float]]] = {}
        for name, events in self._events.items():
            for offset, value in events:
                if offset < split_offset:
                    left_events.setdefault(name, []).append((offset, value))
                else:
                    right_events.setdefault(name, []).append((offset, value))
        for name, events in left_events.items():
            if name in right_events and right_events[name][0][0] == split_offset:
                continue
            event = (split_offset, events[-1][-1])
            right_events.setdefault(name, []).insert(0, event)
        self._events = left_events
        new_node._events = right_events

    def _fixup_node_actions(
        self, new_node: "Node", start_offset: "float", stop_offset: "float"
    ) -> None:
        for offset in sorted(self.session.states):
            if offset < start_offset:
                continue
            elif stop_offset < offset:
                break
            transitions = self.session.states[offset].transitions
            if self in transitions:
                transitions[new_node] = transitions.pop(self)
            for node, action in transitions.items():
                if node is new_node:
                    continue
                if action.target is self:
                    action._target = new_node

    def _get_at_offset(self, offset: float, item: str) -> Optional[float]:
        """
        Relative to Node start offset.
        """
        events = self._events.get(item)
        if not events:
            return None
        index = bisect.bisect_left(events, (offset, 0.0))
        if len(events) <= index:
            old_offset, value = events[-1]
        else:
            old_offset, value = events[index]
        if old_offset == offset:
            return value
        index -= 1
        if index < 0:
            return None
        _, value = events[index]
        return value

    def _set_at_offset(self, offset, item, value):
        """
        Relative to Synth start offset.
        """
        if offset < self.start_offset or self.stop_offset <= offset:
            return
        events = self._events.setdefault(item, [])
        new_event = (offset, value)
        if not events:
            events.append(new_event)
            return
        index = bisect.bisect_left(events, new_event)
        if len(events) <= index:
            events.append(new_event)
        old_offset, old_value = events[index]
        if old_offset == offset:
            events[index] = (offset, value)
        else:
            events.insert(index, new_event)

    def _split(
        self,
        split_offset: float,
        new_nodes=None,
        split_occupiers: bool = True,
        split_traversers: bool = True,
    ) -> List["Node"]:
        import supriya.nonrealtime

        new_nodes = new_nodes or []
        state = self.session.states[split_offset]
        entering, exiting, occupying, starting, _ = self.inspect_children()
        children = state.nodes_to_children.get(self) or ()
        start_offset, stop_offset = self.start_offset, self.stop_offset
        if start_offset < split_offset < stop_offset:
            old_actions = state.transitions
            new_duration = stop_offset - split_offset
            with supriya.nonrealtime.DoNotPropagate():
                if isinstance(self, supriya.nonrealtime.Synth):
                    new_node = self.add_synth(
                        add_action="ADD_BEFORE",
                        duration=new_duration,
                        synthdef=self.synthdef,
                        **self._synth_kwargs,
                    )
                else:
                    new_node = self.add_group(
                        add_action="ADD_BEFORE", duration=new_duration
                    )
            new_nodes.append(new_node)
            new_actions: Dict["Node", NodeAction] = collections.OrderedDict()
            for node in new_nodes:
                if node is new_node and self in old_actions:
                    old_actions.pop(node)
                    action = old_actions.pop(self)
                    new_actions[node] = utils.new(action, source=new_node)
                else:
                    new_actions[node] = old_actions.pop(node)
            for child in reversed(children):
                if child in old_actions:
                    old_actions.pop(child)
                action = supriya.nonrealtime.NodeAction(
                    source=child, target=new_node, action="ADD_TO_TAIL"
                )
                new_actions[child] = action
            new_actions.update(old_actions)
            state._transitions = new_actions
            self._fixup_events(new_node, split_offset)
            self._fixup_duration(split_offset - start_offset)
            self._fixup_node_actions(new_node, split_offset, stop_offset)
            self.session._apply_transitions(
                [new_node.start_offset, new_node.stop_offset]
            )
            result = [self, new_node]
        else:
            return [self]
        for child in children + exiting:
            if (
                (split_occupiers and child in occupying)
                or (split_traversers and child in entering)
                or (split_traversers and child in exiting)
            ):
                child._split(
                    split_offset,
                    new_nodes=new_nodes,
                    split_occupiers=split_occupiers,
                    split_traversers=split_traversers,
                )
        return result

    ### CONSTRUCTORS ###

    @SessionObject.require_offset
    def add_group(
        self, add_action: int = None, duration: float = None, offset: float = None
    ) -> "supriya.nonrealtime.Group":
        import supriya.nonrealtime

        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = supriya.AddAction.from_expr(add_action)
        assert add_action in self._valid_add_actions
        session_id = self.session._get_next_session_id("node")
        node = supriya.nonrealtime.Group(
            self.session, duration=duration, session_id=session_id, start_offset=offset
        )
        self._add_node(node, add_action)
        return node

    @SessionObject.require_offset
    def add_synth(
        self,
        add_action: int = None,
        duration: float = None,
        synthdef=None,
        offset: float = None,
        **synth_kwargs,
    ) -> "supriya.nonrealtime.Synth":
        import supriya.assets.synthdefs
        import supriya.nonrealtime

        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = supriya.AddAction.from_expr(add_action)
        assert add_action in self._valid_add_actions
        session_id = self.session._get_next_session_id("node")
        synthdef = synthdef or supriya.assets.synthdefs.default
        node = supriya.nonrealtime.Synth(
            self.session,
            session_id=session_id,
            duration=duration,
            start_offset=offset,
            synthdef=synthdef,
            **synth_kwargs,
        )
        self._add_node(node, add_action)
        return node

    ### MUTATORS ###

    @SessionObject.require_offset
    def move_node(
        self, node: "Node", add_action: int = None, offset: float = None
    ) -> "Node":
        import supriya.nonrealtime

        state: State = self.session.active_moments[-1].state
        if state.nodes_to_parents is None:
            state._desparsify()
        if node in state.nodes_to_parents and node in self.get_parentage():
            raise ValueError("Can't add parent as a child.")
        if add_action is None:
            add_action = self._valid_add_actions[0]
        add_action = supriya.AddAction.from_expr(add_action)
        assert add_action in self._valid_add_actions
        node_action = supriya.nonrealtime.NodeAction(
            source=node, target=self, action=add_action
        )
        state.transitions[node] = node_action
        self.session._apply_transitions([state.offset, node.stop_offset])
        return node

    def delete(self) -> None:
        start_state = self.session._find_state_at(self.start_offset)
        start_state.start_nodes.remove(self)
        stop_state = self.session._find_state_at(self.stop_offset)
        stop_state.stop_nodes.remove(self)
        start_offset = self.session._find_state_before(
            self.start_offset, with_node_tree=True
        ).offset
        for state_one, state_two in self.session._iterate_state_pairs(
            start_offset, with_node_tree=True
        ):
            state_two._desparsify()
            if self in state_two.nodes_to_children:
                parent = state_two.nodes_to_parents.pop(self)
                inner_children = state_two.nodes_to_children.pop(self) or ()
                outer_children = list(state_two.nodes_to_children[parent])
                index = outer_children.index(self)
                outer_children[index : index + 1] = inner_children
                for child in inner_children:
                    state_two.nodes_to_parents[child] = parent
                state_two.nodes_to_children[parent] = tuple(outer_children) or None
            state_two._transitions = state_two._rebuild_transitions(
                state_one, state_two
            )
            if state_two == self.stop_offset:
                break
        self.session.nodes.remove(self)
        self.session._apply_transitions([self.start_offset, self.stop_offset])

    def set_duration(self, new_duration: float, clip_children: bool = False) -> "Node":
        import supriya.nonrealtime

        assert new_duration > 0
        if self.duration == new_duration:
            return self
        if new_duration < self.duration:
            split_offset = self.start_offset + new_duration
            if clip_children:
                with self.session.at(split_offset) as moment:
                    old_node, new_node = self.split(
                        split_occupiers=True, split_traversers=True
                    )
                    state = moment.state
                    children = reversed(
                        list(state._iterate_nodes(new_node, state.nodes_to_children))
                    )
                    for child in children:
                        child.delete()
            else:
                with self.session.at(split_offset):
                    old_node, new_node = self.split(
                        split_occupiers=False, split_traversers=False
                    )
                    new_node.delete()
            self.session._find_state_at(new_node.stop_offset)._sparsify()
            return old_node
        else:
            old_stop_offset = self.stop_offset
            new_stop_offset = self.start_offset + new_duration
            with self.session.at(old_stop_offset, propagate=False) as moment:
                parent = self.get_parent()
                moment.state.stop_nodes.remove(self)
                moment.state._sparsify()
            self._fixup_duration(new_duration)
            with self.session.at(old_stop_offset, propagate=False) as moment:
                moment.state._sparsify()
            while parent is not None and parent.stop_offset < new_stop_offset:
                with self.session.at(parent.stop_offset, propagate=False) as moment:
                    action = supriya.nonrealtime.NodeAction(
                        source=self, target=parent, action="ADD_BEFORE"
                    )
                    moment.state.transitions[self] = action
                    parent = parent.get_parent()
            with self.session.at(new_stop_offset, propagate=False) as moment:
                moment.state.stop_nodes.add(self)
            with self.session.at(self.start_offset, propagate=False) as moment:
                self.session._apply_transitions(moment.state.offset)
            self.session._apply_transitions(
                [self.start_offset, old_stop_offset, new_stop_offset]
            )
            return self

    @SessionObject.require_offset
    def split(
        self,
        split_occupiers: bool = True,
        split_traversers: bool = True,
        offset: float = None,
    ) -> List["Node"]:
        if offset is None:
            raise ValueError
        state = self.session.active_moments[-1].state
        self.session._apply_transitions(state.offset)
        shards = self._split(
            offset, split_occupiers=split_occupiers, split_traversers=split_traversers
        )
        stop_offset = shards[-1].stop_offset
        while state is not None and state.offset <= stop_offset:
            self.session._apply_transitions(state.offset)
            state = self.session._find_state_after(state.offset)
        return shards

    ### RELATIONS ###

    @SessionObject.require_offset
    def inspect_children(
        self, offset: float = None
    ) -> Tuple[
        Tuple["Node", ...],
        Tuple["Node", ...],
        Tuple["Node", ...],
        Tuple["Node", ...],
        Tuple["Node", ...],
    ]:
        this_state = self.session._find_state_at(offset, clone_if_missing=True)
        prev_state = self.session._find_state_before(this_state.offset, True)
        prev_state._desparsify()
        this_state._desparsify()
        prev_children = prev_state.nodes_to_children.get(self) or ()
        this_children = this_state.nodes_to_children.get(self) or ()
        entering: Set["Node"] = set()
        exiting: Set["Node"] = set()
        occupying: Set["Node"] = set()
        starting: Set["Node"] = set()
        stopping: Set["Node"] = set()
        for node in prev_children:
            if node.stop_offset == offset:
                stopping.add(node)
                continue
            if node in this_children:
                occupying.add(node)
            else:
                exiting.add(node)
        for node in this_children:
            if node.start_offset == offset:
                starting.add(node)
                continue
            if node.stop_offset == offset:
                stopping.add(node)
                continue
            if node in prev_children:
                occupying.add(node)
            else:
                entering.add(node)
        return (
            tuple(sorted(entering, key=lambda x: x.session_id)),
            tuple(sorted(exiting, key=lambda x: x.session_id)),
            tuple(sorted(occupying, key=lambda x: x.session_id)),
            tuple(sorted(starting, key=lambda x: x.session_id)),
            tuple(sorted(stopping, key=lambda x: x.session_id)),
        )

    @SessionObject.require_offset
    def get_parent(self, offset: float = None) -> Optional["Node"]:
        state = self.session._find_state_at(offset, clone_if_missing=True)
        if not state.nodes_to_children:
            state = self.session._find_state_before(state.offset, True)
        elif self.stop_offset == state.offset:
            state = self.session._find_state_before(state.offset, True)
        return state.nodes_to_parents.get(self)

    @SessionObject.require_offset
    def get_parentage(self, offset: float = None) -> List["Node"]:
        state = self.session._find_state_at(offset, clone_if_missing=True)
        if not state.nodes_to_children:
            state = self.session._find_state_before(state.offset, True)
        node = self
        parentage = [node]
        while state.nodes_to_parents[node] is not None:
            parent = state.nodes_to_parents[node]
            parentage.append(parent)
            node = parent
        return parentage

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def session_id(self) -> int:
        return self._session_id

    @property
    def start_offset(self) -> float:
        return self._start_offset

    @property
    def stop_offset(self) -> float:
        if self.duration is None:
            return float("inf")
        return self.start_offset + self.duration
