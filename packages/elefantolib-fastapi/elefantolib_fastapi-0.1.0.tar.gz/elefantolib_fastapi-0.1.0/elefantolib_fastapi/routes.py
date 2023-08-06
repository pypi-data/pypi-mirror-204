from typing import Any, Callable, Coroutine

from elefantolib import context
from elefantolib.provider import fastapi_provider

from fastapi import Request, Response
from fastapi.routing import APIRoute

from .requests import ElefantoRequest


class ElefantoRoute(APIRoute):

    def get_route_handler(self) -> \
            Callable[[Request], Coroutine[Any, Any, Response]]:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            pvr = fastapi_provider.FastAPIProvider(request=request)
            request.scope['pfm'] = context.AsyncPlatformContext(pvr=pvr)
            new_request = ElefantoRequest(request.scope, request.receive)
            return await original_route_handler(new_request)
        return custom_route_handler
