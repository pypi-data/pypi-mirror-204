from base64 import b32decode, b32encode

from __.base import Encoder, io, silent


class base32(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return b32encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return b32decode(self)
