from aiohttp.web import middleware, json_response, Request
from aiohttp.web_exceptions import HTTPException

from kaiju_tools.exceptions import APIException, InternalError, ClientError
from kaiju_tools.serialization import dumps

__all__ = ['error_middleware', 'handle_exception']


def handle_exception(request: Request, exc) -> APIException:
    """Transform an exception in APIException object."""
    if isinstance(exc, APIException):
        error = exc
    elif isinstance(exc, HTTPException):
        if exc.status_code >= 500:
            error = InternalError(message=str(exc), base_exc=exc)
        else:
            error = ClientError(message=str(exc), base_exc=exc)
    else:
        error = InternalError(message=str(exc), base_exc=exc)
    exc_info = exc if error.status_code >= 500 else None
    request.app.logger.error(str(exc), exc_info=exc_info)
    return error


@middleware
async def error_middleware(request: Request, handler):
    """Wrap an error in RPC exception."""
    try:
        response = await handler(request)
    except Exception as exc:
        exc = handle_exception(request, exc)
        response = json_response({'jsonrpc': '2.0', 'id': None, 'error': exc.repr()}, dumps=dumps)
    return response
