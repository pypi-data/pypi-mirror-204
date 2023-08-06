import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class blake2b(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.blake2b(self, **kwargs).digest()
