import abc
from typing import *

from kaiju_tools.serialization import Serializable
from kaiju_tools.exceptions import APIException

__all__ = ('JSONRPC', 'RPCMessage', 'RPCRequest', 'RPCResponse', 'RPCError')

JSONRPC = '2.0'  #: JSON RPC supported protocol version


class RPCMessage(Serializable, abc.ABC):
    """Base JSONRPC message class."""


class RPCRequest(RPCMessage):
    """Valid JSONRPC request."""

    __slots__ = ('id', 'method', 'params')

    def __init__(
        self,
        id: Union[int, None],
        method: str = None,
        params: Union[list, dict] = None,
        jsonrpc=None,  # noqa I know
    ):
        """Initialize."""
        self.id = id
        self.method = method
        self.params = params

    def repr(self):
        """Create a JSONRPC body."""
        data = {'jsonrpc': JSONRPC, 'id': self.id, 'method': self.method}
        if self.params:
            data['params'] = self.params
        return data


class RPCResponse(RPCMessage):
    """Valid JSON RPC response."""

    __slots__ = ('id', 'result')

    def __init__(self, id: Union[int, None], result: Any, jsonrpc=None):  # noqa I know
        """Initialize."""
        self.id = id
        self.result = result

    def repr(self):
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'result': self.result}


class RPCError(RPCMessage):
    """RPC error object."""

    __slots__ = ('id', 'error')

    def __init__(self, id: Union[int, None], error: APIException, jsonrpc=None):  # noqa I know
        """Initialize."""
        self.id = id
        self.error = error

    def repr(self) -> dict:
        """Create a JSONRPC body."""
        return {'jsonrpc': JSONRPC, 'id': self.id, 'error': self.error.repr()}
