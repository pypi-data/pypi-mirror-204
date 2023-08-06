import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha224(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha224(self, **kwargs).digest()
