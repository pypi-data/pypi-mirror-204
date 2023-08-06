from base64 import b64decode, b64encode

from __.base import Encoder, io, silent


class base64(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return b64encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return b64decode(self)
