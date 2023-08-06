from fastapi.requests import Request


class ElefantoRequest(Request):

    @property
    def pfm(self):
        pfm = self.scope['pfm']
        pfm.validate()
        return pfm
