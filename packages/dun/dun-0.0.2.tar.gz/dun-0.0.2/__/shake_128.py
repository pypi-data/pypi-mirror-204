import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class shake_128(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, n=16, data=None, **kwargs):
        return hashlib.shake_128(self, **kwargs).digest(n)
