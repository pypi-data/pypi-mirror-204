from base64 import a85decode, a85encode

from __.base import Encoder, io, silent


class ascii85(Encoder):
    @io()
    @silent
    def encode(self, data=None, **kwargs):
        return a85encode(self)

    @io()
    @silent
    def decode(self, data=None, **kwargs):
        return a85decode(self)
