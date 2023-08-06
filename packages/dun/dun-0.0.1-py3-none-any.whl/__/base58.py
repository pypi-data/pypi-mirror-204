from __.base import Encoder, io, silent
from base58 import b58decode, b58encode


class base58(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return b58encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return b58decode(self)
