import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha512(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha512(self, **kwargs).digest()
