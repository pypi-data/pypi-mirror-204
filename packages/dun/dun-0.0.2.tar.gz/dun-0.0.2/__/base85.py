from base64 import b85decode, b85encode

from __.base import Encoder, io, silent


class base85(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return b85encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return b85decode(self)
