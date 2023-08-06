import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha3_256(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha3_256(self, **kwargs).digest()
