import hashlib

from __.base import Hasher, io, nilbyte_p, silent


class sha384(Hasher):
    @io(nilbyte_p)
    @silent
    def hash(self, data=None, **kwargs):
        return hashlib.sha384(self, **kwargs).digest()
