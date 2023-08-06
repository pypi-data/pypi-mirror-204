import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha256(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha256(self, **kwargs).digest()
