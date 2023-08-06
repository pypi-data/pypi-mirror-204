from base64 import b16decode, b16encode

from __.base import Encoder, io, silent


class base16(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return b16encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return b16decode(self)
