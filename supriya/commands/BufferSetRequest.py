import supriya.osc
from supriya.commands.Request import Request
from supriya.commands.RequestId import RequestId


class BufferSetRequest(Request):
    """
    A /b_set request.

    ::

        >>> import supriya.commands
        >>> request = supriya.commands.BufferSetRequest(
        ...     buffer_id=23,
        ...     index_value_pairs=(
        ...         (0, 1.0),
        ...         (10, 13.2),
        ...         (17, 19.3),
        ...         ),
        ...     )
        >>> request
        BufferSetRequest(
            buffer_id=23,
            index_value_pairs=(
                (0, 1.0),
                (10, 13.2),
                (17, 19.3),
                ),
            )

    ::

        >>> message = request.to_osc()
        >>> message
        OscMessage(35, 23, 0, 1.0, 10, 13.2, 17, 19.3)

    ::

        >>> message.address == supriya.commands.RequestId.BUFFER_SET
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_buffer_id", "_index_value_pairs")

    request_id = RequestId.BUFFER_SET

    ### INITIALIZER ###

    def __init__(self, buffer_id=None, index_value_pairs=None):
        Request.__init__(self)
        self._buffer_id = int(buffer_id)
        if index_value_pairs:
            pairs = []
            for index, value in index_value_pairs:
                index = int(index)
                value = float(value)
                pair = (index, value)
                pairs.append(pair)
            pairs = tuple(pairs)
        self._index_value_pairs = index_value_pairs

    ### PUBLIC METHODS ###

    def to_osc(self, with_request_name=False):
        if with_request_name:
            request_id = self.request_name
        else:
            request_id = int(self.request_id)
        buffer_id = int(self.buffer_id)
        contents = [request_id, buffer_id]
        if self.index_value_pairs:
            for index, value in self.index_value_pairs:
                contents.append(index)
                contents.append(value)
        message = supriya.osc.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        return self._buffer_id

    @property
    def index_value_pairs(self):
        return self._index_value_pairs
