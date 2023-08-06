from fastapi.requests import Request

from starlette.requests import empty_receive, empty_send
from starlette.types import Receive, Scope, Send


class ElefantoRequest(Request):

    def __init__(
            self,
            scope: Scope,
            receive: Receive = empty_receive,
            send: Send = empty_send,
    ):
        super().__init__(scope)

    @property
    def pfm(self):
        pfm = self.scope['pfm']
        pfm.validate()
        return pfm
