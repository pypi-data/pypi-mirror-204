import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class blake2s(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.blake2s(self, **kwargs).digest()
