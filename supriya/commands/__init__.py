"""
Tools for object-modeling OSC responses received from ``scsynth``.
"""
from .BufferAllocateReadChannelRequest import BufferAllocateReadChannelRequest  # noqa
from .BufferAllocateReadRequest import BufferAllocateReadRequest  # noqa
from .BufferAllocateRequest import BufferAllocateRequest  # noqa
from .BufferCloseRequest import BufferCloseRequest  # noqa
from .BufferCopyRequest import BufferCopyRequest  # noqa
from .BufferFillRequest import BufferFillRequest  # noqa
from .BufferFreeRequest import BufferFreeRequest  # noqa
from .BufferGenerateRequest import BufferGenerateRequest  # noqa
from .BufferGetContiguousRequest import BufferGetContiguousRequest  # noqa
from .BufferGetRequest import BufferGetRequest  # noqa
from .BufferInfoResponse import BufferInfoResponse  # noqa
from .BufferNormalizeRequest import BufferNormalizeRequest  # noqa
from .BufferQueryRequest import BufferQueryRequest  # noqa
from .BufferReadChannelRequest import BufferReadChannelRequest  # noqa
from .BufferReadRequest import BufferReadRequest  # noqa
from .BufferSetContiguousRequest import BufferSetContiguousRequest  # noqa
from .BufferSetContiguousResponse import BufferSetContiguousResponse  # noqa
from .BufferSetRequest import BufferSetRequest  # noqa
from .BufferSetResponse import BufferSetResponse  # noqa
from .BufferWriteRequest import BufferWriteRequest  # noqa
from .BufferZeroRequest import BufferZeroRequest  # noqa
from .ClearScheduleRequest import ClearScheduleRequest  # noqa
from .CommandRequest import CommandRequest  # noqa
from .ControlBusFillRequest import ControlBusFillRequest  # noqa
from .ControlBusGetContiguousRequest import ControlBusGetContiguousRequest  # noqa
from .ControlBusGetRequest import ControlBusGetRequest  # noqa
from .ControlBusSetContiguousRequest import ControlBusSetContiguousRequest  # noqa
from .ControlBusSetContiguousResponse import ControlBusSetContiguousResponse  # noqa
from .ControlBusSetRequest import ControlBusSetRequest  # noqa
from .ControlBusSetResponse import ControlBusSetResponse  # noqa
from .DoneResponse import DoneResponse  # noqa
from .DumpOscRequest import DumpOscRequest  # noqa
from .ErrorRequest import ErrorRequest  # noqa
from .FailResponse import FailResponse  # noqa
from .GroupDeepFreeRequest import GroupDeepFreeRequest  # noqa
from .GroupDumpTreeRequest import GroupDumpTreeRequest  # noqa
from .GroupFreeAllRequest import GroupFreeAllRequest  # noqa
from .GroupHeadRequest import GroupHeadRequest  # noqa
from .GroupNewRequest import GroupNewRequest  # noqa
from .GroupQueryTreeRequest import GroupQueryTreeRequest  # noqa
from .GroupTailRequest import GroupTailRequest  # noqa
from .MoveRequest import MoveRequest  # noqa
from .NodeAction import NodeAction  # noqa
from .NodeAfterRequest import NodeAfterRequest  # noqa
from .NodeBeforeRequest import NodeBeforeRequest  # noqa
from .NodeCommandRequest import NodeCommandRequest  # noqa
from .NodeFillRequest import NodeFillRequest  # noqa
from .NodeFreeRequest import NodeFreeRequest  # noqa
from .NodeInfoResponse import NodeInfoResponse  # noqa
from .NodeMapToAudioBusContiguousRequest import (
    NodeMapToAudioBusContiguousRequest,
)  # noqa
from .NodeMapToAudioBusRequest import NodeMapToAudioBusRequest  # noqa
from .NodeMapToControlBusContiguousRequest import (
    NodeMapToControlBusContiguousRequest,
)  # noqa
from .NodeMapToControlBusRequest import NodeMapToControlBusRequest  # noqa
from .NodeOrderRequest import NodeOrderRequest  # noqa
from .NodeQueryRequest import NodeQueryRequest  # noqa
from .NodeRunRequest import NodeRunRequest  # noqa
from .NodeSetContiguousRequest import NodeSetContiguousRequest  # noqa
from .NodeSetContiguousResponse import NodeSetContiguousResponse  # noqa
from .NodeSetRequest import NodeSetRequest  # noqa
from .NodeSetResponse import NodeSetResponse  # noqa
from .NodeTraceRequest import NodeTraceRequest  # noqa
from .NotifyRequest import NotifyRequest  # noqa
from .ParallelGroupNewRequest import ParallelGroupNewRequest  # noqa
from .QueryTreeControl import QueryTreeControl  # noqa
from .QueryTreeGroup import QueryTreeGroup  # noqa
from .QueryTreeResponse import QueryTreeResponse  # noqa
from .QueryTreeSynth import QueryTreeSynth  # noqa
from .QuitRequest import QuitRequest  # noqa
from .Request import Request  # noqa
from .RequestBundle import RequestBundle  # noqa
from .RequestId import RequestId  # noqa
from .RequestName import RequestName  # noqa
from .Requestable import Requestable  # noqa
from .Response import Response  # noqa
from .StatusRequest import StatusRequest  # noqa
from .StatusResponse import StatusResponse  # noqa
from .SyncRequest import SyncRequest  # noqa
from .SyncedResponse import SyncedResponse  # noqa
from .SynthDefFreeAllRequest import SynthDefFreeAllRequest  # noqa
from .SynthDefFreeRequest import SynthDefFreeRequest  # noqa
from .SynthDefLoadDirectoryRequest import SynthDefLoadDirectoryRequest  # noqa
from .SynthDefLoadRequest import SynthDefLoadRequest  # noqa
from .SynthDefReceiveRequest import SynthDefReceiveRequest  # noqa
from .SynthDefRemovedResponse import SynthDefRemovedResponse  # noqa
from .SynthGetContiguousRequest import SynthGetContiguousRequest  # noqa
from .SynthGetRequest import SynthGetRequest  # noqa
from .SynthNewRequest import SynthNewRequest  # noqa
from .SynthNewargsRequest import SynthNewargsRequest  # noqa
from .SynthNoidRequest import SynthNoidRequest  # noqa
from .TriggerResponse import TriggerResponse  # noqa
from .UgenCommandRequest import UgenCommandRequest  # noqa
