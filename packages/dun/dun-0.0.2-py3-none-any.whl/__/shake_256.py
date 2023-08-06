import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class shake_256(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, n=32, data=None, **kwargs):
        return hashlib.shake_256(self, **kwargs).digest(n)
